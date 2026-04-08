---
title: Drifter1
description: Level 1 is a file parsing / heap corruption bug, with C++ classes.
permalink: /docs/wargames/drifter/drifter1/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/drifter/drifter1.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Level 1 is a file parsing / heap corruption bug, with C++ classes.

There is no need to mess around with heap exploitation, and C++ lends
itself to relatively straight forward exploitation.

[SMASHING C++ VPTRS][] - Although keep in mind that compiler changes can
influence how things are laid out.

When looking over the below code, keep in mind what needs to be done to
enable debugging, and what SetBuffer does.

One last hint: In order to correctly overflow the objects / pointers,
the allocation size will have to be similar to the class size ;) Even
blindly messing around will lead to code execution sooner or later

  [SMASHING C++ VPTRS]: http://www.phrack.org/issues.html?issue=56&id=8
