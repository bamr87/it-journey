"""The front-end time-lapse: a repository's key pages, version by version.

Pages are chosen from the ledger, not by hand: the home page (``permalink: /``,
else a root ``index.*``, else the README), the README, and the most-revised
content pages. Each page is followed back through its renames, and its
versions on the mainline are sampled into frames.

Each frame is rendered from that commit's own source: the page's Markdown or
HTML, its front matter, the site title and navigation from that commit's
``_config.yml`` and ``_data/navigation``, its stylesheets and images. Liquid is
reduced to labelled placeholders. The result is a *simulated* front end: what
the source said at that moment, drawn in a neutral shell, not a replay of the
historical build (no theme gem or remote theme is resolved). Playwright takes
the screenshots with network access blocked, so a frame never depends on
what a URL serves today.
"""
from __future__ import annotations

import html
import json
import posixpath
import re
import subprocess
from pathlib import Path

from core import Ledger, git, now_iso
from replay import mainline_order, tree_at

RENDERER = "source-render/v1"
PAGE_EXT = (".md", ".markdown", ".html", ".htm")
SKIP_PREFIX = ("_includes/", "_layouts/", "_sass/", "_site/", "node_modules/", ".github/", "test/", "tests/",
               "spec/", "vendor/", "_data/", ".cache/", "templates/", "src/")
SKIP_NAMES = {"changelog.md", "license.md", "schema.md", "agents.md", "claude.md", "contributing.md",
              "code_of_conduct.md", "security.md", "pull_request_template.md"}
IMG_CAP = 2_500_000
VIEW_W, VIEW_H = 1280, 860


# ------------------------------------------------------------- page choice
def _candidate(path: str) -> bool:
    low = path.lower()
    if not low.endswith(PAGE_EXT) or low.startswith(SKIP_PREFIX):
        return False
    name = low.rsplit("/", 1)[-1]
    if name in SKIP_NAMES or "/_includes/" in low or "/_layouts/" in low or "/node_modules/" in low:
        return False
    return not any(seg.startswith(".") for seg in low.split("/")[:-1])


def page_history(chain: list[dict], path: str) -> list[tuple[dict, str]]:
    """Mainline versions of ``path`` (oldest first), following renames back."""
    out, cur = [], path
    for row in reversed(chain):
        hit = next((f for f in row["files"] if f["p"] == cur), None)
        if hit is None:
            continue
        if hit["s"] == "D":
            break
        changed = hit["s"] in "ARC" or (hit.get("a") or 0) + (hit.get("d") or 0) > 0 or hit.get("a") is None
        if changed:
            out.append((row, cur))
        if hit["s"] == "R" and hit.get("o"):
            cur = hit["o"]
        elif hit["s"] == "A":
            break
    out.reverse()
    return out


def _home(repo: Path, head: str, state: dict) -> str | None:
    pages = [p for p in state if _candidate(p) or p.lower() in ("readme.md", "index.md", "index.html")]
    for p in sorted(pages, key=lambda p: (p.count("/"), p)):
        if p.count("/") > 2:
            continue
        try:
            text = git(repo, "show", f"{head}:{p}").decode("utf-8", "replace")[:3000]
        except RuntimeError:
            continue
        if re.search(r"^permalink:\s*['\"]?/['\"]?\s*$", text, re.M):
            return p
    for p in ("index.html", "index.md", "README.md", "readme.md"):
        if p in state:
            return p
    return None


def choose_pages(repo: Path, commits: dict, head: str, n: int) -> list[dict]:
    chain = mainline_order(commits, head)
    state = tree_at(commits, head)
    chosen: list[dict] = []
    home = _home(repo, head, state)
    if home:
        chosen.append({"path": home, "role": "home page"})
    readme = next((p for p in ("README.md", "readme.md", "README.markdown") if p in state), None)
    if readme and readme != home:
        chosen.append({"path": readme, "role": "repository front door"})
    counts: dict[str, int] = {}
    for row in chain:
        for f in row["files"]:
            if f["s"] != "D" and f["p"] in state and _candidate(f["p"]):
                counts[f["p"]] = counts.get(f["p"], 0) + 1
    used_dirs = {posixpath.dirname(c["path"]) for c in chosen}
    for p in sorted(counts, key=lambda p: (-counts[p], p)):
        if len(chosen) >= n:
            break
        d = posixpath.dirname(p)
        if any(c["path"] == p for c in chosen) or (d in used_dirs and len(counts) > n * 3):
            continue
        if state[p][0] < 15:  # a stub is not a page worth watching
            continue
        chosen.append({"path": p, "role": f"most-revised page ({counts[p]} mainline changes)"})
        used_dirs.add(d)
    for c in chosen:
        c["versions"] = page_history(chain, c["path"])
        if c["role"] == "home page":
            c["versions"] = home_lineage(repo, commits, chain, c["versions"])
            paths = []
            for _, p in c["versions"]:
                if p not in paths:
                    paths.append(p)
            if len(paths) > 1:
                c["role"] = "home page (served by " + " → ".join(paths) + ")"
    return [c for c in chosen if c["versions"]][:n]


