#!/usr/bin/env python3
"""Tests for the repository chronicle, against a synthetic Git repository.

No network, no model: the AI layer is exercised through a fake provider.
Run: python3 scripts/digs/chronicle/test_chronicle.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import ai  # noqa: E402
import content  # noqa: E402
import frames  # noqa: E402
import present  # noqa: E402
from core import Ledger  # noqa: E402
from ingest import ingest  # noqa: E402
from replay import mainline_order, timeline, tree_at  # noqa: E402

QUIET = lambda *a, **k: None  # noqa: E731


def sh(repo: Path, *args: str, date: str = "2021-01-04T10:00:00+00:00") -> str:
    env = {**os.environ, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date,
           "GIT_AUTHOR_NAME": "Ada", "GIT_AUTHOR_EMAIL": "ada@example.com",
           "GIT_COMMITTER_NAME": "Ada", "GIT_COMMITTER_EMAIL": "ada@example.com"}
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True,
                          env=env).stdout


def write(repo: Path, path: str, text: str | bytes) -> None:
    p = repo / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text if isinstance(text, bytes) else text.encode())


def commit(repo: Path, msg: str, date: str) -> None:
    sh(repo, "add", "-A", date=date)
    sh(repo, "commit", "-q", "-m", msg, date=date)


def make_repo(root: Path) -> Path:
    repo = root / "demo"
    repo.mkdir()
    sh(repo, "init", "-q", "-b", "main")
    write(repo, "README.md", "# demo\n\nA small repo.\n")
    commit(repo, "Initial commit", "2021-01-04T10:00:00+00:00")
    write(repo, "_config.yml", "title: Demo Site\nurl: https://demo.example\n")
    write(repo, "index.md", "---\ntitle: Home\npermalink: /\n---\n# Welcome\n\nHello {{ site.title }}.\n")
    write(repo, "docs/guide.md", "# Guide\n" + "line\n" * 20)
    commit(repo, "feat: add site and guide", "2021-01-12T10:00:00+00:00")
    write(repo, "assets/logo.png", bytes(range(256)) * 4)
    write(repo, "docs/guide.md", "# Guide\n" + "line\n" * 25)
    commit(repo, "add logo, grow guide", "2021-02-02T10:00:00+00:00")
    sh(repo, "checkout", "-q", "-b", "side")
    write(repo, "src/app.py", "print('hi')\n" * 3)
    commit(repo, "feat(app): add app", "2021-02-10T10:00:00+00:00")
    sh(repo, "checkout", "-q", "main")
    write(repo, "README.md", "# demo\n\nA small repo, now with docs.\n")
    commit(repo, "docs: readme", "2021-02-11T10:00:00+00:00")
    sh(repo, "merge", "-q", "--no-ff", "-m", "Merge branch 'side'", "side", date="2021-02-12T10:00:00+00:00")
    (repo / "pages").mkdir()
    sh(repo, "mv", "docs/guide.md", "pages/guide.md", date="2021-03-01T10:00:00+00:00")
    write(repo, "pages/guide.md", "# Guide\n" + "line\n" * 25 + "more\n")
    commit(repo, "refactor: move guide to pages", "2021-03-01T10:00:00+00:00")
    os.remove(repo / "index.md")
    write(repo, "index.html", "---\ntitle: Home\npermalink: /\n---\n<h1>New home</h1>\n<p>Fresh.</p>\n")
    commit(repo, "replace the home page", "2021-04-05T10:00:00+00:00")
    write(repo, "src/app.py", "print('hello')\n")
    commit(repo, "fix: app greeting", "2021-04-06T10:00:00+00:00")
    return repo


class FakeProvider(ai.Provider):
    name = "fake"
    model = "fake-model"

    def __init__(self, answer):
        self.answer = answer
        self.calls = 0

    def available(self):
        return True

    def complete(self, system, prompt):
        self.calls += 1
        return self.answer(prompt), {"cost_usd": 0.01, "model": self.model}


class ChronicleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name)
        cls.repo = make_repo(root)
        cls.ledger_root = root / "ledgers"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def fresh(self, name: str) -> Ledger:
        return Ledger(self.ledger_root / name, "local/demo")

    def test_ingest_is_idempotent_and_complete(self):
        led = self.fresh("ingest")
        first = ingest(self.repo, led, "main", log=QUIET)
        self.assertEqual(first["added"], 9)
        before = {p.name: p.read_text() for p in led.commits_dir.glob("*.jsonl")}
        man = led.manifest_path.read_text()
        second = ingest(self.repo, led, "main", log=QUIET)
        self.assertEqual(second["added"], 0)
        self.assertEqual(before, {p.name: p.read_text() for p in led.commits_dir.glob("*.jsonl")})
        self.assertEqual(man, led.manifest_path.read_text(), "a no-op run must not touch the manifest")
        rows = led.commits()
        merge = next(r for r in rows.values() if r["subject"].startswith("Merge"))
        self.assertEqual(len(merge["parents"]), 2)
        self.assertTrue(merge["mainline"])
        self.assertEqual([f["p"] for f in merge["files"]], ["src/app.py"], "merge diffs against its first parent")
        side = next(r for r in rows.values() if r["subject"] == "feat(app): add app")
        self.assertFalse(side["mainline"])
        self.assertEqual(side["facts"]["conventional"], {"type": "feat", "scope": "app"})
        moved = next(r for r in rows.values() if r["subject"].startswith("refactor"))
        rename = moved["files"][0]
        self.assertEqual((rename["s"], rename["o"], rename["p"]), ("R", "docs/guide.md", "pages/guide.md"))
        logo = next(f for r in rows.values() for f in r["files"] if f["p"] == "assets/logo.png")
        self.assertIsNone(logo["a"])
        self.assertEqual(logo["b"], 1024)

    def test_new_commits_are_read_once(self):
        led = self.fresh("incremental")
        ingest(self.repo, led, "HEAD~2", log=QUIET)
        self.assertEqual(len(led.commits()), 7)
        res = ingest(self.repo, led, "main", log=QUIET)
        self.assertEqual(res["added"], 2)

    def test_replay_matches_git(self):
        led = self.fresh("replay")
        ingest(self.repo, led, "main", log=QUIET)
        head = led.manifest()["head"]
        state = tree_at(led.commits(), head)
        real = {}
        for line in sh(self.repo, "ls-tree", "-r", "-l", head).splitlines():
            meta, path = line.split("\t", 1)
            real[path] = int(meta.split()[3])
        self.assertEqual(set(state), set(real))
        for path, size in real.items():
            self.assertEqual(state[path][1], size, path)
        self.assertEqual(state["pages/guide.md"][0], 27)
        self.assertEqual(state["src/app.py"][0], 1)
        tl = timeline(led.commits(), head)
        self.assertEqual(tl["frames"][-1]["files"], len(real))
        self.assertEqual(len(mainline_order(led.commits(), head)), 8)

    def test_heuristic_annotation_without_a_model(self):
        led = self.fresh("heuristic")
        ingest(self.repo, led, "main", log=QUIET)
        res = ai.annotate_commits(led, ai.Provider(), log=QUIET)
        self.assertEqual(res["annotated"], 9)
        kinds = {a["summary"]: a["kind"] for a in led.annotations().values()}
        self.assertEqual(kinds["app greeting"], "fix")
        self.assertEqual(kinds["Merge branch 'side'"], "merge")
        self.assertTrue(all(a["model"] == "heuristic" for a in led.annotations().values()))

    def test_model_annotation_is_cached_and_upgrades_heuristic(self):
        led = self.fresh("model")
        ingest(self.repo, led, "main", log=QUIET)
        ai.annotate_commits(led, ai.Provider(), log=QUIET)

        def answer(prompt):
            ids = [line[4:].strip() for line in prompt.splitlines() if line.startswith("id: ")]
            # drop one id and garble one kind: both must fall back, not crash
            out = [{"id": i, "kind": "feature", "area": "x", "summary": f"did {i}", "significance": 2}
                   for i in ids[1:]]
            out[0]["kind"] = "not-a-kind"
            return "```json\n" + json.dumps(out) + "\n```"
        fake = FakeProvider(answer)
        ai.annotate_commits(led, fake, batch=40, workers=1, log=QUIET)
        ann = led.annotations()
        self.assertEqual(len(ann), 9)
        by_model = {}
        for a in ann.values():
            by_model[a["model"]] = by_model.get(a["model"], 0) + 1
        self.assertEqual(by_model.get("fake-model"), 7)
        calls = fake.calls
        ai.annotate_commits(led, FakeProvider(lambda p: "[]"), log=QUIET)
        self.assertEqual(len(led.annotations()), 9)
        again = FakeProvider(answer)
        ai.annotate_commits(led, again, workers=1, log=QUIET)
        self.assertGreater(calls, 0)
        self.assertLessEqual(again.calls, 2, "only commits still on the heuristic reading are asked again")

    def test_eras_are_validated_and_cached(self):
        led = self.fresh("eras")
        ingest(self.repo, led, "main", log=QUIET)
        ai.annotate_commits(led, ai.Provider(), log=QUIET)
        real = sorted(led.commits())[0][:12]
        doc = {"headline": "Demo grows", "summary": "s",
               "eras": [{"title": "Later", "start": "2021-03", "end": "2021-04", "summary": "b",
                         "key_commits": [real, "deadbeef0000"]},
                        {"title": "Start", "start": "2021-01", "end": "2021-01", "summary": "a",
                         "learnings": [{"lesson": "Decide the layout early.", "evidence": [real, "nope"]}]}],
               "learnings": [{"lesson": "x", "evidence": ["zzz"]}],
               "transitions": [{"when": "2021-03", "from": "docs", "to": "pages", "evidence": [real]}]}
        fake = FakeProvider(lambda p: "Here you go:\n" + json.dumps(doc))
        out = ai.read_eras(led, fake, log=QUIET)
        self.assertEqual([e["title"] for e in out["eras"]], ["Start", "Later"])
        self.assertEqual(out["eras"][0]["end"], "2021-02", "eras are made contiguous")
        self.assertEqual(out["eras"][-1]["end"], "2021-04")
        self.assertEqual(out["eras"][1]["key_commits"], [real], "unknown commit ids are dropped")
        self.assertEqual(out["eras"][0]["learnings"][0]["evidence"], [real])
        self.assertEqual(out["learnings"][0]["evidence"], [])
        ai.read_eras(led, fake, log=QUIET)
        self.assertEqual(fake.calls, 1, "an unchanged digest reuses the filed reading")
        fallback = ai.read_eras(self.fresh_with_commits("eras2"), ai.Provider(), log=QUIET)
        self.assertEqual(fallback["source"], "heuristic")
        self.assertEqual(fallback["eras"][0]["start"], "2021-01")

    def fresh_with_commits(self, name):
        led = self.fresh(name)
        ingest(self.repo, led, "main", log=QUIET)
        return led

    def test_pages_follow_renames_and_home_lineage(self):
        led = self.fresh_with_commits("frames")
        commits = led.commits()
        head = led.manifest()["head"]
        chosen = frames.choose_pages(self.repo, commits, head, 4)
        home = chosen[0]
        self.assertEqual(home["path"], "index.html")
        self.assertEqual([p for _, p in home["versions"]], ["README.md", "index.md", "index.html"],
                         "the home page is followed back through the files that served /")
        guide = next(c for c in chosen if c["path"] == "pages/guide.md")
        self.assertEqual([p for _, p in guide["versions"]], ["docs/guide.md", "docs/guide.md", "pages/guide.md"])

    def test_render_reduces_liquid_and_resolves_assets(self):
        led = self.fresh_with_commits("render")
        commits = led.commits()
        sha = next(s for s, r in commits.items() if r["subject"] == "add logo, grow guide")
        with tempfile.TemporaryDirectory() as tmp:
            r = frames.Renderer(self.repo, Path(tmp))
            slot = r.render(sha, "index.md", "2021-02-02", Path(tmp) / "home" / "f.html")
            page = slot.with_suffix(".page.html").read_text()
            self.assertIn("Hello Demo Site.", page)
            self.assertIn("<h1>Welcome</h1>", page)
            self.assertIn("2021-02-02", slot.read_text())
            out = frames.liquid('<a href="{{ \'/quests/\' | relative_url }}">Go</a> {% include x.html %} {{ y }}',
                                {"baseurl": "/b"}, {})
            self.assertIn('href="/b/quests/"', out)
            self.assertIn("⟨include x.html⟩", out)
            self.assertIn("⟨y⟩", out)

    def test_collections_and_front_matter(self):
        cases = {"pages/_quests/0001/x.md": "quests", "_posts/2020-01-01-a.md": "posts", "index.md": "pages",
                 "docs/guide.md": "docs/", "pages/search.md": "pages", "_includes/head.html": None,
                 ".github/instructions/a.md": None, "CHANGELOG.md": None, "scripts/README.md": None,
                 "assets/a.html": None, "pages/_quests/img.png": None}
        for path, want in cases.items():
            self.assertEqual(content.collection_of(path), want, path)
        v = content.parse_version('---\ntitle: "Rocket \\ud83d\\ude80 launch"\ntags: git, bash\n'
                                  "level: '0101'\nquest_type: main_quest\ndraft: true\n---\nSome words here.\n")
        self.assertEqual(v["t"], "Rocket \U0001F680 launch")
        self.assertEqual(v["tags"], ["git", "bash"])
        self.assertEqual((v["lvl"], v["qt"], v["draft"], v["w"]), ("0101", "main_quest", True, 3))
        self.assertEqual(content.parse_version("# Plain heading\nbody")["t"], "Plain heading")

    def test_articles_keep_identity_and_file_topics_once(self):
        led = self.fresh_with_commits("content")
        res = content.read_versions(self.repo, led, log=QUIET)
        self.assertEqual(res["versions"], 7)
        self.assertEqual(content.read_versions(self.repo, led, log=QUIET)["added"], 0)
        arts = content.articles(led.commits(), led.versions(), led.manifest()["head"])
        by_path = {a["path"]: a for a in arts}
        self.assertEqual(sorted(by_path), ["README.md", "index.html", "pages/guide.md"])
        self.assertTrue(all(a["died"] is None for a in arts))
        self.assertEqual(by_path["pages/guide.md"]["first"], "docs/guide.md", "a detected rename keeps identity")
        self.assertEqual(by_path["index.html"]["first"], "index.md", "a delete and add with one title is a move")
        self.assertEqual(by_path["index.html"]["t"], "Home")

        tax_answer = {"topics": [{"key": k, "name": k.title(), "description": "d"}
                                 for k in ("guides", "home", "meta", "code")]}
        tax = content.taxonomy(led, arts, FakeProvider(lambda p: json.dumps(tax_answer)), log=QUIET)
        self.assertEqual([t["key"] for t in tax["topics"]], ["guides", "home", "meta", "code", "other"])

        def answer(prompt):
            ids = [line[4:] for line in prompt.splitlines() if line.startswith("id: ")]
            return json.dumps([{"id": i, "topic": "guides" if n == 0 else "nonsense"} for n, i in enumerate(ids)])
        fake = FakeProvider(answer)
        content.classify(led, arts, tax, fake, workers=1, log=QUIET)
        got = led.article_topics()
        self.assertEqual(len(got), 3)
        self.assertEqual(sorted(r["model"] for r in got.values()), ["fake-model", "heuristic", "heuristic"])
        again = FakeProvider(answer)
        content.classify(led, arts, tax, again, workers=1, log=QUIET)
        self.assertEqual(again.calls, 1, "only the two heuristic readings are asked again")
        self.assertEqual(content.taxonomy(led, arts, FakeProvider(lambda p: "{}"), log=QUIET)["hash"], tax["hash"],
                         "a filed taxonomy is kept")

    def test_presentation_assembles(self):
        led = self.fresh_with_commits("present")
        ai.annotate_commits(led, ai.Provider(), log=QUIET)
        ai.read_eras(led, ai.Provider(), log=QUIET)
        content.read_versions(self.repo, led, log=QUIET)
        arts = content.articles(led.commits(), led.versions(), led.manifest()["head"])
        content.classify(led, arts, content.taxonomy(led, arts, ai.Provider(), log=QUIET), ai.Provider(), log=QUIET)
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp)
            frames.render_frames(self.repo, led, cache, pages=2, per_page=3, shoot=False, log=QUIET)
            index = present.build(led, cache, cache / "out")
            data = json.loads((cache / "out" / "data.json").read_text())
            self.assertTrue(index.read_text().startswith("<!doctype html>"))
            self.assertFalse((cache / "out" / "page.html").read_text().lstrip().startswith("<!doctype"))
        self.assertEqual(data["stats"]["commits"], 9)
        self.assertEqual(data["stats"]["filesNow"], 6)
        self.assertEqual(data["stats"]["actors"], [9, 0, 0, 0])
        self.assertIn("Jekyll site config", [m["label"] for m in data["milestones"]])
        self.assertEqual(len(data["cadence"]), 14)
        self.assertEqual(len(data["pages"]), 2)
        lib = data["library"]
        self.assertEqual(len(lib["articles"]), 3)
        self.assertEqual(lib["source"]["taxonomy"], "heuristic")
        self.assertTrue(all(row[4] == -1 for row in lib["articles"]), "every article is still live")


if __name__ == "__main__":
    unittest.main(verbosity=2)
