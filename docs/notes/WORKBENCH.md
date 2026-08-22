# Notes Workbench — the design

## The problem this fixes

`/notes/` was a folder of files with a scratchpad in front of it. `pages/_notes/index.md` was 309 lines of PowerShell dumps, Liquid scraps, MathJax samples, and cat photos, and nothing in the repository ever iterated `site.notes` — the 27 real notes were reachable only through the theme's auto-generated sidebar. A reader could read a cheatsheet. They could not keep anything.

The workbench turns that page into a place to work. It holds two tiers of notes side by side, plus the snippets a reader captures while moving around the rest of the site.

## The contract

Three kinds of thing live on a reader's board, sharing one id space so the arrangement is a single flat list that never branches on type:

```js
// localStorage, key: itj.notes.workbench
{
  v: 1,
  notes: { "n_<id>": { id, title, body, tags:[], color, created, updated } },
  clips: { "c_<id>": { id, kind:"code"|"text", text, lang, heading,
                       sourceUrl, sourceTitle, sourceCollection, created } },
  pins:  { "p_<id>": { id, url, title, collection, description, added } },
  board: { order: ["n_…","c_…","p_…"], sizes: { id:[cols,rows] }, collapsed: { id:bool } },
  prefs: { density, sort, showLibrary, lastOpenNoteId }
}
```

**Public notes are not in here.** Those are the markdown files in `pages/_notes/`, authored in the repository, rendered by Jekyll, identical for everyone. A pin only points at one. That split is the whole model: the repository owns what is public, the browser owns what is personal, and neither can quietly become the other.

`window.ITJNotes` is the only way to touch that blob. `assets/js/notes-store.js` owns it and exposes `get, addNote, addClip, addPin, update, remove, reorder, setOrder, setSize, setCollapsed, setPref, reset, exportJson, importJson, subscribe`. Writes are debounced 300ms, every access is wrapped against private-mode browsers that throw, a `storage` listener keeps two open tabs in agreement, and a quota guard warns before the roughly 5MB ceiling instead of letting a save fail silently.

## What it does for each audience

**A reader** gets a board. Write a note in Markdown with live preview; clip a code block from the quest they are following and it arrives with a link back to the exact heading; pin a cheatsheet they keep reopening. Cards drag into any arrangement and stay there. Everything is exportable as JSON, because clearing browser data clears the board with it — the page says so plainly rather than pretending to be storage it is not.

**Someone with JavaScript off**, and every crawler, still gets a complete index of the collection. `_includes/notes/library-static.html` renders every public note grouped by folder at build time; the app hydrates those rows rather than replacing them. This is the first thing to check when changing the page: `/notes/` with scripts disabled must still list all 27 notes.

**A contributor** gets a path from a local note to a public one. The editor's Propose button builds a full front-matter block inside the constraint bands CI enforces — title 30-60 characters, description 120-160, ISO-8601 dates with milliseconds — and hands it to GitHub's prefilled new-file editor. Past roughly 7.5KB of encoded content the URL stops working, so the note goes to the clipboard with the editor opened alongside.

## How it is wired

| File | Role |
|---|---|
| `assets/js/notes-store.js` | The schema and all persistence. Loaded on every page. |
| `assets/js/notes-clipper.js` | Clip buttons, selection popover, note-page toolbar. Every page but the workbench. |
| `assets/js/notes-markdown.js` | Escape-first Markdown renderer for local notes. |
| `assets/js/notes-workbench.js` | Library, board, editor, search, publish. `/notes/` only. |
| `_includes/custom/head.html` | Page identity as meta tags, so the clipper needs no Liquid. |
| `_includes/custom/body-end.html` | Site-wide load of the store and clipper. |
| `_includes/notes/workbench.html` | The three-region shell. |
| `_includes/notes/library-static.html` | Every public note, rendered by Liquid at build time. |
| `_layouts/notes-workbench.html` | Mounts the shell and its assets. |

`_includes/custom/head.html` and `custom/body-end.html` are the theme's own extension points — `bamr87/zer0-mistakes` includes both as empty stubs from `_layouts/root.html` and `_includes/core/head.html`. Filling them in is how this repository adds site-wide markup without forking a theme file.

Two data sources already existed and both are reused rather than duplicated: `/search.json` backs the "search the site to pin a page" box, and `/assets/data/wiki-index.json` resolves `[[Wiki Links]]` in local notes. Neither is fetched until it is needed, and both degrade to a working board if they 404.

## Design notes

**Escape first, then transform.** `notes-markdown.js` HTML-escapes the entire source before any rule runs, so every later transform operates on text that can no longer contain a tag, and the only markup in the output is markup the renderer wrote. A note containing `<script>` renders as the visible characters. This is why there is a hand-written renderer here instead of a library plus a sanitizer: there is no filter to keep ahead of. The one place a URL reaches an attribute allows `http(s)` and site-relative targets only.

**Keyboard parity is not optional.** HTML5 drag-and-drop never fires for a keyboard user, so every card's grip is a real button with a grab mode: Enter picks the card up, arrows move it, Enter drops it, Escape puts it back, and each move is announced through an `aria-live` region. The pointer path follows `assets/js/home-os.js` — handle-only `dragstart`, CSS `order`, state array as the source of truth.

**Guard every theme hook.** The remote theme is unpinned (`remote_theme: bamr87/zer0-mistakes`, no version), so `.code-block-header`, `#main-content`, the `custom/*` stubs, and `_layouts/note.html` can all change underneath. Every injection point is looked up defensively and skipped when absent: a theme change costs a feature, never a page.

**The theme builds its code-block headers in the browser, not at build time.** The clipper watches for them with a `MutationObserver` rather than assuming script order, and `decorateHeaders()` marks each block's `<pre>` as claimed so the late bare-`<pre>` fallback cannot double-add a button. Inferring that relationship from DOM depth was tried first and was wrong — the wrapper nesting is exactly the thing a theme update changes.

**The page is a tool, so it is laid out like one.** `hide_intro: true` drops the theme's hero, metadata block, and reading-time estimate the way `/home/` does, and on screens under 40rem the explainer moves below the board with CSS `order` — the DOM keeps the prose first for crawlers and for anyone reading with styles off.

**The site's own stylesheet styles buttons broadly.** A `.button, button:not(.copy)` rule hands every other button a 20px-padded outline, exempting the theme's copy button by name. The clip button's rules are scoped to the header so they outrank it and it can sit beside Copy as a matched sibling.

## Rollout status

Shipped in one pull request on `claude/notes-interactive-workbench-y3l8uj`. Everything is client-side and additive: no workflow, script, Makefile, or plugin changes.

Verified with a Jekyll CI-parity build, `frontmatter-validator.py` (0 errors), `brand_lint.py`, `make prose-oneline`, `make liquid-check`, `make mermaid-check`, a 34-assertion store harness, a 50-assertion renderer harness covering XSS and scheme allowlisting, and a 46-assertion browser run against the built site — creation, persistence across reloads, pinning, filtering, site search, keyboard reordering, resize and collapse, export, clipping from a quest page, and the JavaScript-disabled path.

Known limits worth revisiting: the board is per-browser with no sync; the renderer covers a Markdown subset rather than full kramdown; and `[[Wiki Links]]` match on exact title, basename, slug, or a title whose subtitle follows a colon, so an inventive alias will not resolve and offers to create a local note instead.
