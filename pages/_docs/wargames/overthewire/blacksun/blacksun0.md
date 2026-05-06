---
title: Blacksun0
description: 'Level0 is a remote format string intended to get you started with

  blacksun. It is a remote format string bug with you being able to see

  the reply, with address space randomisation enabled. You''ll need to use

  the direct parameter access method to anal...'
permalink: /docs/wargames/blacksun/blacksun0/
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
source_url: https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/blacksun/blacksun0.md
source_name: overthewire
license: MIT
---

> **Source:** This content is aggregated from [overthewire](https://github.com/OverTheWireOrg/OverTheWire-website) ([MIT](https://github.com/OverTheWireOrg/OverTheWire-website/blob/gh-pages/LICENSE)). Visit the original repository for the latest version.

Level0 is a remote format string intended to get you started with
blacksun. It is a remote format string bug with you being able to see
the reply, with address space randomisation enabled. You'll need to use
the direct parameter access method to analyse the stack and to
manipulate it.

Once getting access to a shell, read /etc/motd for more information

### Binary information

| Stack smashing protection (SSP):            | Enabled         				|
| Postition Independent Executable (PIE):     | Enabled         				|
| Address space layout randomisation (ASLR):  | Enabled         				|
| Non-executable pages:                       | None / disabled                             	|
|--------------------------------------------:+:------------------------------------------------|
| Location:                                   | Connect to blacksun.overthewire.org on port 79 	|

Alternatively, there is a debug version on port 78 if you need help
understanding what you're seeing


