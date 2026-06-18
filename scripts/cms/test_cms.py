#!/usr/bin/env python3
"""
test_cms.py — unit + integration tests for the IT-Journey CMS engine and the
read-only safety guard in the frontmatter normalizer.

Run:  python3 scripts/cms/test_cms.py            (or: python3 -m unittest ...)
Exits non-zero on any failure (suitable for CI).

These tests pin the behaviours an adversarial review flagged: out-of-range date
handling, recursive-glob path-boundary correctness, keyword counting across
shapes, lane classification, and the vendored/read-only skip in the normalizer.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _load(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / relpath)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod                      # needed for dataclass annotations
    spec.loader.exec_module(mod)
    return mod


cms = _load("cms", "scripts/cms/cms.py")
nf = _load("normalize_fm", "scripts/content/normalize-frontmatter.py")
CFG = cms.load_config()


class TestDateParsing(unittest.TestCase):
    def test_out_of_range_returns_none_not_crash(self):
        for bad in ("2024-13-45", "2024-02-30", "2024-00-00", '"2024-13-45"'):
            self.assertIsNone(cms.to_dt(bad), f"{bad!r} should be None")

    def test_iso_with_ms(self):
        dt = cms.to_dt("2020-07-30T10:19:45.000Z")
        self.assertEqual((dt.year, dt.month, dt.day, dt.hour, dt.minute), (2020, 7, 30, 10, 19))
        self.assertIsNotNone(dt.tzinfo)

    def test_nanosecond_precision_keeps_time(self):
        dt = cms.to_dt("2024-01-15T10:30:00.123456789Z")
        self.assertEqual((dt.year, dt.hour, dt.minute), (2024, 10, 30))

    def test_date_only_and_none(self):
        self.assertEqual(cms.to_dt("2024-01-15").day, 15)
        self.assertIsNone(cms.to_dt(None))


class TestGlobMatching(unittest.TestCase):
    def test_recursive_readme_respects_boundaries(self):
        g = ["**/README.md"]
        self.assertTrue(cms.glob_match("README.md", g))
        self.assertTrue(cms.glob_match("pages/x/README.md", g))
        self.assertFalse(cms.glob_match("pages/MYREADME.md", g))   # the bug fix
        self.assertFalse(cms.glob_match("pages/foo-README.md", g))

    def test_wargames_nested(self):
        self.assertTrue(cms.glob_match("pages/_docs/wargames/a/b.md",
                                       ["pages/_docs/wargames/**"]))

    def test_middle_doublestar(self):
        g = ["a/**/b.md"]
        self.assertTrue(cms.glob_match("a/b.md", g))
        self.assertTrue(cms.glob_match("a/x/y/b.md", g))
        self.assertFalse(cms.glob_match("a/xb.md", g))


class TestKeywordCount(unittest.TestCase):
    def test_shapes(self):
        self.assertEqual(cms._keyword_count(["a", "b", "c"]), 3)
        self.assertEqual(cms._keyword_count({}), 0)                # empty dict bug
        self.assertEqual(cms._keyword_count({"primary": ["a", "b"]}), 2)
        self.assertEqual(cms._keyword_count({"primary": "a", "secondary": "b"}), 2)
        self.assertEqual(cms._keyword_count("a, b, c"), 3)
        self.assertEqual(cms._keyword_count(None), 0)


class TestClassificationAndScore(unittest.TestCase):
    def test_coerce_draft(self):
        self.assertIs(cms._coerce_draft(True), True)
        self.assertIs(cms._coerce_draft("published"), False)
        self.assertIs(cms._coerce_draft("draft"), True)
        self.assertIs(cms._coerce_draft("in progress"), True)
        self.assertIsNone(cms._coerce_draft(None))

    def test_freshness_buckets(self):
        self.assertEqual(cms._freshness_bucket(10, CFG), "fresh")
        self.assertEqual(cms._freshness_bucket(120, CFG), "aging")
        self.assertEqual(cms._freshness_bucket(300, CFG), "stale")
        self.assertEqual(cms._freshness_bucket(1000, CFG), "critical")

    def test_collection_for_longest_prefix(self):
        self.assertEqual(cms.collection_for("pages/_posts/devops/x.md", CFG)[0], "posts")
        self.assertEqual(cms.collection_for("pages/_quests/0000/x.md", CFG)[0], "quests")
        self.assertEqual(cms.collection_for("pages/home.md", CFG)[0], "pages")

    def test_playable_quest(self):
        self.assertTrue(cms._is_playable_quest({"quest_type": "main_quest"}))
        self.assertTrue(cms._is_playable_quest({"level": "0000"}))
        self.assertFalse(cms._is_playable_quest({"title": "hub"}))


class TestSchema(unittest.TestCase):
    def test_schema_has_all_collections_with_base_required(self):
        sch = cms.build_schema(CFG)
        self.assertEqual(len(sch["collections"]), len(CFG["collections"]))
        for name, c in sch["collections"].items():
            for fld in CFG["required_base"]:
                self.assertIn(fld, c["required"], f"{name} missing base required {fld}")


class TestParseFileResilience(unittest.TestCase):
    def test_malformed_date_does_not_raise(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.md"
            p.write_text('---\ntitle: X\ndate: 2024-13-45\n---\nbody\n', encoding="utf-8")
            fm, body, err = cms.parse_file(p)   # must not raise
            self.assertIsNone(fm)
            self.assertIsNotNone(err)


class TestNormalizerReadOnlyGuard(unittest.TestCase):
    def _process(self, text: str, rel: str):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
            return nf.process_file(p, root, apply=False, touch_lastmod=False)

    def test_vendored_source_repo_skipped(self):
        r = self._process(
            '---\ntitle: V\nsource_repo: https://github.com/x/y\n'
            'description: short\ndraft: published\n---\nProse\n',
            "pages/_docs/wargames/t/v.md")
        self.assertIsNotNone(r.skipped_reason)
        self.assertIn("read-only", r.skipped_reason)
        self.assertFalse(r.changed_fields)

    def test_vendored_source_url_skipped(self):
        r = self._process(
            '---\ntitle: V\nsource_url: https://x/y\ncategories: foo\n---\nProse\n',
            "pages/_docs/x.md")
        self.assertIsNotNone(r.skipped_reason)

    def test_normal_post_is_processed(self):
        r = self._process(
            '---\ntitle: Normal\ncategories: devops\n---\nbody\n',
            "pages/_posts/n.md")
        self.assertIsNone(r.skipped_reason)
        self.assertTrue(r.changed_fields)   # string categories -> list


class TestEngineIntegration(unittest.TestCase):
    """Smoke-test the real scan over the repo."""
    def test_full_index_runs_and_is_sane(self):
        now = datetime.now(timezone.utc)
        records = cms.build_index(CFG, now)
        self.assertGreater(len(records), 400)
        summary = cms.summarize(records, now)
        for key in ("total_files", "actionable_files", "avg_health_actionable",
                    "by_collection", "health_buckets"):
            self.assertIn(key, summary)
        # health never out of range
        for r in records:
            self.assertTrue(r.health == -1 or 0 <= r.health <= 100,
                            f"{r.path} health {r.health} out of range")
        # vendored wargames are all read-only
        wm = [r for r in records if "/wargames/" in r.path]
        self.assertTrue(wm, "expected wargames files in index")
        self.assertTrue(all(r.read_only for r in wm),
                        "all wargames files must be read_only")


if __name__ == "__main__":
    unittest.main(verbosity=2)
