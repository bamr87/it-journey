---
title: Vortex3
description: 'A Stack Overflow with a Difference

  ----------------------------------

  This level is pretty straight forward. Just sit down and understand

  what the code is doing. Your shellcode will require a

  setuid(LEVEL4\UID) since bash drops effective privileges. ...'
permalink: /docs/wargames/vortex/vortex3/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/vortex/vortex3.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

A Stack Overflow with a Difference
----------------------------------
This level is pretty straight forward. Just sit down and understand
what the code is doing. Your shellcode will require a
setuid(LEVEL4\_UID) since bash drops effective privileges. You could
alternatively write a quick setuid(geteuid()) wrapper around bash.

 **NOTE:** ctors/dtors might no longer be writable, although this
level is compiled with *-Wl,-z,norelro*. Lookup some information
about this e.g. [here][]

Reading Material
----------------
- [Smashing the Stack for Fun and Profit][]
- [Bypassing StackGuard and StackShield][]



[here]: http://unix.stackexchange.com/questions/8062/dtors-looks-writable-but-attempts-to-write-segfault
[Smashing the Stack for Fun and Profit]: http://phrack.org/issues/49/14.html#article
[Bypassing StackGuard and StackShield]: http://www.phrack.org/issues.html?issue=56&id=5#article
