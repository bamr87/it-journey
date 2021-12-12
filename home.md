---
Title: IT-Journey
Author: bamr87
layout: default
permalink: /home/
Motive: I want to help my community to learn more about IT.
Intentions: Provide a platform for people to share their knowledge and experience about IT.
Keywords: 'Home, Zer0'
Description: This is an overall outline where you can start.
Post: null
lastmod: '2021-12-10T22:07:07.937Z'
toc: true
sidebar:
  nav: main
---

<!-- TODO:
- [x] Build Jekyll Layout
- [ ] Automate build process
- [ ] finish building the outline
- [ ] Add index link to jekyll for it-journey 
- [ ] Build Site map page
- [ ] Publish training article on [Programming Historian](https://programminghistorian.org/) 
- [X] Expand with open source colab to leverage the community
- [x]   Goal to cater to everyone's need
- [ ]   Publish manifesto article
-->

# it-journey.home

This is the starting point, midpoint, but never the endpoint. This is the place where we return after getting lost or wandering off. Think of this as our home base with a collection of maps, tools, and information we need to traverse through this chaotic digital world. There are journals to capture our experiences and findings, notes to quickly reference when our memories fail, and a library of documentation that gives us the depth of knowledge to build upon and share. Everything here is open source and free to use, and the goal is to make this repository a comprehensive learning tool for everyone to use.

## Abstract

From zero to hero collection of docs, tools, scripts, walk-throughs, and information to help with your IT journey.

## Quick Start

For those who are already familiar with core IT concepts, this the quick start guide to get you going. There are some prerequisites listed before you can clone this repository. Each is linked to a detailed installation instruction.

### Site layout

#### Top Navigation Bar

![](../assets/images/top-nav.png)

This is a fixed navigation bar that is always visible at the top of the page. It is a horizontal bar that contains links to the different sections of the site. The links are organized into three sections:

- [Journals](#journals)
- [Library](#Library)
- [Notes](#Notes)

#### Sidebar Navigation

The sidebar navigation is a vertical bar that is always visible on the left side of the page. It is automatically generated based on the navigation YAML file under ../_data/navigation.yml.

```yaml
main:
  - nav-title: "Main Menu"
  - title: "Home"
    url: /home/
  - title: "Journal"
    url: /posts/
  - title: "Library"
    url: /docs/
    sublinks:
    - title: "Jekyll"
      url: /docs/jekyll/
    - title: "Command Line"
      url: /docs/command-line/
  - title: "Notes"
    url: /notes/
    sublinks:
    - title: "home"
      url: /notes/
    - title: "shell"
      url: /notes/shell/    
    - title: "Javascript"
      url: /notes/js/
    - title: "Jekyll"
      url: /notes/jekyll/
  - title: "About"
    url: /about/
```

#### Table Of Contents right sidebar

This is an automatically generated table of contents that is always visible on the right side of the page. It is generated from using a programs located under /_includes/toc.html

It is based on the heading tags in the markdown file. The table of contents is generated from the markdown file and is updated whenever the markdown file is updated.

#### Source Code Short Cuts

Above the right TOC, there is a short cut to the source code. This is a link to the GitHub repository. The link to the shortcut is based on the config file located under /_config.yml. This is the where you have forked this repository.

```yaml
repository               : "bamr87/it-journey" # GitHub username/repo-name 
local_repo               : "it-journey"
local_git_pc             : "C:/Users/AmrAbdel-Motaleb/OneDrive/Documents/GitHub/"
local_git_mac            : "/Users/amr-mb/OneDrive/Documents/GitHub/"
```

### [Prerequisites](#prerequisites)

The best way to build the
In order to build this repository and contribute, you need the following applications installed:

- [VS Code](/posts/qs-vscode/)
- Github
- Ruby
- Jekyll

### [Installation](#installation)

```bash
cd ~/github/
gh clone bamr87/it-journey
```
### Features

- [x] Code Copy button
- [x] Side table of contents
- [x] Add quick edit links to GitHub and VS Code
- [x] Dark Mode toggle
  - [ ] [JTD](https://pmarsceill.github.io/just-the-docs/docs/customization/)
- [x] Navigation bar dropdown
- [x] auto genereate sidebar
- [ ] alternate TOC structures (easy/med/hard) (pc/mac/linux) (by role)
- [ ] Tool box page
- [ ] Contribution Instructions
- [ ] Search engine
- [x] Programming Language cheat sheets
- [x] Accordion TOC
- [x] bootstrap4
- [x] auto navbar 
  - [ ] [Just the Docs](https://pmarsceill.github.io/just-the-docs/docs/navigation-structure/)
- [ ] Add back to [top button](https://jun711.github.io/web/how-to-highlight-code-on-a-Jekyll-site-syntax-highlighting/) in cellphone view
- [ ] add [plugins](https://jekyllcodex.org/without-plugins/) without plugins
- [ ] Auto integrate/embed source code files into documentation
- [ ] UI testing automation - [Selenium](https://www.selenium.dev/)
- [ ] code snippet syntax [highlighting](https://jun711.github.io/web/how-to-highlight-code-on-a-Jekyll-site-syntax-highlighting/) 
- [ ] page revision view (diff)

[Java Docs](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

Edit in [VSCode](vscode://file/C:/Users/AmrAbdel-Motaleb/OneDrive/Documents/GitHub/{{ page.path}})

this page's path is {{ page.path}}


## /init_world

```bash
- Win - [pshero](it-journey-docs/notes/init-world/pshero.ipynb)
  - POLR
- Mac - [machero]
- Linux - [bashero]
- Cloud - [chero]

### Hello-World

### Paths

- Command and Conquer - CNC
  - PowerShell
    - WinGet
    - GitHub
    - VSCode
  - Bash
    - apt-get
  - Iterm
    - Homebrew
  - VS Code
- Git your shit together - GYST
  - Build
  - File Management
  - Continuous Integration and Continuous Deployment (CI/CD)
  - Source Code Management (SCM)
- Doc your Jekyll
  - Make the Docs
- Marry your Hub
  - Host the hub
  - Integrate
  - Continuously Integrate and Deploy - CID

## Story Lines

- Book vs Street Smarts - BVSS
- Share your creations - SYC
- Dr. Jekyll & Mr. Hub - DJMH
  - [examples](https://github.com/collections/github-pages-examples)

## Journal

<!-- TODO: Eventually, the only way to overcome these challenges is to leverage the community for help evolving the system to cater to everyone's needs. -->

## Level zer0   - 0000 - Navigation/Foundation

### RTD - Read the docs

- [PowerShell](https://docs.microsoft.com/en-us/powershell/)
- [Microsoft Docs](https://docs.microsoft.com/en-us/documentation/)
- [VS Code](https://code.visualstudio.com/docs)

### Get your tools

### Build your command center

### CLI - Command Line Interface

### Git - Source Code Control

- Milestones
  - Forking
  - Pull Requests
  - Branches

### Jekyll - Static Site Generator

Jekyll is a static site generator that is used to generate static websites.

```liquid
{% raw %}
{{site.github.repository_url}}
{% endraw %}
```

```html
{%raw %}
<div class="sidebar__top">
  <a href="'''liquid{{site.github.repository_url}}'''/blob/gh-pages/{{page.name}}">
    <i class="fab fa-github-square"></i>
  </a>
  <a href="vscode://file{{ site.local_git_pc}}/{{ site.local_repo }}/{{ page.path }}">
    <i class="fas fa-laptop-code"></i>
  </a>
  <a href="vscode://file{{ site.local_git_mac}}/{{ site.local_repo }}/{{ page.path }}">
    <i class="fas fa-laptop-code"></i>
  </a>
  <a href="#page-title" class="back-to-top">{{ site.data.ui-text[site.locale].back_to_top | default: 'Back to Top' }} &uarr;</a>
</div>
{% endraw %}
```

### MTD - Make the docs

[MkDocs](https://www.mkdocs.org/)

[Docusaurus](https://docusaurus.io/)

## Level 0n3    - 0001 - Basic building blocks

### Web building

### Infrastructure

### Database

## Level tw0    - 0010 - Programming

## Level thr33  - 0011 - PIjects

## Level f0ur   - 0100 - Front end basics

## Level f1v3   - 0101 - Back end basics

## Level s1x    - 0110 - Data basics

## Level s3v3n  - 0111 - Web Development

## Level 31ght  - 1000 - Security

## Level n1n3   - 1001 - Cloud

## Level t3n    - 1010 - Borne Again Solutions Hero

### Automate OS Install

[win](https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-setup-automation-overview)

## Tools and Equipment

### Terminal

#### Powershell

[operators](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators?view=powershell-7.1)

[sub-expression](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_operators?view=powershell-7.1#subexpression-operator--)

```powershell
"Today is $(Get-Date)"
```

> Today is 12/02/2019 13:15:20

```powershell
"Folder list: $((dir c:\ -dir).Name -join ', ')"
```

> Folder list: Program Files, Program Files (x86), Users, Windows

### Bash

### Iterm

## Package Management

- winget
- apt-get
- homebrew

## Text_Editor

- atom
- Notepad++
- xml Notepad
- Visual Studio Code
- [LaTeX](https://en.wikibooks.org/wiki/LaTeX)

## DevOps

### Source_Code

- Gitlab
- OneDrive

## IT Stack

### Infrastructure stack

### Security

### Web/App Development

### Networking

- DNS
- Authentication
- VPN
- Sub-Nets
- Ports
- HTTPS

## Development Areas

### Graphic Design - gdsn

1. GIMP
2. Inkscape
3. Blender
4. Krita
5. Pencil 2D

## #Data_analysis

- Database admin
- Data analytics

## Devops

### CI/CD

### System Administration

### Documentation

- wordpress
- mkdocs
- jekyll
- Pandoc
- Github Pages
- Docusaurus

### Colaboration

- Jupyter Notebooks
- Github
- Jekyll

> this is a quote
 
