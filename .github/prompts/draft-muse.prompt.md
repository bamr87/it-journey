---
mode: agent
description: "Draft a short-form IT-Journey devops-news muse: opinion-forward, brand-voiced, hook-take-link, surfaced on the /news/ magazine landing"
date: 2026-06-21T00:00:00.000Z
lastmod: 2026-06-21T00:00:00.000Z
---

# Draft Muse

Generate a short-form **muse** — an opinion/news take, not a tutorial. Muses live
in `pages/_posts/devops/`, are written in the `muse-opinion` voice, and surface on
the `/news/` magazine landing. Frontmatter complies with
[`posts.instructions.md`](../instructions/posts.instructions.md) and
[`brand.instructions.md`](../instructions/brand.instructions.md).

## Intake (PLAN)

Ask only what's missing:

- **Topic** (1-line) — what happened / what you're reacting to.
- **The take** — your actual opinion in one sentence. (A muse without a take is
  just news; insist on one.)
- **One source/link** — the thing you're pointing at.

## Operating Protocol (DO)

1. **Load brand voice.** Invoke the `brand-voice` skill with
   `section_guide: devops-news-muse` (profile `muse-opinion`). Pull the values'
   `writing_implication`s and `_data/brand/sections/devops-news-muse.md`.

2. **Generate frontmatter:**

```yaml
---
title: "<≤60-char title that hints at the take>"
description: "<120–160 char SEO summary that states the angle>"
date: <today ISO with ms>
lastmod: <today ISO with ms>
author: bamr87
categories: [DevOps]
tags: [<2–5 tags>]
section_guide: devops-news-muse
excerpt: "<one-sentence hook>"
draft: true
# featured: true   # uncomment to surface in the magazine header
# breaking: true    # uncomment for time-sensitive news
---
```

3. **Generate the muse body** (~150–700 words) in this shape:

```markdown
## <hook line — lead with the tension or the result>

<1–2 sentences that state the take outright. Don't bury it.>

<2–4 sentences of evidence: the command, the metric, the thing that happened.
Be honest about what broke (DFF).>

<One link out — the source. Not ten.>

> From zer0 to her0: <one line tying it back to the reader's own journey.>
```

## Quality checklist (CHECK)

- [ ] The take is stated in the first two sentences.
- [ ] Word count ~150–700 (short form — don't let it become a tutorial).
- [ ] No discouraged terms (comprehensive/powerful/seamless/cutting-edge/…);
      canonical spellings (GitHub, CI/CD, VS Code).
- [ ] Exactly one primary link out.
- [ ] `section_guide: devops-news-muse`, `categories: [DevOps]`.
- [ ] Frontmatter passes validation (title ≤60, description 120–160, lists).
- [ ] `draft: true` on first generation.

## Output Format

Return:

```markdown
## Muse Created

**File:** `pages/_posts/devops/<YYYY-MM-DD-slug>.md` (preview below — not written)
**Voice profile:** muse-opinion   **Word count:** N

---
<full file content>
---

**Next:** Refine the take → `/brand-audit` to confirm voice → `/commit-publish`.
```

Do **not** write the file to disk unless the user confirms.

## Hard Rules

- A muse must carry an opinion — never produce a neutral news summary.
- Never set `draft: false` on first generation.
- Never pad to length; a tight 200-word muse beats a baggy 800-word one.

---

**Related:** [`draft-article.prompt.md`](draft-article.prompt.md) · [`brand-audit.prompt.md`](brand-audit.prompt.md) · brand store at `_data/brand/`.
