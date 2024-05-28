---
title: Dockering Jekyll with Bootstrap 5
author: GPT and bamr87
excerpt: Embark on a quest to build a Jekyll site using Bootstrap 5 for CSS and JavaScript in the Frontend Forests. This guide will navigate you through the enchanted woods, ensuring you leverage the magical powers of Jekyll and Bootstrap to create an enchanting website.
layout: default
description: Embark on a quest to build a Jekyll site using Bootstrap 5 for CSS and JavaScript in the Frontend Forests. This guide will navigate you through the enchanted woods, ensuring you leverage the magical powers of Jekyll and Bootstrap to create an enchanting website.
draft: true
lastmod: 2024-05-28T04:11:52.774Z
permalink: /quests/frontend-docker/
---

Journey through the Frontend Forests to use Docker on a macOS system for building our Jekyll site with Bootstrap 5. This way, you won't have to worry about installing Ruby or other dependencies directly on your system.

### Step 1: Set Up Your Environment

#### Tools You Need:
- Docker Desktop
- Node.js (optional, but handy for managing JavaScript dependencies)

#### Installing Docker Desktop:
1. **Download Docker Desktop for Mac:** Go to the [Docker website](https://www.docker.com/products/docker-desktop) and download Docker Desktop for Mac.
2. **Install Docker Desktop:** Open the downloaded file and follow the installation instructions.

### Step 2: Create a New Jekyll Site

We'll create a Docker container for Jekyll and use it to create a new Jekyll site.

1. **Create a Dockerfile:**
   In your project directory, create a `Dockerfile`:
   ```Dockerfile
   FROM jekyll/jekyll:latest
   WORKDIR /srv/jekyll
   COPY . /srv/jekyll
   EXPOSE 4000
   ```

2. **Create a Docker Compose file:**
   Create a `docker-compose.yml` file in the same directory:
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

3. **Create a New Jekyll Site:**
   Open a terminal, navigate to your project directory, and run:
   ```sh
   docker-compose run jekyll jekyll new .
   ```

### Step 3: Add Bootstrap 5 to Your Jekyll Site

1. **Navigate to Your Project Directory:**
   ```sh
   cd my-jekyll-site
   ```

2. **Include Bootstrap:**
   Open `_includes/head.html` (create this file if it doesn’t exist) and add the following lines to include Bootstrap 5:
   ```html
   <!-- Bootstrap CSS -->
   <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-xxx" crossorigin="anonymous">

   <!-- Bootstrap JS and Popper.js -->
   <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>
   <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>
   <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0/js/bootstrap.min.js" integrity="sha384-xxx" crossorigin="anonymous"></script>
   ```

Replace the `xxx` with the appropriate integrity values from the Bootstrap CDN site.

### Step 4: Customize Your Site with Bootstrap Components

1. **Homepage Layout:**
   Open `index.md` or `index.html` and add some Bootstrap components:
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

2. **Styling Your Site:**
   You can customize Bootstrap's look and feel by overriding CSS in your main stylesheet (`assets/css/style.scss` or similar).

### Step 5: Deploy Your Jekyll Site

Now that your site is ready, let's deploy it to GitHub Pages.

1. **Create a Repository on GitHub.**
2. **Push Your Jekyll Site to This Repository:**
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin master
   ```

3. **Deploy to GitHub Pages:**
   - Go to your repository settings on GitHub.
   - Scroll down to the GitHub Pages section and select the branch to deploy from (usually `main` or `master`).

To start your local server with Docker, simply run:
```sh
docker-compose up
```
Visit `http://localhost:4000` to see your Jekyll site in action!

And there you have it! Your Docker-powered Jekyll site with Bootstrap 5 is up and running. If you need any more help, feel free to ask. Happy coding! 🌟