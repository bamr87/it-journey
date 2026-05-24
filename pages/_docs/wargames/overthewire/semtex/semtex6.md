---
title: Semtex6
description: 'ICMP forging

  ------------

  Send a special ICMP packet to an unknown host. Add the correct

  payload to it, to make sure you can receive the password. Spoof your

  origin address and make semtex believe, the packet is really coming

  from some government ser...'
permalink: /docs/wargames/semtex/semtex6/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/semtex/semtex6.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

ICMP forging
------------
Send a special ICMP packet to an unknown host. Add the correct
payload to it, to make sure you can receive the password. Spoof your
origin address and make semtex believe, the packet is really coming
from some government server (\*.gov) Make sure this server you are
sending from has a reverse DNS entry, otherwise you will not receive
an answer.

You find more specific information in your home directory.
** Note: You will have to use /semtex/semtexraw. Take a look at the source**

Reading Material
----------------
- [ICMP Request For Comment][]
- [Mixter's raw socket tutorial][]



[ICMP Request For Comment]: http://www.faqs.org/rfcs/rfc792.html
[Mixter's raw socket tutorial]: http://mixter.void.ru/rawip.html
