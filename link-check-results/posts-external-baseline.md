# Posts External Link Status — Phase 4 Baseline (auto-generated)

This document records known broken or flaky **external** links in `pages/_posts/`
after the Phase 4 link-repair pass. **Internal links: 282/282 OK** when validated
against the built `_site/` (run `lychee --offline --base "$PWD/_site"`).

External link rot is an ongoing maintenance burden — these entries are
acknowledged and tracked, not necessarily considered actionable in the cleanup
PR.

## Validation command

```bash
lychee --no-progress --format json --base "$PWD/_site" \
  --max-concurrency 10 --timeout 15 --max-retries 1 \
  --accept '200..=299,403' \
  pages/_posts/**/*.md
```

## Known broken / flaky external links (post-Phase 4)

| File | URL | Status | Notes |
|------|-----|--------|-------|
| devops/2025-11-17-deploying-jekyll-sites-to-azure-cloud.md | https://jekyllrb.com/docs/deployment/methods/ | ✅ FIXED | Replaced with `/docs/deployment/` (Jekyll site reorganized) |
| devops/2025-11-17-deploying-jekyll-sites-to-azure-cloud.md | https://azure.microsoft.com/products/devops/ | Timeout | Intermittent — Microsoft host slow under bot UA |
| devops/2025-11-17-deploying-jekyll-sites-to-azure-cloud.md | https://azure.microsoft.com/products/devops/pipelines/ | Timeout | Same as above |
| devops/2026-03-07-foundational-ci-cd-pipelines-github-vscode-extensions.md | https://dev.azure.com/ | Timeout | Intermittent |
| learning/2021-11-08-it-purpose-manifesto.md | https://www.gnu.org/gnu/manifesto.en.html | 429 | Rate-limited; URL is valid in browsers |
| system-administration/2025-10-13-el-capitan-bootable-installer-apple-silicon.md | https://archive.org/details/macosinstallers | 404 | Item removed from archive.org |
| web-development/2025-11-15-github-pages-hidden-gem.md | https://www.youtube.com/watch?v=2MsN8gpT6jY | 404 | Video removed by uploader |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | http://www.ezfolk.com/library/ | 404 | Site offline |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | https://libraries.indiana.edu/cook | 404 | URL restructured |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | http://www.gutenberg.org/wiki/Gutenberg:The_Sheet_Music_Project | 404 | Project page removed |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | http://www.sheetmusicarchive.net/index.cfm | 404 | Site offline |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | http://memory.loc.gov/ammem/smhtml/smhome.html | Timeout | Library of Congress URL deprecated |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | http://www.ccel.org/cceh/ | 404 | URL changed |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | http://www.bpl.org/research/music/aboutmusic.htm | 404 | Site reorganized |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | http://www.leeds.ac.uk/music/Info/RRTuneBk/ | 404 | Site reorganized |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | http://www.cpdl.org/wiki/index.php/Main_Page | 500 | Server error; valid wiki at cpdl.org |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | http://memory.loc.gov/ammem/collections/sheetmusic/brown/ | Timeout | LOC URL deprecated |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | http://www.pdinfo.com/Public-Domain-Music-List.php | 404 | Page removed |
| creative-experimental/2025-07-03-music-resources-free-sheet-music.md | http://www.sims.berkeley.edu/~mkduggan/neh.html | Network error | Berkeley faculty page removed |

## Recommended follow-ups (post-merge, not blocking)

1. **`creative-experimental/2025-07-03-music-resources-free-sheet-music.md`**:
   12 of 19 broken links live in this single "list of resources" post that is
   heavily decayed. Recommended action: prepend an editor's note linking to a
   Wayback Machine snapshot, OR mark the post as archived/historical, OR
   replace each URL with its `https://web.archive.org/web/*/<url>` mirror.

2. **Azure timeouts**: Consider switching to canonical short URLs
   (`https://azure.microsoft.com/en-us/products/devops/`) which sometimes
   respond faster under automated probes.

3. **Other dead links**: One-by-one review against current vendor docs
   (jekyllrb.com URLs change with releases; YouTube videos disappear).

## Reports

- Current full report: `work/posts-cleanup/reports/lychee-online.json`
- Internal-only baseline (clean): `work/posts-cleanup/reports/lychee-offline-base.json`
- Phase 4 commit: see git log on branch `chore/posts-mass-cleanup`
