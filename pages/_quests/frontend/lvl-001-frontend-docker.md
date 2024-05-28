---
title: level-001-frontend-docker
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
lastmod: 2024-05-28T04:24:59.730Z
slug: null
permalink: null
attachments: ""
type: default
draft: draft
---

You've successfully set up your Docker environment, and now you're ready to delve deeper into the mystical realms of Level 001. This level involves creating your Jekyll site with the power of Docker, setting the stage for our enchanted journey ahead.

### Level 001: Create Jekyll Site with Docker

#### Step 1: Set Up Project Directory

1. **Open Terminal and Create Project Directory:**
   - **Why It's Important:** Organizing your project in a dedicated directory keeps your files tidy and manageable. It also ensures that Docker has a clear and specific location for your Jekyll site.
   - **How to Do It:**
     - Open Terminal.
     - Type the following command and press Enter:
       ```sh
       mkdir my-jekyll-site
       cd my-jekyll-site
       ```
     - **Mystical Insight:** Think of this as creating your enchanted clearing in the forest where you will build your magical project. This space is dedicated to your creative endeavors and will house all your files and configurations.

#### Step 2: Create Dockerfile

1. **Create a Dockerfile in Your Project Directory:**
   - **Why It's Important:** The Dockerfile is like a spellbook for Docker. It contains instructions for creating a Docker image that will run your Jekyll site. This ensures that your environment is consistent and replicable.
   - **How to Do It:**
     - In your project directory, create a file named `Dockerfile`:
       ```sh
       touch Dockerfile
       ```
     - Open the `Dockerfile` in your preferred text editor (e.g., `nano`, `vim`, or a graphical editor like VS Code).
     - Add the following content to the `Dockerfile`:
       ```Dockerfile
       FROM jekyll/jekyll:latest
       WORKDIR /srv/jekyll
       COPY . /srv/jekyll
       EXPOSE 4000
       ```
     - **Explanation of the Dockerfile Contents:**
       - `FROM jekyll/jekyll:latest`: This line specifies the base image for your container, which is the latest Jekyll image. It's like invoking a powerful Jekyll entity to help you.
       - `WORKDIR /srv/jekyll`: This sets the working directory inside the container. It's the enchanted location where your magic (Jekyll site) will come to life.
       - `COPY . /srv/jekyll`: This copies all the files from your project directory on your host machine to the working directory inside the container.
       - `EXPOSE 4000`: This tells Docker to expose port 4000, the port on which your Jekyll site will run.

#### Step 3: Create Docker Compose File

1. **Create a `docker-compose.yml` File:**
   - **Why It's Important:** Docker Compose allows you to define and run multi-container Docker applications. For our purposes, it simplifies the process of starting and managing your Jekyll container.
   - **How to Do It:**
     - In your project directory, create a file named `docker-compose.yml`:
       ```sh
       touch docker-compose.yml
       ```
     - Open the `docker-compose.yml` file in your text editor.
     - Add the following content to the `docker-compose.yml` file:
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
     - **Explanation of the `docker-compose.yml` Contents:**
       - `version: '3'`: Specifies the version of the Docker Compose file format.
       - `services`: Defines the services that make up your application.
       - `jekyll`: The name of the service. This service will run a Jekyll container.
       - `image: jekyll/jekyll:latest`: Uses the latest Jekyll image.
       - `command: jekyll serve --watch --force_polling`: Runs the `jekyll serve` command to start the Jekyll server and enable file watching.
       - `ports: - "4000:4000"`: Maps port 4000 on your host to port 4000 in the container, allowing you to access your Jekyll site at `http://localhost:4000`.
       - `volumes: - .:/srv/jekyll`: Mounts your project directory to the working directory inside the container, ensuring that changes you make locally are reflected in the container.

#### Step 4: Create a New Jekyll Site

1. **Run the Following Command in Terminal:**
   - **Why It's Important:** This command uses Docker Compose to run a Jekyll container that creates a new Jekyll site in your project directory. It's like casting a spell to summon a new magical realm.
   - **How to Do It:**
     - In your project directory, run the following command:
       ```sh
       docker-compose run jekyll jekyll new .
       ```
     - **Mystical Insight:** This command invokes the power of Docker and Jekyll to generate a new site. The `jekyll new .` part of the command tells Jekyll to create a new site in the current directory (`.`).

### Summary of Level 001

In Level 001, you've learned how to set up a project directory, create a Dockerfile and a Docker Compose file, and generate a new Jekyll site using Docker. Each step builds the foundation for running your Jekyll site in a consistent, isolated environment, ensuring that it behaves the same way regardless of where it's deployed.

You've now created the groundwork for your magical project, with Docker as your trusty companion. Are you ready to proceed to the next level, where we'll add Bootstrap 5 and start customizing your site? Or do you have any questions about Level 001? 🌟🏞️
