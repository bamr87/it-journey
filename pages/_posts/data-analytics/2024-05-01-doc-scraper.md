---
title: "Document Scraping: Extracting Structured Data From Web Sources"
description: "Notes and exploration around document scraping techniques for extracting structured data from web sources — BeautifulSoup, Playwright, rate limiting, and storage patterns."
date: '2024-07-27T19:27:05.000Z'
lastmod: '2026-06-13T00:00:00.000Z'
preview: ''
tags:
- data-analytics
- python
- web-scraping
- beautifulsoup
categories:
- Data & Analytics
section: Data & Analytics
type: default
draft: false
keywords:
- data & analytics
- scraper
- python scraping
- beautifulsoup
- playwright
- structured data
excerpt: "Practical notes on doc scraping with BeautifulSoup, Playwright, and Scrapy — covering rate limiting, JS-rendered pages, storage patterns, and the failure modes that will catch you first."
author: bamr87
---

## Why Scrape Documents

Most data worth having is locked inside HTML pages, PDFs, and APIs that were never designed to be queried programmatically. A doc scraper bridges that gap — it turns unstructured or semi-structured web content into rows you can actually work with.

The catch: every site is slightly different. A technique that works on a corporate press releases page will break on a government PDF archive. The notes here track what worked on specific targets, not a universal solution.

## The Stack

Three tools cover most cases:

| Tool | Best For |
|---|---|
| `requests` + `BeautifulSoup` | Static HTML, small volumes |
| `Scrapy` | Large crawls, follows links, built-in throttling |
| `Playwright` / `Selenium` | JavaScript-rendered pages, login flows |

Start with `requests` + `BeautifulSoup`. It is the smallest surface area and the fastest to debug. Reach for `Playwright` only when the content does not exist in the raw HTML response.

## Basic Pattern

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table(url: str) -> pd.DataFrame:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")
    return pd.read_html(str(table))[0]
```

`pd.read_html` handles most well-formed HTML tables without writing a custom parser. For everything else, `.find_all()` with a CSS selector is the next step:

```python
rows = []
for item in soup.select("div.result-item"):
    rows.append({
        "title": item.select_one("h2.title").get_text(strip=True),
        "date":  item.select_one("span.date").get_text(strip=True),
        "link":  item.select_one("a")["href"],
    })
df = pd.DataFrame(rows)
```

## Handling JavaScript-Rendered Pages

When the raw HTML is mostly empty `<div>` tags and the data appears after scroll or click:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/data")
    page.wait_for_selector("table.results")
    html = page.content()
    browser.close()

soup = BeautifulSoup(html, "html.parser")
```

The `wait_for_selector` call blocks until the target element appears in the DOM. This is safer than a fixed `sleep`.

## Rate Limiting and Politeness

Scrapers that hammer servers get blocked — and rightly so. A few defaults that keep you off blocklists:

```python
import time, random

for url in urls:
    resp = requests.get(url, headers={"User-Agent": "research-bot/1.0"})
    process(resp)
    time.sleep(random.uniform(1.5, 3.5))  # jitter prevents pattern detection
```

Also check `robots.txt` before running anything at volume. `urllib.robotparser` handles the parsing:

```python
from urllib import robotparser

rp = robotparser.RobotFileParser()
rp.set_url("https://example.com/robots.txt")
rp.read()
rp.can_fetch("*", "https://example.com/data/page-1")  # True/False
```

## Storing the Output

For small runs, CSV is fine. For anything that needs to survive schema changes or multiple runs without duplicates:

```python
import sqlite3

conn = sqlite3.connect("scraped.db")
df.to_sql("results", conn, if_exists="append", index=False)
conn.close()
```

`if_exists="append"` lets you resume interrupted scrapes without re-processing already-captured rows. Add a `url` column as a dedup key and filter on it before each batch.

## Common Failure Modes

- **Selector breaks after site redesign** — target `data-*` attributes or stable IDs over positional CSS paths when possible.
- **IP block after N requests** — reduce rate, rotate user agents, or route through a proxy if the use case allows it.
- **Encoding errors** — set `resp.encoding = resp.apparent_encoding` before parsing if the site does not declare a charset.
- **Pagination stops early** — check whether "next page" is a link or a JavaScript event; the latter needs Playwright.

## Related

- [Post: Excel to Python](/posts/excel-to-python/)
- [Post: Robots.txt in Jekyll](/posts/robots-txt-jekyll/)
- [Docs: Data & Analytics Index](/posts/data-analytics/)
