---
title: Frontend Docker - level 000
author: GPT and bamr87
layout: default
description: Verify Docker installation on macOS for building Jekyll sites with Bootstrap 5 in the Frontend Forests.
draft: true
tags:
    - level-000
    - frontend
    - docker
    - macos
    - jekyll
    - bootstrap
lastmod: 2024-05-28T02:28:31.950Z
---

## Intro

As you begin your journey through the Frontend Forests, imagine Docker Desktop as your magical backpack. It's filled with everything you need to build, deploy, and run your mystical projects. The Terminal is your enchanted wand, allowing you to cast spells (commands) to interact with Docker spirits. By verifying the Docker installation, you ensure that your backpack and wand are in perfect condition, ready to assist you on your quest.

### Level 000: Initial Setup

#### Step 1: Install Docker Desktop

1. **Download Docker Desktop for Mac:**
   - **Why It's Important:** Docker Desktop is crucial because it allows you to create, manage, and run Docker containers locally on your Mac. These containers will encapsulate your application along with its dependencies, ensuring that it runs consistently across different environments.
   - **How to Do It:**
     - Visit the [Docker website](https://www.docker.com/products/docker-desktop) and download Docker Desktop for Mac. This tool provides a user-friendly interface to manage Docker containers.
     - Once the download is complete, open the `.dmg` file and follow the installation prompts.

2. **Install Docker Desktop:**
   - **Why It's Important:** Installing Docker Desktop properly is essential as it sets up the Docker Engine on your Mac, allowing you to build and run containers.
   - **How to Do It:**
     - Open the downloaded file and drag the Docker icon to your Applications folder.
     - Launch Docker from your Applications folder.
     - Follow any additional setup instructions that appear, such as enabling Docker to have the necessary permissions.

#### Step 2: Verify Docker Installation

1. **Open Terminal:**
   - **Why It's Important:** The Terminal is a powerful tool for interacting with Docker via command-line interface (CLI). It's essential to verify that Docker is installed correctly and is operational.
   - **How to Do It:**
     - Open the Terminal application from your Applications folder or by using Spotlight search (Cmd + Space, then type "Terminal").

2. **Check Docker Version:**
   - **Why It's Important:** Checking the Docker version ensures that Docker has been installed correctly and is functioning. This step verifies the installation and lets you know which version of Docker is running, which can be important for compatibility reasons.
   - **How to Do It:**
     - In the Terminal, type the following command and press Enter:
       ```sh
       docker --version
       ```
     - You should see an output similar to `Docker version 20.10.7, build f0df350`.
     - **Mystical Insight:** Think of this step as summoning the Docker spirits. If they respond with their version number, you know they are ready to assist you in your journey.

### Why These Steps Are Crucial

1. **Setting Up Docker:**
   - Docker is a containerization platform that simplifies the process of managing application dependencies. By using Docker, you create a consistent environment for your application, eliminating the classic "works on my machine" problem. This ensures that your Jekyll site (and any other application) will run the same way, regardless of the underlying system.

2. **Verifying Docker Installation:**
   - Before embarking on more complex tasks, verifying that Docker is installed and working correctly saves time and frustration. It ensures that your foundational setup is solid, allowing you to build on it confidently.

### Detailed Explanations

- **Docker Desktop:** This is the application that provides a GUI for Docker on your Mac. It's the gateway to managing your Docker containers and images.
- **Terminal:** A command-line interface that allows you to execute commands directly on your system. It's a powerful tool for developers and a crucial part of managing Docker containers.
- **Docker Version Command:**
  - `docker --version`: This command checks the installed version of Docker. Knowing your Docker version helps in troubleshooting and ensuring compatibility with other tools and scripts.

### Conclusion

With Level 000 completed, you're now equipped with the knowledge and tools to venture further into the forest. Each step we take from here will build upon this solid foundation, guiding you deeper into the enchanted realms of Jekyll and Bootstrap.
