---
title: Home
author: bamr87
description: This is an overall outline of this site, and a place to start or come back to when lost.
excerpt: This is where we begin our journey. The place where we return after getting lost or wandering off.
purpose: To build a platform for learning and share knowledge and tools
keywords: Home, Zer0, IT-Journey, programming, development
permalink: /home/
bookmark: /zer0/
sidebar:
   nav: home
date: 2024-05-15T03:54:48.681Z
lastmod: 2025-07-03T16:40:00.000Z
categories:
  - home
  - navigation
  - guides
tags:
  - home
  - journey
  - learning
  - programming
  - development
  - tutorial
TODO:
   - Add a story line
draft: false
---

Go to [bookmark]({{ page.bookmark }})

## What to Build Today?

```text
I want to build an integration from GitHub to an LLM (such as Gemini) to review markdown files for grammar, spelling, completeness, etc., and then commit the changes for review.
```

## TODO 

{{ page.TODO }}
{:.dev-settings .alert .alert-warning}

## Introduction

This is where we begin our journey — the place where we return after getting lost or wandering off. Think of this as our home base with a collection of maps, tools, and information we need to traverse through this chaotic digital world.

There are [journals](/posts) to capture our experiences and findings, [notes](/notes) to quickly reference when our memories fail, and a [library](/docs) of documentation that gives us the depth of knowledge to build upon and share. Everything here is open source and free to use, and the goal is to make this repository a comprehensive learning tool for everyone to use and share.

## Abstract

From zero to hero collection of docs, tools, scripts, walk-through, and information to help with your IT journey.

### Zer0 to Her0 [Quest](/quest/)

<!-- TODO: Need story line  -->

1. Prologue - Init Hello World
   1. Who are you and what do you want?
   2. Are you willing to put in the time and effort to become a full-stack developer?
   3. What are your minimum requirements to start this journey?
   4. What are your goals?
   5. What are your expectations?
2. Chapter 1 - Identity Crisis
   1. Tools of the trade
   2. Minimum requirements
      1. Quick start with [github](https://docs.github.com/en/get-started/start-your-journey)
   3. Class Selection up
   4. Character Building
3. Chapter 2 - Training

### Skill Level Route

For those who prefer the route based on difficulty:

1. Beginner - 000
2. Intermediate - 001
3. Advanced - 010
4. Expert - 011
5. Master - 100
6. Hero - 101
7. Super Hero - 110
8. God - 111

### Stack Attack

For those who are intermediate/advanced and want to work on a specific stack:

1. Front-end (HTML, CSS, JS)
2. Back-end (Python, PHP, Ruby, Command Line)
3. Databases (MySQL, NoSQL, PostgreSQL)
4. Integrations (API, REST, GraphQL, SOAP)
5. Infrastructure (AWS, Azure, GCP, Linux)
6. Solutions (LAMP, Jamstack, MERN, WINS)

[Source](https://devopedia.org/full-stack-developer)
[Wiki](https://en.wikipedia.org/wiki/Solution_stack)

### Specialization route

For those who are advanced/expert and what to specialize in a field:

1. Infrastructure (System Administration, Networking, Operating Systems)
2. DevOps (Source Code control, CD/CI, Automated Testing, Agile Development)
3. Web Design (HTML, CSS, JavaScript, Jekyll, Bootstrap)
4. Software Engineering (Python, Ruby, Java, C#, C++)
5. Data Science (Python, SQL, BI, Hadoop, Spark, HBase, Hive, Kafka, Cassandra)
6. Cyber Security (Firewalls, Metadata analysis, Network Penetration, Ransomware, Vulnerability, Exploits, Malware)
7. Multimedia/Graphic Design (GIMP, Blender, Inkscape, Krita, Pencil 2D)
8. Mobile Development (Android, iOS, React Native)
9. Game Development (Unity, Unreal Engine)
10. AI (Machine Learning, Deep Learning, Natural Language Processing)

### Project Route

1. Wikimedia Server - [Downloads](https://www.mediawiki.org/wiki/Download)
2. Personal Website
3. Retro "Picade"
4. Mobile App
5. Web Scraper
6. Documentation Site
7. Video game

## Quick Start

For those who are already familiar with core IT concepts, this is the quick start guide to get you going. There are some prerequisites listed before you can clone this repository. Each is linked to a detailed installation instruction.

Master Setup [Local link](\_quickstart\machine-setup.md)  Or [Web link](\quickstart\machine-setup\)

Integrated Development Environment (Visual Studio Code) [Local link](\_quickstart\vscode.md)  Or [Web link](\quickstart\vscode\)

Static Website Generator (Jekyll) [Local link](\_quickstart\Jekyll.md)  Or [Web link](\quickstart\Jekyll\)

### Site layout

#### Top Navigation Bar

```html
{% raw %}
<div class="bd-example-snippet bd-code-snippet">
{%- include header.html -%}
</div>
{% endraw %}
```

This is a fixed navigation bar that is always visible at the top of the page. It is a horizontal bar that contains links to the different sections of the site. The links are organized into three sections:

- [Journals](/posts/)
- [Library](/docs/)
- [Notes](/Notes/)

#### Sidebar Navigation

The sidebar navigation is a vertical bar that is always visible on the left side of the page. It is automatically generated based on the navigation YAML file under ../_data/navigation.yml.

[Including](https://jekyllrb.com/docs/includes/) a [truncated](https://shopify.github.io/liquid/filters/truncate/) navigation YAML file under the `_data` folder will automatically generate the sidebar and top navigation.

```yaml
{%- raw -%}
{% capture nav %}{% include_relative _data/navigation-old.yml %}{% endcapture %}{{ nav | truncate: 332 }}
{% endraw %}
```

#### Table Of Contents right sidebar

This is an automatically generated table of contents that is always visible on the right side of the page. It is generated from using a programs located under /_includes/toc.html

It is based on the heading tags in the markdown file. The table of contents is generated from the markdown file and is updated whenever the markdown file is updated.

#### Source Code Short Cuts

Above the right TOC, there is a short cut to the source code. This is a link to the GitHub repository. The link to the shortcut is based on the config file located under /_config.yml. This is the where you have forked this repository.

```yaml
repository               : "bamr87/it-journey" # GitHub username/repo-name
local_repo               : "it-journey"
home_dir_pc              : &home-win '$HOME'
home_dir_mac             : &home-mac '$HOME'
local_git_pc             : [ *home-win, 'github\' ]
local_git_mac            : [ *home-mac, 'GitHub/' ]
```

NOTE: Replace `$HOME` with your home directory. Normally, it is the user id of the machine. Just type `echo $HOME` in the terminal.
{: .alert .alert-primary }

## Sitemap

{% include sitemap.html %}