---
title: "Robots.txt: Web Crawler Control for Jekyll Sites"
author: bamr87
categories:
    - Posts
    - Web-Development
    - SEO
date: '2023-12-04T00:00:00.000Z'
description: "Learn how to properly configure robots.txt files for Jekyll websites to control search engine crawlers and optimize SEO"
draft: false
section: Data & Analytics
excerpt: "Master robots.txt configuration for Jekyll sites to guide search engine crawlers and improve your site's SEO performance"
lastmod: 2024-05-16T02:49:07.594Z
snippet: "robots.txt - your site's first line of communication with search engines"
sub-title: "SEO and Web Crawler Management"
tags:
    - robots-txt
    - seo
    - jekyll
    - web-crawlers
    - search-engines
    - web-development
title: "robots dot txt"
type: Article
layout: journals
keywords:
    primary:
        - robots.txt
        - jekyll seo
        - web crawlers
    secondary:
        - search engine optimization
        - site indexing
        - crawler directives
permalink: /posts/robots-txt-jekyll/
---


A `robots.txt` file is used to instruct web robots (typically search engine robots) which pages on your website to crawl and which not to. Here's an example of a `robots.txt` file that you might use for a Jekyll site:

```plaintext
User-agent: *
Disallow: /secret/
Disallow: /private/
Disallow: /tmp/
Sitemap: {{ site.url}}/sitemap.xml
```

In this example:

- `User-agent: *` means that the instructions apply to all web robots.
- `Disallow: /secret/` tells robots not to crawl pages under the `/secret/` directory.
- `Disallow: /private/` and `Disallow: /tmp/` do the same for these directories.
- `Sitemap: https://www.yoursite.com/sitemap.xml` provides the location of your site's sitemap, which is helpful for search engines to find and index your content.

Remember to replace `https://www.yoursite.com/sitemap.xml` with the actual URL of your sitemap. Also, the `Disallow` entries should be adjusted based on the specific directories or pages you want to keep private or don't want to be indexed by search engines.