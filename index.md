---
title: Hello World
sub-title: Landing site for the IT Journey
description: This is the index.md file for the whole site and root
preview: /images/wizard-on-journey.png
layout: landing
keywords:
  - Github
  - Jekyll
  - Web Development
tags:
  - index
categories:
  - hello world
lastmod: 2024-05-08T04:53:36.889Z
slug: /
TODO: 
  - add 3rd level nav bar drop down option
  - automate pull request to publish to gh-pages
  - Add create new post button
  - add floating "back to top" button
  - create custom svg icon
  - quick view of post contents/reading time
  - Adjust menu toggle in Mobile view
  - leader board for level progression
  - Add keyboard shortcuts (e.g. ctl + / to toggle search)
  - Build Site map page [example](http://www.publicdomainsherpa.com/site-map.html)
  - Publish training article on [Programming Historian](https://programminghistorian.org/) 
  - Add search functionality
  - Add tab functionality https://idratherbewriting.com/documentation-theme-jekyll/mydoc_navtabs.html
  - Add GUI instructions for the n00bs
  - Add language title to code blocks
  - Integrate Jupyter Notebooks into the site
  - add embedded todo button for viewing
  - update SEO, document setup https://jsinibardy.com/optimize-seo-jekyll
  - add next/back button to turn pages
  - enhance right side bar design - [example](https://bootstrap-themes.github.io/dashboard/docs/#whats-included)
  - Cross reference features to documentation
  - alternate TOC structures (easy/med/hard) (pc/mac/linux) (by role)
  - add a tool kit page with all software tools used
  - Contribution Instructions
  - add [plugins](https://jekyllcodex.org/without-plugins/) without plugins
  - Auto integrate/embed source code files into documentation
  - UI testing automation - [Selenium](https://www.selenium.dev/)
  - page revision view (diff)
  - integrate kanban board
  - build account based system
  - simulate generic business operations
  - build backend todo interface checking
  - Build note to article function/workflow
---

{{ page.TODO }}
{: .collapse .collapsed .dev-settings }

# Welcome to IT-Journey.dev: Your Full Stack Development Quest Begins Here!

Embark on an epic adventure through the realms of full stack development, where coding skills empower you to build anything from the ground up. At IT-Journey.dev, we believe learning should be a quest - full of challenges, mysteries, and achievements. Are you ready to become a Full Stack Wizard?

## 🧙‍♂️ Begin Your Quest

In the world of IT-Journey.dev, your mission is to traverse through various lands, each representing a core aspect of full stack development. From the mystical Frontend Forests to the cavernous depths of Backend Badlands, your path is filled with engaging tutorials, hands-on projects, and legendary challenges.

### The Frontend Forests

- **Explore HTML Hills**: Master the ancient runes of HTML, crafting the skeleton of your digital creations.
- **CSS Cascades**: Weave magic with CSS to style your applications, making them not just functional but visually enchanting.
- **JavaScript Jungles**: Tame the wild beasts of JavaScript to breathe life into your static pages.

[Start Your Frontend Quest](/pages/_quests/frontend.md)

### The Backend Badlands

- **Node.js Nexus**: Harness the power of Node.js to build scalable and efficient server-side applications.
- **Database Dunes**: Learn to store and retrieve your quest's treasures with databases like MongoDB and PostgreSQL.
- **API Alps**: Conquer the peaks of API development, creating gateways to connect your frontend and backend realms.

[Begin Your Backend Journey](/backend)

### The DevOps Depths

- **Container Cove**: Dive into the world of Docker and Kubernetes, mastering the art of containerization and deployment.
- **CI/CD Cliffs**: Automate your deployment process with continuous integration and continuous deployment tools.

[Embark on the DevOps Voyage](/devops)

## 🗺️ Map Your Progress

Track your journey and mark your progress through the realms of IT-Journey.dev. Earn badges, unlock achievements, and climb the leaderboard as you complete quests.

## 🛡️ Join the Community

You're not alone on this journey. Join fellow adventurers in our community forums and Discord channel. Share your progress, seek help from seasoned wizards, and collaborate on quests.

[Join the Community](/community)

## 📚 Resources and Tools

Arm yourself with a selection of resources and tools designed to aid your quest. From code editors to development environments, we've gathered everything you need in one place.

[Access Resources](/resources)

---

This landing page sets the tone for a learning adventure, inviting users to explore full stack development in a fun and engaging way. Feel free to tweak the content however you see fit, or even create your own landing page to better fit your site's theme and structure. Good luck on your quest to educate the next generation of Full Stack Wizards!

Click on these particales for fun.

<div id="particles-js" class=""></div>

## Powered BY

{% for power in site.powered_by %}
<ul href="{{ power.url }}" rel="nofollow">{{ power.name }}</ul>
{% endfor %}

## FIXME:
- [ ] Fix the copy button on code snippets
- [ ] left sidebar header color
- [ ] Adjust menu toggle in Mobile view
- [ ] fix presentation of search results
- [ ] Need to fix quick index in side bar