#!/usr/bin/env python3
"""
test_idea_intake.py — unit tests for the quest-idea intake collector.

Run:  python3 scripts/quest/test_idea_intake.py       (or: python3 -m unittest ...)
Exits non-zero on any failure (suitable for CI).

These tests pin the behaviours the intake lane's gatekeeping depends on: the
issue-form heading parser (including `_No response_` and duplicate headings),
the readiness rubric's thresholds, the conservative spam signals, controlled-
vocabulary normalization, and the duplicate radar.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _load(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / relpath)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


intake = _load("idea_intake", "scripts/quest/idea_intake.py")

NO_NETWORK = Path("/nonexistent/quest-network.json")


def form_body(**overrides) -> str:
    """Render a well-formed issue-form body, with per-field overrides."""
    fields = {
        "What's the quest idea?": (
            "Build a self-healing uptime monitor: a GitHub Actions cron pings the "
            "site, and on failure it opens an issue and rolls back the last deploy "
            "with `git revert`. Learners wire the loop and watch it catch a staged outage."
        ),
        "Why does it matter?": (
            "It turns CI/CD from a buzzword into an operational reflex learners can feel."
        ),
        "Learning objectives": (
            "- Schedule a GitHub Actions cron workflow\n"
            "- Trigger a rollback from a workflow\n"
            "- Open and label an incident issue automatically"
        ),
        "Character path (skill focus)": "devops",
        "Level (binary progression)": "0101",
        "Difficulty": "🟡 Medium",
        "Tools & technologies": "github-actions, bash, git",
        "Similar existing quests you checked": "_No response_",
    }
    fields.update(overrides)
    return "\n".join(f"### {label}\n\n{value}\n" for label, value in fields.items())


class TestFieldParsing(unittest.TestCase):
    def test_all_fields_extracted(self):
        fields = intake.parse_fields(form_body())
        self.assertIn("uptime monitor", fields["summary"])
        self.assertIn("operational reflex", fields["why"])
        self.assertEqual(fields["path"], "devops")
        self.assertEqual(fields["level"], "0101")
        self.assertEqual(fields["technologies"], "github-actions, bash, git")

    def test_no_response_becomes_empty(self):
        fields = intake.parse_fields(form_body())
        self.assertEqual(fields["existing"], "")

    def test_heading_apostrophe_variants(self):
        body = form_body().replace("What's the quest idea?", "What’s the quest idea?")
        fields = intake.parse_fields(body)
        self.assertIn("uptime monitor", fields["summary"])

    def test_duplicate_heading_first_wins(self):
        body = form_body() + "\n### What's the quest idea?\n\nspoofed second value\n"
        fields = intake.parse_fields(body)
        self.assertNotIn("spoofed", fields["summary"])

    def test_duplicate_heading_never_fills_an_empty_field(self):
        body = form_body(**{"What's the quest idea?": "_No response_"}) + \
            "\n### What's the quest idea?\n\nspoofed into the empty slot\n"
        fields = intake.parse_fields(body)
        self.assertEqual(fields["summary"], "")

    def test_unknown_headings_ignored(self):
        body = "### Mystery field\n\nnoise\n\n" + form_body()
        fields = intake.parse_fields(body)
        self.assertIn("uptime monitor", fields["summary"])

    def test_multiline_values_preserved(self):
        fields = intake.parse_fields(form_body())
        self.assertEqual(len(fields["objectives"].splitlines()), 3)

    def test_user_written_heading_stays_in_field(self):
        body = form_body(**{"What's the quest idea?": (
            "A quest with structure:\n### Phase one\nset up the repo\n"
            "### Phase two\nship it — plenty of detail either way."
        )})
        fields = intake.parse_fields(body)
        self.assertIn("Phase two", fields["summary"])
        self.assertIn("operational reflex", fields["why"])  # later fields intact

    def test_heading_inside_code_fence_ignored(self):
        body = form_body(**{"What's the quest idea?": (
            "Render this snippet:\n```\n### Why does it matter?\nnot a heading\n```\ndone."
        )})
        fields = intake.parse_fields(body)
        self.assertIn("not a heading", fields["summary"])
        self.assertIn("operational reflex", fields["why"])

    def test_crlf_body_parses(self):
        fields = intake.parse_fields(form_body().replace("\n", "\r\n"))
        self.assertIn("uptime monitor", fields["summary"])
        self.assertEqual(fields["existing"], "")


class TestNormalization(unittest.TestCase):
    def test_level_must_be_binary(self):
        self.assertEqual(intake._valid_level("0110"), "0110")
        self.assertEqual(intake._valid_level("Level 1010 please"), "1010")
        self.assertEqual(intake._valid_level("Not sure yet"), "")
        self.assertEqual(intake._valid_level("0123"), "")

    def test_path_controlled_vocabulary(self):
        self.assertEqual(intake._valid_path("devops"), "devops")
        self.assertEqual(intake._valid_path("  Security "), "security")
        self.assertEqual(intake._valid_path("wizardry"), "")

    def test_difficulty_keyword(self):
        self.assertEqual(intake._valid_difficulty("🟡 Medium"), "medium")
        self.assertEqual(intake._valid_difficulty("⚔️ Epic"), "epic")
        self.assertEqual(intake._valid_difficulty("Not sure"), "")

    def test_objective_lines_strip_markers(self):
        lines = intake._objective_lines("- [ ] one\n2. two\n* three\n\n")
        self.assertEqual(lines, ["one", "two", "three"])


class TestRubric(unittest.TestCase):
    def test_complete_idea_is_ready(self):
        manifest = intake.collect(form_body(), NO_NETWORK)
        self.assertEqual(manifest["verdict"], "ready")
        self.assertGreaterEqual(manifest["readiness"]["score"], intake.READY_THRESHOLD)

    def test_thin_idea_needs_detail(self):
        body = form_body(**{
            "What's the quest idea?": (
                "A quest where learners set up a small static website and publish it "
                "so they can share notes with their study group online."
            ),
            "Learning objectives": "_No response_",
            "Tools & technologies": "_No response_",
            "Character path (skill focus)": "Not sure",
        })
        manifest = intake.collect(body, NO_NETWORK)
        self.assertEqual(manifest["verdict"], "needs_detail")
        self.assertLess(manifest["readiness"]["score"], intake.READY_THRESHOLD)

    def test_score_never_exceeds_max(self):
        manifest = intake.collect(form_body(), NO_NETWORK)
        self.assertLessEqual(manifest["readiness"]["score"], manifest["readiness"]["max_score"])
        self.assertEqual(manifest["readiness"]["max_score"], 100)

    def test_specificity_from_code_span(self):
        rubric = intake.score({"summary": "x" * 80 + " uses `kubectl get pods`",
                               "why": "", "objectives": "", "technologies": ""})
        earned = {c["id"]: c["earned"] for c in rubric["checks"]}
        self.assertEqual(earned["specificity"], 10)

    def test_specificity_from_known_tech(self):
        rubric = intake.score(
            {"summary": "Learners deploy with docker and kubernetes." + " x" * 40,
             "why": "", "objectives": "", "technologies": ""},
            known_techs={"docker", "kubernetes"},
        )
        earned = {c["id"]: c["earned"] for c in rubric["checks"]}
        self.assertEqual(earned["specificity"], 10)

    def test_specificity_matches_hyphenated_tech(self):
        rubric = intake.score(
            {"summary": "Automate the deploy with github-actions on every push." + " x" * 30,
             "why": "", "objectives": "", "technologies": ""},
            known_techs={"github-actions"},
        )
        earned = {c["id"]: c["earned"] for c in rubric["checks"]}
        self.assertEqual(earned["specificity"], 10)


class TestSpamSignals(unittest.TestCase):
    def test_too_short(self):
        manifest = intake.collect(form_body(**{
            "What's the quest idea?": "do stuff",
            "Why does it matter?": "_No response_",
            "Learning objectives": "_No response_",
        }), NO_NETWORK)
        self.assertTrue(manifest["flags"]["too_short"])
        self.assertEqual(manifest["verdict"], "spam_suspect")

    def test_link_spam(self):
        links = " ".join(f"https://spam.example/{i}" for i in range(6))
        manifest = intake.collect(form_body(**{"What's the quest idea?": "great deals " + links}), NO_NETWORK)
        self.assertTrue(manifest["flags"]["link_spam"])
        self.assertEqual(manifest["verdict"], "spam_suspect")

    def test_shouting(self):
        manifest = intake.collect(form_body(**{
            "What's the quest idea?": "BUY NOW " * 20,
            "Why does it matter?": "_No response_",
            "Learning objectives": "_No response_",
        }), NO_NETWORK)
        self.assertTrue(manifest["flags"]["shouting"])

    def test_low_diversity_mash(self):
        manifest = intake.collect(form_body(**{
            "What's the quest idea?": "ababab " * 20,
            "Why does it matter?": "_No response_",
            "Learning objectives": "_No response_",
        }), NO_NETWORK)
        self.assertTrue(manifest["flags"]["low_diversity"])

    def test_clean_idea_has_no_flags(self):
        manifest = intake.collect(form_body(), NO_NETWORK)
        self.assertFalse(any(manifest["flags"].values()), manifest["flags"])


class TestDuplicateRadar(unittest.TestCase):
    def _network(self):
        return [
            {"id": "/quests/0101/uptime-monitor/", "title": "Build a Self-Healing Uptime Monitor",
             "level": "0101", "type": "main_quest", "technology": "github-actions",
             "file": "pages/_quests/0101/uptime-monitor.md"},
            {"id": "/quests/0000/hello-terminal/", "title": "Hello Terminal: First Steps",
             "level": "0000", "type": "main_quest", "technology": "bash",
             "file": "pages/_quests/0000/hello-terminal.md"},
        ]

    def test_near_duplicate_found(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump({"nodes": self._network()}, fh)
            path = Path(fh.name)
        try:
            body = "# Self-healing uptime monitor quest\n\n" + form_body()
            manifest = intake.collect(body, path)
            self.assertTrue(manifest["duplicates"], "expected a duplicate hit")
            self.assertEqual(manifest["duplicates"][0]["permalink"], "/quests/0101/uptime-monitor/")
        finally:
            path.unlink()

    def test_unrelated_titles_do_not_match(self):
        dupes = intake.find_duplicates("Paint watercolor landscapes", "art and brushes",
                                       self._network())
        self.assertEqual(dupes, [])

    def test_missing_network_degrades(self):
        manifest = intake.collect(form_body(), NO_NETWORK)
        self.assertEqual(manifest["duplicates"], [])
        self.assertEqual(manifest["stats"]["network_nodes"], 0)

    def test_malformed_network_shapes_degrade(self):
        for payload in ('[]', '"nodes"', '{"nodes": "oops"}', '{"nodes": [1, {"title": "ok"}]}'):
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
                fh.write(payload)
                path = Path(fh.name)
            try:
                nodes = intake.load_network(path)
                self.assertIsInstance(nodes, list, payload)
                self.assertTrue(all(isinstance(n, dict) for n in nodes), payload)
            finally:
                path.unlink()


class TestIssueTitle(unittest.TestCase):
    def test_issue_title_wins_and_prefix_stripped(self):
        manifest = intake.collect(form_body(), NO_NETWORK,
                                  issue_title="Quest idea: Self-Healing Uptime Monitor")
        self.assertEqual(manifest["title"], "Self-Healing Uptime Monitor")

    def test_h1_fallback_without_issue_title(self):
        body = "# My H1 Title\n\n" + form_body()
        manifest = intake.collect(body, NO_NETWORK)
        self.assertEqual(manifest["title"], "My H1 Title")

    def test_h1_inside_fence_not_title(self):
        body = form_body(**{"What's the quest idea?": (
            "Start from:\n```\n# not a title\n```\n" + "a real description of the quest " * 4
        )})
        manifest = intake.collect(body, NO_NETWORK)
        self.assertNotEqual(manifest["title"], "not a title")


class TestSelftest(unittest.TestCase):
    def test_embedded_selftest_passes(self):
        self.assertEqual(intake._selftest(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
