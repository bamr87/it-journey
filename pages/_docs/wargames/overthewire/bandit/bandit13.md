---
title: Bandit13
description: 'The password for the next level is stored in the file data.txt,

  which is a hexdump of a file that has been repeatedly compressed.

  For this level it may be useful to create a directory under /tmp in

  which you can work. Use mkdir with a hard to guess d...'
permalink: /docs/wargames/bandit/bandit13/
date: '2026-04-07T01:41:08.000Z'
lastmod: '2026-04-07T01:41:08.000Z'
categories:
- wargames
tags:
- security
- wargames
- linux
- ctf
- cybersecurity
toc_sticky: true
source_repo: https://github.com/OverTheWireOrg/OverTheWire-website
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/bandit/bandit13.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

## Level Goal

The password for the next level is stored in the file **data.txt**,
which is a hexdump of a file that has been repeatedly compressed.
For this level it may be useful to create a directory under /tmp in
which you can work. Use mkdir with a hard to guess directory name.
Or better, use the command "mktemp -d".
Then copy the datafile using cp, and rename it using mv (read the
manpages!)

## Commands you may need to solve this level

grep, sort, uniq, strings, base64, tr, tar, gzip, bzip2, xxd, mkdir,
cp, mv, file

## Helpful Reading Material

- [Hex dump on Wikipedia][]

[Hex dump on Wikipedia]: https://en.wikipedia.org/wiki/Hex_dump
