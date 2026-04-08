---
title: Blacksun2
description: 'Level2 is a test application from a [pop3 library][] that''s pretty

  buggy. The idea is to write a pop3 server to trigger a vulnerability

  (pick any you like :p) in the code and get a shell.'
permalink: /docs/wargames/blacksun/blacksun2/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/blacksun/blacksun2.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Level2 is a test application from a [pop3 library][] that's pretty
buggy. The idea is to write a pop3 server to trigger a vulnerability
(pick any you like :p) in the code and get a shell.

**Notes**

-   -fpic -fPIC was added to the compile options to remote DT\_TEXTREL's
    :p
-   If you're feeling generous, perhaps drop the author a note about any
    bugs you find so that future versions of the library can be fixed.
-   ASLR remote fun!

Binary information

### Binary information

| Stack smashing protection (SSP):            | Disabled        							|
| Postition Independent Executable (PIE):     | Disabled        							|
| Address space layout randomisation (ASLR):  | Enabled 								|
| Non-executable pages:                       | None / disabled 							|
|--------------------------------------------:+:------------------------------------------------------------------------|
| Code Location:                              | /levels/2/libspopc-0.7, using poptest1.c, and associated library code 	|
|---------------------------------------------+-------------------------------------------------------------------------|
| Location:                                   | /levels/level2							 	|

  [pop3 library]: http://brouits.free.fr/libspopc/