def home_lineage(repo: Path, commits: dict, chain: list[dict], versions: list, depth: int = 6) -> list:
    """Prepend the pages that served the home page before the current one was born."""
    index = {row["sha"]: i for i, row in enumerate(chain)}
    for _ in range(depth):
        if not versions:
            return versions
        first_row, first_path = versions[0]
        i = index.get(first_row["sha"], 0)
        if i == 0:
            return versions
        before = chain[i - 1]
        state = tree_at(commits, before["sha"])
        prev = _home(repo, before["sha"], state)
        if not prev:
            return versions
        older = [(r, p) for r, p in page_history(chain[:i], prev)]
        if not older:
            return versions
        versions = older + versions
    return versions


def sample(items: list, k: int) -> list:
    if len(items) <= k:
        return list(items)
    idx = sorted({round(i * (len(items) - 1) / (k - 1)) for i in range(k)})
    return [items[i] for i in idx]


# ------------------------------------------------------------- rendering
def _yaml(text: str) -> dict:
    try:
        import yaml
        doc = yaml.safe_load(text)
        return doc if isinstance(doc, dict) else {}
    except Exception:
        out = {}
        for m in re.finditer(r"^([A-Za-z_][\w-]*):\s*['\"]?([^'\"\n#&*][^'\"\n#]*?)['\"]?\s*$", text, re.M):
            out.setdefault(m.group(1), m.group(2))
        return out


def split_front_matter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return {}, text
    return _yaml(m.group(1)), text[m.end():]


def _show(repo: Path, sha: str, path: str, binary: bool = False):
    try:
        out = git(repo, "show", f"{sha}:{path}")
    except RuntimeError:
        return None
    return out if binary else out.decode("utf-8", "replace")


def _lookup(ctx: dict, dotted: str):
    cur = ctx
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur if isinstance(cur, (str, int, float)) else None


def liquid(text: str, site: dict, page: dict) -> str:
    """Reduce Liquid to its static parts and labelled placeholders."""
    raws: list[str] = []

    def keep(m):
        raws.append(m.group(1))
        return f"\x00RAW{len(raws) - 1}\x00"
    text = re.sub(r"{%-?\s*raw\s*-?%}(.*?){%-?\s*endraw\s*-?%}", keep, text, flags=re.S)
    text = re.sub(r"{%-?\s*comment\s*-?%}.*?{%-?\s*endcomment\s*-?%}", "", text, flags=re.S)
    text = re.sub(r"{%-?\s*include\s+([\w./-]+)[^%]*-?%}",
                  lambda m: f'<div class="lq-include">⟨include {html.escape(m.group(1))}⟩</div>', text)

    baseurl = str(site.get("baseurl") or "").rstrip("/")

    def value(expr: str) -> str | None:
        head, _, filters = expr.partition("|")
        head = head.strip()
        lit = re.match(r"^(['\"])(.*)\1$", head)
        if lit:
            out = lit.group(2)
            if "relative_url" in filters or "absolute_url" in filters:
                out = baseurl + out
            return out
        for scope, ctx in (("site.", site), ("page.", page)):
            if head.startswith(scope):
                val = _lookup(ctx, head[len(scope):])
                if val is not None:
                    return str(val)
        return None

    def in_tag(m):  # inside an HTML tag: a literal value, never markup
        return re.sub(r"{{-?\s*(.*?)\s*-?}}", lambda v: html.escape(value(v.group(1)) or "", quote=True),
                      m.group(0), flags=re.S)
    text = re.sub(r"<[a-zA-Z][^<>]*?{{.*?}}[^<>]*?>", in_tag, text, flags=re.S)

    def var(m):
        val = value(m.group(1))
        if val is not None:
            return html.escape(val)
        return '<span class="lq-var">⟨' + html.escape(m.group(1).split("|")[0].strip()[:40]) + '⟩</span>'
    text = re.sub(r"{{-?\s*(.*?)\s*-?}}", var, text, flags=re.S)
    text = re.sub(r"{%.*?%}", "", text, flags=re.S)
    text = re.sub(r"^\s*\{:[^}\n]*\}\s*$", "", text, flags=re.M)  # kramdown attribute lists
    text = re.sub(r"\{:\s*[.#:][^}\n]*\}", "", text)
    return re.sub(r"\x00RAW(\d+)\x00", lambda m: html.escape(raws[int(m.group(1))]), text)


