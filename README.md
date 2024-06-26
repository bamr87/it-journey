---
title: README - it-journey
description: it-journey
excerpt: it-journey
version: 0.0.1
date-released: 2022-03-01
repo: https://github.com/bamr87/it-journey
tags:
    - it-journey
    - readme
    - jekyll
license: MIT
lastmod: 2024-05-17T01:42:30.675Z
created: 2022-03-01T12:00:00.000Z
draft: in progress
slug: readme
keywords:
    - readme
permalink: /readme/
layout: home
---


Branch | Build Status
---------|---------
Master | [![Build Status](https://app.travis-ci.com/bamr87/it-journey.svg?branch=master)](https://app.travis-ci.com/bamr87/it-journey)
gh-pages | [![Build Status](https://app.travis-ci.com/bamr87/it-journey.svg?branch=gh-pages)](https://app.travis-ci.com/bamr87/it-journey)

[![pages-build-deployment](https://github.com/bamr87/it-journey/actions/workflows/pages/pages-build-deployment/badge.svg?branch=gh-pages)](https://github.com/bamr87/it-journey/actions/workflows/pages/pages-build-deployment)

## README

Welcome to the source code reposoity for it-journey.dev.
 
test

## About IT-Journey.dev

IT-Journey.dev is a collaborative platform dedicated to the world of Information Technology (IT). Our mission is to provide a comprehensive resource for IT professionals, students, and enthusiasts to learn, share, and grow in the dynamic field of IT.

## What You'll Find Here

- **Tutorials & Guides:** Step-by-step tutorials and guides covering various IT topics, from basic programming to advanced network security.
- **Community Articles:** Contributions from members of the IT community, offering insights, tips, and experiences.
- **Resource Library:** A curated collection of resources like e-books, whitepapers, and tools beneficial for IT learning and development.
- **Discussion Forums:** Engage with other IT professionals, ask questions, and share your knowledge.
- **Career Advice:** Guidance and tips for building a successful career in IT, including interview preparation and resume building.

## How to Navigate

- **Homepage:** Start here to see the latest updates, featured articles, and community highlights.
- **Tutorials Section:** Categorized tutorials for easy navigation based on your interests and skill level.
- **Community Hub:** Access user-contributed articles and join discussions in the forums.
- **Resources:** Explore our extensive library of IT resources.
- **Career Center:** Get advice and tools for advancing your IT career.

## Contributing to IT-Journey.dev

We welcome and appreciate contributions from the IT community. Here’s how you can be part of our journey:

1. **Become a Contributor:** Share your expertise by writing articles or tutorials. Visit our 'Contribute' section for guidelines and submission details.
2. **Participate in Discussions:** Join our forums, answer questions, or start new topics to engage with the community.
3. **Provide Feedback:** Your suggestions help us improve. Use the 'Feedback' form on our site to share your thoughts.
4. **Share Resources:** If you have resources like tools, books, or articles beneficial to the IT community, let us know!

## Join Us

- **Sign Up:** Create your free account to start contributing and accessing exclusive content.
- **Follow Us:** Stay updated with the latest from IT-Journey.dev on [Twitter/Facebook/LinkedIn].
- **Newsletter:** Subscribe to our newsletter for weekly updates and highlights.

## Contact Us

For queries, support, or collaboration, contact us at [email@it-journey.dev](mailto:email@it-journey.dev).

Thank you for being part of IT-Journey.dev - Your Pathway to IT Mastery!

---

This template provides a clear and engaging overview of the site, its contents, and how users can contribute. You can tailor it to fit the specific features and guidelines of "it-journey.dev."


## Abstract

From zero to hero collection of docs, tools, scripts, and information to support your IT journey

## Pre reqs

* ruby 2.7.4
* jekyll 3.8
* git
* gh cli

## Docker Image Build

```shell
docker build -t it-journey .
```

## Docker Run
<!-- TODO: combine windows and mac commands -->

### Mac

```shell
# run the docker image and mount the local directory to the container and open a bash shell
# Run the container in detached mode
docker run -d -p 4002:4002 -v ${GITHOME}/it-journey:/app --name it_container it-journey

# Start the container and run the CMD line from the Dockerfile
docker start my_container

# Attach to the running container
docker exec -it my_container /bin/bash

```

```shell
http://localhost:4002/
```

### Windows

<!-- TODO: Check on windows docker bug "Auto-regeneration may not work on some Windows versions."-->

```shell
docker run -p 4002:4002 -v C:\Users\AmrAbdel-Motaleb\github\it-journey:/app it-journey
```

> [!NOTE]
> Auto-regeneration may not work on some Windows versions

## Sources

* [JTD](https://just-the-docs.github.io/just-the-docs/)
* [highlighting](https://jun711.github.io/web/how-to-highlight-code-on-a-Jekyll-site-syntax-highlighting/)
* [Static Badges](https://shields.io/badges)