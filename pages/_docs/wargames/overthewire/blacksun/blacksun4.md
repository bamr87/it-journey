---
title: Blacksun4
description: 'level4 is an installation of Apache and PHP with an introduced heap

  vulnerability.'
permalink: /docs/wargames/blacksun/blacksun4/
date: '2026-04-07T01:41:09.000Z'
lastmod: '2026-04-07T01:41:09.000Z'
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/blacksun/blacksun4.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

level4 is an installation of Apache and PHP with an introduced heap
vulnerability.

The introduced vulnerability is as follows:



Thanks to orix for the introduced code snippet

The document root is in /levels/level4/htdocs, you'll need to put your
php code there and call it via the webserver on port 55555.

**Note:** that if you're executing a shell, it can't be /bin/sh or
/bin/bash, oh, and the apache process can't access the /etc/pass
directory :P

### Binary information

| Stack smashing protection (SSP):            | Enabled         |
| Postition Independent Executable (PIE):     | Enabled         |
| Address space layout randomisation (ASLR):  | Enabled         |
| Non-executable pages:                       | None / disabled |
|--------------------------------------------:+:----------------|
| Location:                                   | 127.0.0.1:55555 |



