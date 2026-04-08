---
title: Semtex9
description: 'Tunneling your firewall

  -----------------------

  How do you get data through a firewall that is blocking any tcp

  connection? You just don''t use a tcp connection, but instead other

  packets, that might not be filtered. For example network maintenance

  pr...'
permalink: /docs/wargames/semtex/semtex9/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/semtex/semtex9.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Tunneling your firewall
-----------------------
How do you get data through a firewall that is blocking any tcp
connection? You just don't use a tcp connection, but instead other
packets, that might not be filtered. For example network maintenance
protocols like ICMP.

There is a raw socket open on a yet unknown host that listens for
icmp packets and forwards them to a tcp server that you cannot
reach. Your job is to create a client that communicates with this
icmp "server". If everything works, you find yourself in a shell on
an unknown system, and can search for the password.

The protocol and the server, that is used by the ICMP tunnel is
described in your home directory. If you manage to blackbox analyze
it, then you can jump directly from semtex0 to semtex10 :)

You will have to use /rdx/rawwrapper. 