def markdown_html(text: str) -> str:
    try:
        import markdown
        return markdown.markdown(text, extensions=["extra", "sane_lists"], output_format="html")
    except ImportError:
        return _mini_markdown(text)


def _inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)[^)]*\)", r'<img alt="\1" src="\2">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)[^)]*\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"(?<![*\w])\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)


def _mini_markdown(text: str) -> str:
    """A small Markdown subset, used only when Python-Markdown is not installed."""
    out, para, in_code, lst = [], [], False, None

    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>" + _inline(" ".join(para)) + "</p>")
            para = []
        if lst:
            out.append(f"</{lst}>")
            lst = None
    for line in text.splitlines():
        if line.strip().startswith("```"):
            flush()
            out.append("</code></pre>" if in_code else "<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            out.append(html.escape(line))
            continue
        if line.lstrip().startswith("<"):
            flush()
            out.append(line)
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            flush()
            out.append(f"<h{len(m.group(1))}>{_inline(m.group(2))}</h{len(m.group(1))}>")
            continue
        m = re.match(r"^\s*([-*+]|\d+\.)\s+(.*)", line)
        if m:
            tag = "ol" if m.group(1)[0].isdigit() else "ul"
            if para:
                out.append("<p>" + _inline(" ".join(para)) + "</p>")
                para = []
            if lst != tag:
                if lst:
                    out.append(f"</{lst}>")
                out.append(f"<{tag}>")
                lst = tag
            out.append(f"<li>{_inline(m.group(2))}</li>")
            continue
        if not line.strip():
            flush()
            continue
        if line.startswith(">"):
            flush()
            out.append(f"<blockquote>{_inline(line.lstrip('> '))}</blockquote>")
            continue
        para.append(line.strip())
    flush()
    return "\n".join(out)


BASE_CSS = """
*{box-sizing:border-box}html,body{margin:0}body{font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
color:#1d2330;background:#fff}.site-head{display:flex;align-items:center;gap:24px;padding:14px 32px;
border-bottom:1px solid #e3e6ee;background:#f8f9fc}.site-title{font-weight:700;font-size:18px;color:#1d2330;
white-space:nowrap}.site-nav{display:flex;gap:18px;flex-wrap:wrap;font-size:14px}.site-nav a{color:#3d4a6b;
text-decoration:none}.page{max-width:900px;margin:0 auto;padding:28px 32px 60px}.page h1{font-size:2.1em;
line-height:1.2;margin:.2em 0 .5em}.page h2{margin-top:1.6em;border-bottom:1px solid #eceef4;padding-bottom:.2em}
.page img{max-width:100%;height:auto}.page pre{background:#f4f5f9;padding:12px 14px;overflow:auto;border-radius:6px;
font-size:13px}.page code{font-size:.9em;background:#f4f5f9;padding:.1em .3em;border-radius:4px}.page table{
border-collapse:collapse}.page td,.page th{border:1px solid #e3e6ee;padding:4px 8px}.page blockquote{margin:1em 0;
padding:.2em 1em;border-left:4px solid #d7dbe8;color:#55607a}.lq-include{border:1px dashed #b8bfd3;color:#7a849e;
font:12px ui-monospace,monospace;padding:6px 10px;margin:8px 0;border-radius:6px;background:#fafbfe}
.lq-var{color:#8b93ab;font:12px ui-monospace,monospace;background:#f1f3f8;border-radius:4px;padding:0 4px}
img[data-missing]{display:inline-block;min-width:60px;min-height:20px;border:1px dashed #c6cbe0;
color:#8b93ab;font:11px ui-monospace,monospace;padding:2px 6px;border-radius:4px;vertical-align:middle}
"""

CHROME = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;background:#dfe3ec;font:13px system-ui,-apple-system,"Segoe UI",sans-serif}
.win{width:%(w)dpx;height:%(h)dpx;display:flex;flex-direction:column;background:#fff;overflow:hidden}
.bar{display:flex;align-items:center;gap:10px;height:42px;padding:0 14px;background:#eef0f5;border-bottom:1px solid #d5d9e3}
.dots{display:flex;gap:6px}.dots i{width:11px;height:11px;border-radius:50%%;background:#c9cdd8;display:block}
.url{flex:1;background:#fff;border:1px solid #d5d9e3;border-radius:999px;padding:5px 14px;color:#4a5570;
white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.stamp{font:12px ui-monospace,monospace;color:#5b6684}
iframe{border:0;flex:1;width:100%%}</style></head><body><div class="win"><div class="bar"><div class="dots"><i></i><i></i><i></i></div>
<div class="url">%(url)s</div><div class="stamp">%(stamp)s</div></div><iframe src="%(page)s"></iframe></div></body></html>"""


class Renderer:
    def __init__(self, repo: Path, out: Path):
        self.repo, self.out = repo, out
        self.assets = out / "assets"
        self.assets.mkdir(parents=True, exist_ok=True)
        self._site: dict[str, tuple] = {}

    def site(self, sha: str) -> tuple[dict, list]:
        if sha not in self._site:
            cfg = _yaml(_show(self.repo, sha, "_config.yml") or "")
            nav_src = _show(self.repo, sha, "_data/navigation/main.yml") or _show(self.repo, sha, "_data/navigation.yml")
            nav = []
            if nav_src:
                try:
                    import yaml
                    doc = yaml.safe_load(nav_src)
                    if isinstance(doc, dict):
                        doc = doc.get("main") or next((v for v in doc.values() if isinstance(v, list)), [])
                    nav = [str(i.get("title")) for i in doc or [] if isinstance(i, dict) and i.get("title")][:9]
                except Exception:
                    nav = []
            self._site[sha] = (cfg, nav)
        return self._site[sha]

    def _asset(self, sha: str, path: str) -> str | None:
        try:
            entry = git(self.repo, "ls-tree", "-l", sha, "--", path).decode().split("\t")[0].split()
        except RuntimeError:
            return None
        if len(entry) != 4 or entry[1] != "blob" or not entry[3].isdigit():
            return None
        blob, size = entry[2], int(entry[3])
        if size > IMG_CAP:
            return None
        ext = posixpath.splitext(path)[1].lower() or ".bin"
        name = f"{blob[:16]}{ext}"
        dest = self.assets / name
        if not dest.exists():
            dest.write_bytes(git(self.repo, "cat-file", "blob", blob))
        return f"../assets/{name}"

    def _resolve(self, sha: str, page_path: str, src: str, baseurl: str) -> str | None:
        src = src.strip().split("#")[0].split("?")[0]
        if not src or re.match(r"^(https?:|data:|//|mailto:)", src):
            return None
        if baseurl and src.startswith(baseurl + "/"):
            src = src[len(baseurl):]
        path = src.lstrip("/") if src.startswith("/") else posixpath.normpath(
            posixpath.join(posixpath.dirname(page_path), src))
        return self._asset(sha, path)

    def render(self, sha: str, path: str, date: str, slot: Path) -> Path:
        text = _show(self.repo, sha, path) or ""
        fm, body = split_front_matter(text)
        cfg, nav = self.site(sha)
        site = {**cfg}
        page = {**fm}
        body = liquid(body, site, page)
        is_html = path.lower().endswith((".html", ".htm"))
        content = body if is_html else markdown_html(body)
        baseurl = str(cfg.get("baseurl") or "").rstrip("/")

        def img(m):
            new = self._resolve(sha, path, html.unescape(m.group(2)), baseurl)
            if new:
                return f'{m.group(1)}"{new}"'
            return f'{m.group(1)}"data:," data-missing="1"'
        content = re.sub(r'(<img\b[^>]*?\bsrc=)["\']([^"\']+)["\']', img, content, flags=re.I)

        def css(m):
            new = self._resolve(sha, path, html.unescape(m.group(1)), baseurl)
            return f'<link rel="stylesheet" href="{new}">' if new and new.endswith(".css") else ""
        content = re.sub(r'<link\b[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\'][^>]*>', css, content,
                         flags=re.I)
        content = re.sub(r'<script\b[^>]*\bsrc=[^>]*>\s*</script>', "", content, flags=re.I)
        title = str(fm.get("title") or cfg.get("title") or path)
        site_title = str(cfg.get("title") or self.repo.name)
        nav_html = "".join(f"<a>{html.escape(n)}</a>" for n in nav)
        full = "<html" in content[:2000].lower()
        if full:
            doc = content
        else:
            doc = (f'<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>'
                   f"<style>{BASE_CSS}</style></head><body><header class=\"site-head\"><span class=\"site-title\">"
                   f"{html.escape(site_title)}</span><nav class=\"site-nav\">{nav_html}</nav></header>"
                   f"<main class=\"page\">{'' if is_html or re.search(r'^#\s', body, re.M) else f'<h1>{html.escape(title)}</h1>'}"
                   f"{content}</main></body></html>")
        slot.parent.mkdir(parents=True, exist_ok=True)
        page_file = slot.with_suffix(".page.html")
        page_file.write_text(doc, encoding="utf-8")
        url = str(cfg.get("url") or "").rstrip("/") + baseurl + "/" + str(fm.get("permalink") or path).lstrip("/")
        slot.write_text(CHROME % {"w": VIEW_W, "h": VIEW_H, "url": html.escape(url), "page": page_file.name,
                                  "stamp": f"{date} · {sha[:7]}"}, encoding="utf-8")
        return slot


def _key(path: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", path).strip("-").lower()[:60] or "page"


def render_frames(repo: Path, ledger: Ledger, cache: Path, pages: int = 4, per_page: int = 18,
                  shoot: bool = True, log=print) -> dict:
    commits = ledger.commits()
    head = ledger.manifest()["head"]
    chosen = choose_pages(repo, commits, head, pages)
    work = cache / "frames"
    renderer = Renderer(repo, work)
    index = {"schema": "chronicle-frames/v1", "renderer": RENDERER, "head": head, "pages": []}
    jobs = []
    for c in chosen:
        key = _key(c["path"])
        versions = c["versions"]
        picked = sample(versions, per_page)
        frames = []
        for row, path_then in picked:
            stem = f"{row['ct'][:10]}-{row['sha'][:10]}"
            slot = work / key / f"{stem}.html"
            img = work / key / f"{stem}.webp"
            if not img.exists():
                renderer.render(row["sha"], path_then, row["ct"][:10], slot)
                jobs.append({"html": str(slot), "out": str(img)})
            frames.append({"sha": row["sha"], "date": row["ct"][:10], "path": path_then,
                           "image": f"{key}/{stem}.webp"})
        index["pages"].append({"key": key, "path": c["path"], "role": c["role"], "versions": len(versions),
                               "frames": frames})
        log(f"[frames] {c['path']}: {len(versions)} versions, {len(frames)} frames")
    if shoot and jobs:
        screenshot(jobs, log)
    ledger.write_doc("frames.json", {**index, "at": now_iso()} if jobs or not ledger.read_doc("frames.json")
                     else ledger.read_doc("frames.json") | index)
    return {"pages": len(index["pages"]), "rendered": len(jobs)}


def screenshot(jobs: list[dict], log=print) -> None:
    """Screenshot each chrome page with Playwright (network blocked), then save as WebP."""
    script = Path(__file__).with_name("shot.mjs")
    manifest = Path(jobs[0]["out"]).parent.parent / "shot-jobs.json"
    for j in jobs:
        j["png"] = str(Path(j["out"]).with_suffix(".png"))
    manifest.write_text(json.dumps({"width": VIEW_W, "height": VIEW_H, "jobs": jobs}), encoding="utf-8")
    res = subprocess.run(["node", str(script), str(manifest)], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"screenshots failed: {res.stderr[-800:]}")
    from PIL import Image
    for j in jobs:
        png = Path(j["png"])
        if png.exists():
            im = Image.open(png).convert("RGB")
            im = im.resize((960, round(im.height * 960 / im.width)), Image.LANCZOS)
            im.save(j["out"], "WEBP", quality=64, method=6)
            png.unlink()
    log(f"[frames] {len(jobs)} screenshots")
