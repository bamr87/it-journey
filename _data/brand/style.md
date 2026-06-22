# IT-Journey — Prose & Formatting Style

> The single home for prose/formatting rules. `.github/instructions/posts.instructions.md`
> §7 points here instead of restating these (DRY). The structural post rules
> (frontmatter, filenames, permalinks, CI gates) stay in `posts.instructions.md`;
> this file governs *how the prose reads and is formatted*.

## Voice mechanics

- **Imperative** in instructions: "Run `bundle exec jekyll serve`", not "You can
  run…".
- **Past tense** in chronicles: "The model suggested…", "The build failed…".
- **Second person** for the reader ("you"); never "the user" inside prose.

## Structure

- **One H1**, auto-generated from `title`. Start the body at `##`.
- Don't pad. Skip sections that don't apply rather than filling them.
- Lead each section with its point; put detail after.

## Formatting

- **Every code block has a language tag** (```bash, ```python, ```yaml). No bare
  fences.
- **Nested fences** use a longer outer fence (4 backticks if the inner uses 3).
- **Cross-references are markdown links**, never inline code: write
  [the Docker quest](/quests/...), not `/quests/...`.
- **Tables** for comparisons and option matrices; **lists** for steps.
- **Diagrams:** Mermaid for flows (set `mermaid: true` in frontmatter); PNG/SVG
  under `assets/images/posts/<slug>/`.

## Emoji

- Allowed as occasional **section markers** and in the magazine/muse framing.
- Not decorative spam, and never inside body sentences in a `concept-essay`.
- Per-section emoji budgets are enforced by the CMS engine — see
  `.cms/config.yml > brand` (`emoji_intensity`).

## Words to cut

Empty hype (flagged by the engine; see [`glossary.yml`](glossary.yml) →
`discouraged`): **comprehensive, powerful, seamless, cutting-edge, revolutionary,
game-changing, effortless.** Trim a long description by removing words, never with
an ellipsis. Canonical spellings (GitHub, JavaScript, CI/CD, VS Code, Node.js,
Docker Compose) live in `glossary.yml` and are enforced.

## Safety

- Never commit literal secret prefixes (`ghp_`, `sk-`, `AKIA`, …). Use
  `${env:NAME}` / `${input:name}` placeholders.
- Don't link from `pages/_docs/` to `../../docs/...` (excluded from the build) —
  use a full GitHub URL.
