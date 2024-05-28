---
title: level-010-frontend-docker
description: null
date: 2024-05-28T02:30:46.765Z
preview: null
tags: []
categories: []
sub-title: null
excerpt: null
snippet: null
author: bamr87
layout: null
keywords: {}
lastmod: 2024-05-28T04:25:00.957Z
slug: null
permalink: null
attachments: ""
type: default
draft: draft
---

Awesome! You’ve laid a strong foundation by setting up Docker and creating your Jekyll site. Now, let’s journey further into Level 010, where we will add Bootstrap 5 to enhance the visual appeal and functionality of your site.

### Level 010: Adding Bootstrap 5

#### Step 1: Open Project Directory

1. **Navigate to Your Project Directory:**
   - **Why It's Important:** This ensures you are working within the correct directory where your Jekyll site files are located.
   - **How to Do It:**
     - Open Terminal.
     - Navigate to your project directory using the command:
       ```sh
       cd my-jekyll-site
       ```
     - **Mystical Insight:** Think of this step as entering your workshop, where all your tools and materials are ready for the next stage of creation.

#### Step 2: Include Bootstrap 5

1. **Create `_includes/head.html` if it doesn’t exist:**
   - **Why It's Important:** The `_includes/head.html` file is where you can add HTML code that will be included in the `<head>` section of your site's pages. Including Bootstrap here ensures it’s available site-wide.
   - **How to Do It:**
     - Create the `_includes` directory and the `head.html` file:
       ```sh
       mkdir -p _includes
       touch _includes/head.html
       ```
     - **Mystical Insight:** Imagine crafting a magical charm that will be placed at the top of every page, imbuing each with the power of Bootstrap.

2. **Edit `_includes/head.html` to Include Bootstrap 5:**
   - **Why It's Important:** Adding Bootstrap 5 via a CDN (Content Delivery Network) makes it easy to integrate its powerful CSS and JS framework into your site without manual installation.
   - **How to Do It:**
     - Open `_includes/head.html` in your text editor and add the following code:
       ```html
       <!DOCTYPE html>
       <html lang="en">
       <head>
         <!-- Required meta tags -->
         <meta charset="utf-8">
         <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

         <!-- Bootstrap CSS -->
         <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-xxx" crossorigin="anonymous">

         <!-- Bootstrap JS and Popper.js -->
         <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>
         <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>
         <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0/js/bootstrap.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>
       </head>
       </html>
       ```
     - **Explanation of the Code:**
       - `<meta charset="utf-8">`: Sets the character encoding for the document.
       - `<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">`: Ensures proper scaling and layout on mobile devices.
       - `<link href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-xxx" crossorigin="anonymous">`: Includes Bootstrap CSS.
       - `<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>`: Includes jQuery, a dependency for Bootstrap's JavaScript.
       - `<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>`: Includes Popper.js, required for Bootstrap's tooltips and popovers.
       - `<script src="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0/js/bootstrap.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>`: Includes Bootstrap's JavaScript.

     - **Replace `xxx` with the appropriate integrity values from the Bootstrap CDN site:**
       - You can find these values on the [Bootstrap CDN page](https://getbootstrap.com/docs/5.0/getting-started/introduction/#cdn-links).

     - **Mystical Insight:** Embedding these scripts and styles is akin to enchanting your pages with Bootstrap’s spells, granting them enhanced beauty and functionality.

#### Step 3: Modify Your Layout

1. **Customize Your Homepage:**
   - **Why It's Important:** Customizing your homepage with Bootstrap components showcases Bootstrap’s capabilities and gives your site a professional and polished look.
   - **How to Do It:**
     - Open `index.md` or `index.html` in your text editor.
     - Replace its content with the following HTML code that uses Bootstrap components:
       ```html
       ---
       layout: default
       title: Home
       ---

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
       ```
     - **Mystical Insight:** Think of this step as decorating your enchanted clearing with beautiful artifacts. Each Bootstrap component adds a touch of elegance and utility to your site.

### Summary of Level 010

In Level 010, you’ve added Bootstrap 5 to your Jekyll site, allowing you to use its powerful CSS and JavaScript components. By including Bootstrap in the `_includes/head.html` file, you ensure it’s available across your entire site. You also customized your homepage to utilize Bootstrap’s components, enhancing the visual appeal and functionality of your site.

You've now equipped your site with the magical powers of Bootstrap. Are you ready to proceed to the next level, where we'll further customize and style your site? Or do you have any questions about Level 010? 🌟🏞️