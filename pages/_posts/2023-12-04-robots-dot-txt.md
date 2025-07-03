---
author: bamr87
categories:
- posts
date: '2023-12-04T00:00:00.000Z'
description: null
draft: 2023-12-04 21:15:31.625000+00:00
excerpt: null
lastmod: 2024-05-16 02:49:07.594000+00:00
snippet: 2023-12-04 21:15:31.625000+00:00
sub-title: null
tags: []
title: robots dot txt
type: Article
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