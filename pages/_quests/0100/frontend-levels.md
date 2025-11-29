---
title: Frontend Forests Levels
description: This guide will navigate you through the enchanted woods, ensuring you leverage the magical powers of Jekyll and Bootstrap to create an enchanting website.
date: 2024-05-28T02:17:12.672Z
preview: /images/frontend-forests.png
tags: []
categories: []
sub-title: null
excerpt: Embark on a quest to build a Jekyll site using Bootstrap 5 for CSS and JavaScript in the Frontend Forests
snippet: null
author: GPT and bamr87
layout: null
keywords: {}
lastmod: 2024-05-28T04:13:59.660Z
slug: frontend-forests-levels
permalink: null
attachments: ""
type: default
draft: draft
---

Absolutely! Let's structure our adventure with binary-coded levels, making our journey both organized and fun. Each level will have specific tasks and goals to help you progress step by step. Here’s our quest map in binary-coded levels:

### Level 000: Initial Setup

#### Step 1: Install Docker Desktop

1. **Download Docker Desktop for Mac:** 
   Go to the [Docker website](https://www.docker.com/products/docker-desktop) and download Docker Desktop for Mac.
   
2. **Install Docker Desktop:** 
   Open the downloaded file and follow the installation instructions.

#### Step 2: Verify Docker Installation

1. **Open Terminal:**
   - Type `docker --version` to check if Docker is installed correctly.
   - You should see something like `Docker version 20.10.7, build f0df350`.

### Level 001: Create Jekyll Site with Docker

#### Step 1: Set Up Project Directory

1. **Open Terminal and Create Project Directory:**
   ```sh
   mkdir my-jekyll-site
   cd my-jekyll-site
   ```

#### Step 2: Create Dockerfile

1. **Create a Dockerfile in Your Project Directory:**
   ```Dockerfile
   FROM jekyll/jekyll:latest
   WORKDIR /srv/jekyll
   COPY . /srv/jekyll
   EXPOSE 4000
   ```

#### Step 3: Create Docker Compose File

1. **Create a `docker-compose.yml` File:**
   ```yaml
   version: '3'
   services:
     jekyll:
       image: jekyll/jekyll:latest
       command: jekyll serve --watch --force_polling
       ports:
         - "4000:4000"
       volumes:
         - .:/srv/jekyll
   ```

#### Step 4: Create a New Jekyll Site

1. **Run the Following Command in Terminal:**
   ```sh
   docker-compose run jekyll jekyll new .
   ```

### Level 010: Adding Bootstrap 5

#### Step 1: Open Project Directory

1. **Navigate to Your Project Directory:**
   ```sh
   cd my-jekyll-site
   ```

#### Step 2: Include Bootstrap 5

1. **Create `_includes/head.html` if it doesn’t exist:**
   ```sh
   touch _includes/head.html
   ```

2. **Edit `_includes/head.html` to Include Bootstrap 5:**
   ```html
   <!-- Bootstrap CSS -->
   <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-xxx" crossorigin="anonymous">

   <!-- Bootstrap JS and Popper.js -->
   <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>
   <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>
   <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0/js/bootstrap.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>
   ```

Replace the `xxx` with the appropriate integrity values from the Bootstrap CDN site.

### Level 011: Customize Your Site

#### Step 1: Create Basic Layout

1. **Edit `index.md` or `index.html` to Add Bootstrap Components:**
   ```html
   <!DOCTYPE html>
   <html>
   <head>
     <meta charset="UTF-8">
     <title>My Jekyll Site</title>
   {% raw %}
   {% include head.html %}
   {% endraw %}
   </head>
   <body>
     <nav class="navbar navbar-expand-lg navbar-light bg-light">
       <a class="navbar-brand" href="#">Navbar</a>
       <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
         <span class="navbar-toggler-icon"></span>
       </button>
       <div class="collapse navbar-collapse" id="navbarNav">
         <ul class="navbar-nav">
           <li class="nav-item active">
             <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
           </li>
           <li class="nav-item">
             <a class="nav-link" href="#">Features</a>
           </li>
           <li class="nav-item">
             <a class="nav-link" href="#">Pricing</a>
           </li>
           <li class="nav-item">
             <a class="nav-link disabled" href="#">Disabled</a>
           </li>
         </ul>
       </div>
     </nav>
     <div class="container">
       <div class="jumbotron">
         <h1 class="display-4">Hello, world!</h1>
         <p class="lead">This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information.</p>
         <hr class="my-4">
         <p>It uses utility classes for typography and spacing to space content out within the larger container.</p>
         <a class="btn btn-primary btn-lg" href="#" role="button">Learn more</a>
       </div>
     </div>
     {% raw %}
     {% include footer.html %}
     {% endraw %}
   </body>
   </html>
   ```

#### Step 2: Customize Bootstrap

1. **Edit Main Stylesheet:**
   - You can override Bootstrap styles by editing `assets/css/style.scss` or your main stylesheet.

### Level 100: Deploy Your Site

#### Step 1: Create GitHub Repository

1. **Create a Repository on GitHub:**

#### Step 2: Push Site to Repository

1. **Run the Following Commands in Terminal:**
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin master
   ```

#### Step 3: Deploy to GitHub Pages

1. **Go to Your Repository Settings on GitHub:**
   - Scroll down to the GitHub Pages section.
   - Select the branch to deploy from (usually `main` or `master`).

### Level 101: Running and Viewing Your Site Locally

#### Step 1: Start Docker Container

1. **Run the Following Command in Terminal:**
   ```sh
   docker-compose up
   ```

2. **Visit `http://localhost:4000` in Your Browser:**

Congratulations! You've reached the end of our binary-coded adventure, and your Docker-powered Jekyll site with Bootstrap 5 is up and running. If you need any more help or want to explore more features, feel free to ask. Happy coding! 🌟