---
title: 'Doc Scraper: Convert HTML Documentation to Markdown with Python'
description: A small, reusable Python scraper that turns web documentation pages into clean Markdown using requests, BeautifulSoup, and markdownify — with simple content-area heuristics.
date: '2024-07-27T19:27:05.000Z'
preview: ''
tags:
- data-analytics
- python
- web-scraping
- markdown
categories:
- Data & Analytics
section: Data & Analytics
type: default
draft: false
keywords:
- html to markdown
- python web scraper
- beautifulsoup markdownify
- documentation scraping
lastmod: '2026-06-13T00:00:00.000Z'
excerpt: A small, reusable Python scraper that turns web documentation pages into clean Markdown using requests, BeautifulSoup, and markdownify.
author: bamr87
---

Documentation lives on the web as HTML, but most of the tools we actually work in — note vaults, static-site generators, LLM context windows — prefer Markdown. This post walks through a compact Python scraper that fetches a documentation page, isolates the meaningful content, and converts it to clean Markdown you can drop straight into a repo.

## Why convert HTML to Markdown?

- **Portability** — Markdown is plain text: diff-able, version-controllable, and readable anywhere.
- **Reuse** — pull reference material into your own notes, wikis, or Jekyll site.
- **AI workflows** — Markdown is a far cheaper, cleaner format to feed into a model than raw HTML.

## Prerequisites

```bash
pip install requests beautifulsoup4 markdownify
```

- [`requests`](https://requests.readthedocs.io/) — fetch the page.
- [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/) — parse the HTML.
- [`markdownify`](https://pypi.org/project/markdownify/) — convert an HTML fragment to Markdown.

## The scraper

The trick to a *useful* scrape is grabbing the main content and skipping the chrome (nav bars, sidebars, footers). The helper below tries a few common content containers in order, then falls back to the `<body>`:

```python
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def find_content(soup):
    """Return the most likely main-content element, with graceful fallback."""
    content_selectors = [
        {'tag': 'div', 'attr': {'class': 'main-content'}},
        {'tag': 'main', 'attr': {}},
        {'tag': 'article', 'attr': {}},
    ]

    for selector in content_selectors:
        content = soup.find(selector['tag'], attrs=selector['attr'])
        if content:
            return content

    # Fallback: the whole body (or None if even that is missing)
    return soup.find('body') or None


def html_to_markdown(url):
    """Fetch a page and convert its main content to Markdown."""
    response = requests.get(url)
    response.raise_for_status()  # raise on 4xx/5xx

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = find_content(soup)

    if content_div:
        return md(str(content_div), heading_style="ATX")
    return "Content not found."


# Example usage
url = 'https://getbootstrap.com/docs/5.3/components/modal/'
markdown_output = html_to_markdown(url)
print(markdown_output)
```

## How it works

1. **Fetch** — `requests.get(url)` pulls the raw HTML; `raise_for_status()` turns a bad response into an exception instead of silently scraping an error page.
2. **Parse** — BeautifulSoup builds a navigable tree from the HTML.
3. **Locate** — `find_content` walks a short list of heuristics (`div.main-content` → `main` → `article` → `body`). Ordering matters: the first match wins, so put the most specific selector first.
4. **Convert** — `markdownify` renders the chosen fragment to Markdown. `heading_style="ATX"` produces `#`-style headings (the form Jekyll/kramdown expect) rather than the underline style.

## Caveats and next steps

- **JavaScript-rendered pages** won't work with `requests` alone — the HTML you fetch is what the server sends, before any client-side rendering. For those, reach for a headless browser (Playwright, Selenium).
- **Site-specific tuning** — add selectors to `content_selectors` for the docs you scrape most (e.g. `div.content`, `div#docs-content`).
- **Be a good citizen** — check `robots.txt`, throttle requests, and cache results so you don't hammer a site while iterating.
- **Clean-up pass** — real-world output often needs light post-processing (stripping "On this page" blocks, collapsing blank lines). A few regex substitutions go a long way.

The full working notebook — including a complete sample conversion of the Bootstrap modal docs — lives in the notes: [HTML to Markdown Web Scraping](/notes/html_md_doc_scrapper/).
