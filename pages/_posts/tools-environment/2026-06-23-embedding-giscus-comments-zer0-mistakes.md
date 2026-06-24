---
title: "Embedding Giscus Comments in the zer0-mistakes Theme"
description: "A screenshot-driven walkthrough of configuring GitHub Giscus comments on giscus.app and wiring the generated snippet into a zer0-mistakes Jekyll site."
date: 2026-06-23T18:00:00.000Z
lastmod: 2026-06-23T18:00:00.000Z
author: bamr87
categories:
- web development
- devops
- jekyll
tags:
- giscus
- github-discussions
- jekyll
- comments
- zer0-mistakes
- github-pages
keywords:
- giscus
- github discussions comments
- jekyll comments
- zer0-mistakes theme
- giscus.app configuration
- github pages comments
excerpt: "Turn GitHub Discussions into a comment system: generate the giscus embed on giscus.app and wire it into IT-Journey's zer0-mistakes theme — including the one-character config bug that was silently disabling it."
permalink: /posts/2026-06-23-embedding-giscus-comments-zer0-mistakes/
section: Tools & Environment
draft: false
---

# Embedding Giscus Comments in the zer0-mistakes Theme

Static sites are fast and cheap to host, but they have no backend — so "just add
comments" turns into a hunt for a third-party service. [Giscus](https://giscus.app/)
solves this by storing every comment thread as a **GitHub Discussion** in your own
repository. No database, no ads, no tracking, and your readers authenticate with
the GitHub account they already have.

