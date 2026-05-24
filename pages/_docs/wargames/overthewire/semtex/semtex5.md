---
title: Semtex5
description: 'Random Networking

  -----------------

  Make 10 connections to port 24027 from different IP''s. On each

  connection you will receive a string of 10 ASCII characters. XOR

  this string with the Semtex5 password, character by character. Then

  send back the 10 c...'
permalink: /docs/wargames/semtex/semtex5/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/semtex/semtex5.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Random Networking
-----------------
Make 10 connections to port 24027 from different IP's. On each
connection you will receive a string of 10 ASCII characters. XOR
this string with the Semtex5 password, character by character. Then
send back the 10 characters followed by another string of exactly 10
characters which identifies you (can be anything within A-Z, a-z,
0-9). The first 10 characters that you send, are different on every
connection, the last 10 have to be the same. If you do not send the
correct string back within 5 seconds you are disconnected. Once
connected with at least 10 different IP's You will receive the
password on one connection, chosen randomly.

**Note:  Your connections time out in 2 minutes and you cannot connect from an IP that is still connected.  May the sockets be with you. **

Reading Material
----------------
- [Socks5 Request For Comment][]

[Socks5 Request For Comment]: http://www.faqs.org/rfcs/rfc1928.html
