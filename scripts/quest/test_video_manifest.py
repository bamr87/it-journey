#!/usr/bin/env python3
"""Unit tests for video_manifest.py (the deterministic quest-video arm).

Run:  python3 scripts/quest/test_video_manifest.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import video_manifest as vm  # noqa: E402

try:
    import yaml  # noqa: F401
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False


QUEST_MD = """---
title: 'Terminal Mastery: Conquering the Command-Line Realm'
description: Master terminal navigation in this hands-on quest
date: '2025-07-28T23:34:51.000Z'
lastmod: '2025-09-27T19:59:13.000Z'
level: '0001'
difficulty: 🟢 Easy
permalink: /quests/0001/terminal-mastery/
---

# Quest body

One paragraph on one line.
"""


class TestTitle(unittest.TestCase):
    def test_short_title_gets_full_suffix(self):
        t = vm.compose_title("Terminal Mastery", "0001")
        self.assertEqual(t, "Terminal Mastery — IT-Journey Quest Walkthrough (Level 0001)")
        self.assertLessEqual(len(t), vm.TITLE_MAX)

    def test_long_title_truncates_under_limit(self):
        t = vm.compose_title("Q" * 140, "0001")
        self.assertLessEqual(len(t), vm.TITLE_MAX)
        self.assertIn("IT-Journey", t)

    def test_angle_brackets_stripped(self):
        self.assertNotIn("<", vm.compose_title("a <b> c", "0001"))


class TestChapters(unittest.TestCase):
    def test_first_chapter_forced_to_zero_and_gap_enforced(self):
        lines = vm.compose_chapters([
            {"start": 0.4, "label": "Intro"},
            {"start": 5.0, "label": "too close"},
            {"start": 14.0, "label": "$ ls"},
            {"start": 30.0, "label": "Verdict"},
        ])
        self.assertEqual(lines, ["00:00 Intro", "00:14 $ ls", "00:30 Verdict"])

    def test_too_few_chapters_omitted(self):
        self.assertEqual(vm.compose_chapters([{"start": 0, "label": "Intro"}]), [])

    def test_hour_format(self):
        self.assertEqual(vm._mmss(3725), "1:02:05")
        self.assertEqual(vm._mmss(65), "01:05")


class TestDescription(unittest.TestCase):
    def _video(self):
        return {
            "quest": {"title": "Terminal Mastery", "permalink": "/quests/0001/terminal-mastery/",
                      "level": "0001", "difficulty": "🟢 Easy"},
            "evidence": {"overall": 91.5, "verdict": "pass"},
            "chapters": [{"start": 0, "label": "Intro"}, {"start": 15, "label": "$ ls"},
                         {"start": 40, "label": "Verdict & next steps"}],
        }

    def test_contains_quest_url_and_provenance(self):
        meta = {"character": {"name": "Developer"}, "level": {"code": "0001", "theme": "Web"},
                "base_url": "https://it-journey.dev"}
        d = vm.compose_description(self._video(), meta, "https://example.com/run/1", "2026-08-19")
        self.assertIn("https://it-journey.dev/quests/0001/terminal-mastery/", d)
        self.assertIn("https://example.com/run/1", d)
        self.assertIn("00:00 Intro", d)
        self.assertNotIn("<", d)
        self.assertLessEqual(len(d), vm.DESC_MAX)

    def test_tags_bounded(self):
        meta = {"character": {"key": "developer"}, "level": {"code": "0001", "theme": "Web Fundamentals"}}
        tags = vm.compose_tags(self._video(), meta)
        self.assertIn("it-journey", tags)
        self.assertLessEqual(sum(len(t) for t in tags), vm.TAGS_MAX_TOTAL)
        self.assertEqual(len(tags), len(set(tags)))


class TestApplyToQuest(unittest.TestCase):
    def test_insert_block_and_bump_lastmod(self):
        out = vm.apply_to_quest(QUEST_MD, "AbC123XyZ_-", "2026-08-19", "https://run/9")
        self.assertIn("walkthrough_video:\n  provider: youtube\n  id: AbC123XyZ_-", out)
        self.assertIn("url: https://www.youtube.com/watch?v=AbC123XyZ_-", out)
        self.assertIn("recorded: '2026-08-19'", out)
        self.assertIn("run_url: https://run/9", out)
        self.assertIn("lastmod: '2026-08-19T00:00:00.000Z'", out)
        self.assertIn("# Quest body", out)
        self.assertEqual(out.count("walkthrough_video:"), 1)

    def test_idempotent_and_replaces_existing(self):
        once = vm.apply_to_quest(QUEST_MD, "AbC123XyZ_-", "2026-08-19", "https://run/9")
        twice = vm.apply_to_quest(once, "AbC123XyZ_-", "2026-08-19", "https://run/9")
        self.assertEqual(once, twice)
        replaced = vm.apply_to_quest(once, "NewId456_-x", "2026-08-20", "https://run/10")
        self.assertNotIn("AbC123XyZ_-", replaced)
        self.assertIn("id: NewId456_-x", replaced)
        self.assertEqual(replaced.count("walkthrough_video:"), 1)

    def test_body_untouched(self):
        out = vm.apply_to_quest(QUEST_MD, "AbC123XyZ_-", "2026-08-19", "")
        self.assertTrue(out.endswith("# Quest body\n\nOne paragraph on one line.\n"))

    def test_no_frontmatter_raises(self):
        with self.assertRaises(ValueError):
            vm.apply_to_quest("no frontmatter here\n", "AbC123XyZ_-", "2026-08-19", "")


@unittest.skipUnless(HAVE_YAML, "pyyaml not installed")
class TestCatalog(unittest.TestCase):
    def test_catalog_roundtrip(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "videos.yml"
            cat = vm.load_catalog(p)
            cat["videos"]["/quests/0001/terminal-mastery/"] = {"id": "AbC123XyZ_-", "recorded": "2026-08-19"}
            vm.save_catalog(p, cat)
            text = p.read_text(encoding="utf-8")
            self.assertIn("videos.yml — the committed quest walkthrough-video catalog", text)
            again = vm.load_catalog(p)
            self.assertEqual(again["videos"]["/quests/0001/terminal-mastery/"]["id"], "AbC123XyZ_-")


if __name__ == "__main__":
    unittest.main(verbosity=2)