This post is a hands-on walkthrough of configuring giscus and embedding it in
IT-Journey, which runs on the [zer0-mistakes](https://github.com/bamr87/zer0-mistakes)
Jekyll theme. Every giscus.app screenshot below was captured live against this
repository (`bamr87/it-journey`) with Playwright, so what you see is the real
configuration this site uses — including two genuine bugs we had to fix to make
comments actually appear: a one-character config typo, and a Liquid tag hiding
inside an HTML comment in the theme's own include.

## How giscus works (the 30-second version)

```text
Reader's browser  ──▶  giscus client.js  ──▶  GitHub Discussions API
   (your page)            (iframe widget)        (your repo's discussions)
```

1. You drop a `<script>` tag on the page where comments should appear.
2. `giscus/client.js` injects an `<iframe>` that renders the widget.
3. The widget maps the current page to a **Discussion** (by URL pathname, in our
   case) and reads/writes comments through the GitHub Discussions API.
4. The first comment on a new page auto-creates its Discussion thread.

Because the data lives in GitHub Discussions, moderation, search, and even
markdown rendering are handled by GitHub. You are essentially skinning
Discussions and dropping it onto your site.

## What the zer0-mistakes theme already does for you

The theme provides a ready-made include, `content/giscus.html`, and pulls it into
the post layout. You don't paste the giscus.app snippet anywhere — the include
already *is* the snippet, with most attributes **hardcoded** and only three
values read from your site config:

```liquid
{% raw %}<script src="https://giscus.app/client.js"
        data-repo="{{ site.repository }}"
        data-repo-id="{{ site.giscus.data-repo-id }}"
        data-category-id="{{ site.giscus.data-category-id }}"
        data-mapping="pathname"
        data-strict="1"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="en"
        crossorigin="anonymous"
        async>
</script>{% endraw %}
```

So the giscus.app generator (which produces the *whole* snippet) is really just
there to hand you **two** values — `data-repo-id` and `data-category-id` — plus
to confirm your repo is wired up correctly. `data-repo` comes from
`site.repository`, and everything else is the theme's opinionated default.
Knowing this up front saves a lot of "why is my `data-theme` being ignored?"
confusion.

In this version of the theme, only the **post** layout embeds giscus:

```liquid
{% raw %}{% if page.comments != false and site.giscus %}
  ...<h2>Comments</h2>...
  {% include content/giscus.html %}
{% endif %}{% endraw %}
```

`_config.yml` assigns `layout: article` to `pages/_posts`, while notes,
notebooks, docs, quests, and the hub/index pages resolve to layouts
(`default.html`, `collection.html`, …) that don't reference giscus. There's a
second gate, too: the guard's `page.comments != false` half. The site's
front-matter defaults set `comments: false` at the root scope, but the
`pages/_posts` scope overrides that with **`comments: true`** — so **every post
shows the widget by default**, and you opt a single post out with
`comments: false`. Everything that isn't a post stays off via the root default.

### A real bug in the shipped include — vendor a corrected copy

Enabling giscus surfaced a genuine theme bug worth understanding, because the
failure mode is bewildering. The theme *does* ship `content/giscus.html`, but its
header documentation comment contains a literal usage example:

```liquid
{% raw %}║ Usage:        {% include giscus.html %} (typically at bottom of posts/pages) ║{% endraw %}
```

The trap: **Liquid evaluates `{% raw %}{% ... %}{% endraw %}` tags even inside HTML comments.**
That "example" is not inert documentation — Jekyll runs it. So the instant the
comment guard passes and the include renders, that nested tag executes, looks for
a top-level `giscus.html` that doesn't exist, and the build aborts:

```text
Liquid Exception: Could not locate the included file 'giscus.html' ... in /_layouts/article.html
```

"Fixing" the example to point at `content/giscus.html` is worse — the file then
includes *itself* and you get the equally cryptic `stack level too deep` (≈9000
recursion levels). The clean fix is to **vendor a corrected copy into the site**:
Jekyll resolves a site's own `_includes/` ahead of any theme, so a tag-free copy
at `_includes/content/giscus.html` overrides the buggy one and the build passes
for every theme delivery path (gem, `remote_theme`, Docker CI). This repo already
overrides theme includes the same way (see `_includes/content/`). Create it with
the snippet shown above — and keep all Liquid tags **out of the comment** (or wrap
them in `{% raw %}…{% endraw %}`).

## Prerequisites

- A **public** GitHub repository (private repos can't show public comments).
- Repository admin rights (to enable Discussions and install an app).
- A Jekyll site on the zer0-mistakes theme (or any theme — the giscus.app steps
  are identical; only the wiring in the last section differs).

## Part 1 — Prepare the GitHub repository

Giscus needs three things to be true about your repo. The giscus.app page lists
them as a checklist, and it validates all three live.

### 1.1 Make the repository public

Comments are public GitHub Discussions, so the repo must be public. (Settings →
General → Danger Zone → *Change repository visibility* if it isn't.)

### 1.2 Enable the Discussions feature

In your repository, go to **Settings → General → Features** and tick
**Discussions**. GitHub's docs cover this here:
[Enabling or disabling GitHub Discussions for a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/enabling-or-disabling-github-discussions-for-a-repository).

Once enabled, the repo gets a **Discussions** tab. IT-Journey's looks like this —
note the category list in the sidebar, which giscus will let you choose from:

![The Discussions tab on bamr87/it-journey, showing the default category list in the sidebar](/assets/images/posts/giscus/09-itjourney-discussions.png)

### 1.3 Pick (or create) a discussion category

Giscus recommends a category of type **Announcements**, because Announcement
categories only allow *maintainers* to open new discussions — which is exactly
what you want when giscus is the only thing creating them. IT-Journey uses the
default **Announcements** category. You can manage categories from the Discussions
tab (the ✏️ pencil next to "Categories").

### 1.4 Install the giscus GitHub App

The widget writes comments on your behalf through the
[giscus GitHub App](https://github.com/apps/giscus). Install it and grant it
access to the repo you'll be embedding (you can scope it to a single repository).

![The giscus GitHub App installation page](/assets/images/posts/giscus/08-giscus-github-app.png)

## Part 2 — Generate the embed on giscus.app

With the repo prepped, head to [giscus.app](https://giscus.app/). The page is
both the documentation *and* the configuration generator — you scroll down a
single form and it builds the snippet as you go.

![The giscus.app configuration page](/assets/images/posts/giscus/01-giscus-app-landing.png)

### 2.1 Connect your repository

Type `owner/repo` into the **repository** field. Giscus immediately calls the
GitHub API to check the three prerequisites from Part 1. When all three pass you
get a green checkmark and **"Success! This repository meets all of the above
criteria."**

![The repository field validated for bamr87/it-journey with a success message, and the Page to Discussions mapping options below](/assets/images/posts/giscus/02-repository-validated.png)

If you see an error instead, it tells you which prerequisite failed — usually
"giscus is not installed on this repository" (revisit step 1.4) or that
Discussions isn't enabled (step 1.2).

### 2.2 Choose the page ↔ discussion mapping

This controls how a page is matched to its Discussion thread. The zer0-mistakes
include is hardcoded to **`pathname`**, so pick **"Discussion title contains page
`pathname`"** to match. Each URL path (e.g. `/posts/.../`) gets its own thread.

![The Page to Discussions Mapping section with pathname selected](/assets/images/posts/giscus/03-page-mapping.png)

The theme also sets `data-strict="1"` (strict title matching), which avoids
GitHub's fuzzy search picking the wrong thread when two paths look similar — so
tick **"Use strict title matching"** if you want the preview snippet to match the
theme exactly.

### 2.3 Choose the discussion category

Select the category you settled on in step 1.3. For IT-Journey that's
**Announcements**, whose category ID giscus fills in as `DIC_kwDOEOrJ7c4CAn8D`.
This is the value you'll copy into your site config.

![The Discussion Category dropdown set to Announcements](/assets/images/posts/giscus/04-category-announcements.png)

### 2.4 Set the features

The zer0-mistakes defaults are: reactions **on**, metadata **off**, and the
comment box **above** the comments (`data-input-position="top"`). Match those if
you want the generated snippet to mirror the theme.

![The Features section with reactions enabled and the comment box placed above the comments](/assets/images/posts/giscus/05-features.png)

### 2.5 Copy the generated snippet

Scroll to **Enable giscus** at the bottom. Giscus has assembled the full
`<script>` tag from your choices:

![The Enable giscus section showing the generated script tag with data-repo-id and data-category-id](/assets/images/posts/giscus/06-enable-giscus-snippet.png)

For `bamr87/it-journey` it produces:

```html
<script src="https://giscus.app/client.js"
        data-repo="bamr87/it-journey"
        data-repo-id="MDEwOlJlcG9zaXRvcnkyODM4MjI1NzM="
        data-category="Announcements"
        data-category-id="DIC_kwDOEOrJ7c4CAn8D"
        data-mapping="pathname"
        data-strict="1"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="en"
        crossorigin="anonymous"
        async>
</script>
```

Compare this to the theme include from earlier — it's almost identical. The one
difference: giscus.app adds a `data-category="Announcements"` line (the
human-readable name), which the theme include omits because it passes only
`data-category-id` — the ID is all the giscus client needs. That's exactly why,
of this whole block, the only two values you have to copy are:

- `data-repo-id` → `MDEwOlJlcG9zaXRvcnkyODM4MjI1NzM=`
- `data-category-id` → `DIC_kwDOEOrJ7c4CAn8D`

> **Note on the trailing `=`.** giscus.app emits the repo ID with base64 padding
> (`…1NzM=`); the value stored in `_config.yml` omits it (`…1NzM`). The unpadded
> form isn't valid standalone base64, but the giscus client restores the missing
> padding before decoding, so both resolve to the same underlying value
> (`010:Repository283822573`) — the dropped `=` is harmless.

The bottom of giscus.app also renders a **live widget** so you can see what your
readers will get (this preview runs against giscus's own demo repo):

![The live giscus comment widget rendered at the bottom of giscus.app](/assets/images/posts/giscus/07-live-widget-preview.png)

## Part 3 — Wire it into the zer0-mistakes site

Two pieces make it work: the **config block** below, plus the **vendored include**
from the previous section (`_includes/content/giscus.html`). Because that include
already contains the `<script>` template, you do **not** paste the giscus.app
snippet into a layout — you just give the include its two values via `_config.yml`:

```yaml
giscus:
  enabled: true
  data-repo-id: "MDEwOlJlcG9zaXRvcnkyODM4MjI1NzM"
  data-category-id: "DIC_kwDOEOrJ7c4CAn8D"
```

`site.repository` is already defined near the top of `_config.yml`, so
`data-repo` resolves to `bamr87/it-journey` automatically:

```yaml
github_user      : &github_user "bamr87"
repository_name  : &github_repository "it-journey"
repository       : [*github_user, "/", *github_repository]   # → bamr87/it-journey
```

### The gotcha that was hiding in this repo

Here's the real-world catch this walkthrough uncovered. IT-Journey's config
declared the block under the key **`gisgus:`** — a transposed-letter typo:

```yaml
## ❌ Before — the key is misspelled, so `site.giscus` is nil
gisgus:
  enabled: true
  data-repo-id: "MDEwOlJlcG9zaXRvcnkyODM4MjI1NzM"
  data-category-id: "DIC_kwDOEOrJ7c4CAn8D"
```

The theme reads `site.giscus.*` (correct spelling), but the config defined
`site.gisgus.*`. Liquid doesn't error on a missing key — it just returns `nil`.
So the layout guard `{% raw %}{% if page.comments != false and site.giscus %}{% endraw %}`
evaluated to false on every page, and **the comment widget never rendered.** No
error, no warning, no comments — for every post on the site.

The fix is one word:

```yaml
## ✅ After — key matches what the theme reads
giscus:
  enabled: true
  data-repo-id: "MDEwOlJlcG9zaXRvcnkyODM4MjI1NzM"
  data-category-id: "DIC_kwDOEOrJ7c4CAn8D"
```

The lesson generalizes: when a templating engine treats unknown keys as `nil`,
a misconfiguration looks identical to a disabled feature. If a config-driven
include silently produces nothing, **dump the variable** (`{% raw %}{{ site.giscus | inspect }}{% endraw %}`)
before assuming the include is broken.

### A second subtlety: defaults precedence, and the guard tests existence not `enabled`

Two things trip people up here. First, **defaults precedence**: the root scope
sets `comments: false`, but the more-specific `pages/_posts` scope sets
`comments: true`, and the most-specific matching default wins — so posts get
comments while everything else stays off. Override a single post with
`comments: false`. Second, the guard tests whether the `giscus` **key exists**,
not `site.giscus.enabled`. So `enabled: false` does *not* turn comments off
site-wide — only removing the whole `giscus:` block (making `site.giscus` nil)
does. Keep `enabled: true` for forward-compatibility, but treat the
`pages/_posts` default (plus per-post `comments: false`) as the real on/off switch.

## Part 4 — Verify it locally

Build the site and open any post (comments are on for the whole posts collection):

```bash
make serve            # Docker-based dev server on port 4002
# then browse to a comments:true post and scroll to the bottom
```

You should see the "Comments" section render the giscus iframe. If you'd rather
not spin up the full server, a quick build sanity check works too:

```bash
make build-ci         # CI-parity Jekyll build
```

Then confirm the rendered HTML actually contains the script with your real IDs:

```bash
grep -r "giscus.app/client.js" _site | head
grep -r "data-repo-id=\"MDEw" _site | head   # should NOT be empty
```

An empty result from the second command means `site.giscus.data-repo-id` is
still `nil` — i.e. the key is misspelled or missing.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Widget area is blank | `gisgus`/`giscus` key mismatch, or `enabled` missing | Match the key the theme reads; see Part 3 |
| "giscus is not installed on this repository" | App not installed/scoped | Reinstall the [giscus app](https://github.com/apps/giscus) for this repo |
| "Discussions is not enabled" | Feature off | Settings → General → Features → Discussions |
| Comments load but can't post | Repo is private | Make the repo public |
| Wrong/duplicate thread per page | Mapping mismatch | Keep `data-mapping="pathname"` and `data-strict="1"` consistent |
| `data-repo-id` empty in built HTML | Config not read | Run `make build-ci`, then grep `_site` as above |
| Build: "Could not locate the included file 'giscus.html'" | Theme include has a Liquid tag in its comment | Vendor a corrected, tag-free `_includes/content/giscus.html` (see Part 2's theme section) |
| Build: "stack level too deep" in `article.html` | The vendored include's comment includes itself | Remove the `{% raw %}{% include %}{% endraw %}` tag from the comment, or keep all Liquid tags out of comments entirely |

## Recap

- Giscus turns **GitHub Discussions** into a zero-backend comment system.
- giscus.app is a generator; for zer0-mistakes you only need the **`data-repo-id`**
  and **`data-category-id`** it produces — the rest is baked into
  `content/giscus.html`.
- Wire those two values (plus `enabled: true`) into a **`giscus:`** block in
  `_config.yml` — and double-check the spelling, because a `nil` key looks
  exactly like a disabled feature.
- Vendor a corrected `_includes/content/giscus.html` (tag-free comment) so the
  theme's Liquid-in-comment bug doesn't break the build.
- Comments are on for the whole **posts** collection by default (the
  `pages/_posts` default sets `comments: true`); opt a post out with
  `comments: false`. Notes, docs, quests, and hub pages use layouts that don't
  embed giscus, so they never show comments.

**Related:**

- [giscus.app](https://giscus.app/) — the configuration generator
- [GitHub Discussions docs](https://docs.github.com/en/discussions)
- [zer0-mistakes theme](https://github.com/bamr87/zer0-mistakes) — the theme powering this site
