---
title: 'Docker Container Fundamentals: Images to Registries'
author: IT-Journey Team
description: 'Master Docker container fundamentals: images versus containers, writing a Dockerfile, build and run workflows, image layers and caching, and registries.'
excerpt: Master Docker container fundamentals including images, the Dockerfile, layers, and registries for portable application deployment
preview: images/previews/container-fundamentals-isolation-quest-title-porta.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-30T00:00:00.000Z'
level: '0100'
difficulty: 🟡 Medium
estimated_time: 60-75 minutes
primary_technology: docker
quest_type: main_quest
quest_series: Docker Mastery
quest_line: The Adventurer's Forge
quest_arc: Containers of the Container Coast
quest_dependencies:
  required_quests: []
  recommended_quests: []
  unlocks_quests:
  - /quests/0100/docker-compose-orchestration/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic command line navigation (cd, ls, running a program)
  - Comfort editing plain text files in an editor
  - A rough idea of what a web server or application process is
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Docker Engine or Docker Desktop installed
  - A terminal and a text editor or IDE (VS Code recommended)
  skill_level_indicators:
  - Comfortable running commands and reading their output
  - Ready to experiment, break things, and rebuild
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A working image built from your own Dockerfile and run as a container
  skill_demonstrations:
  - Can explain the difference between an image and a container
  - Can write, build, and run a multi-stage-aware Dockerfile
  knowledge_checks:
  - Understands image layers and the build cache
  - Can push and pull from a registry
permalink: /quests/0100/container-fundamentals/
redirect_from:
- /quickstart/local-development/
categories:
- Quests
- DevOps
- Medium
tags:
- '0100'
- docker
- containers
- main_quest
- devops
- hands-on
- gamified-learning
keywords:
  primary:
  - '0100'
  - docker
  - containers
  secondary:
  - main_quest
  - devops
  - hands-on
  - gamified-learning
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0100 (4) Quest: Main Quest - Docker Fundamentals'
rewards:
  badges:
  - 🏆 Containerwright - Built and ran your first container from a hand-written Dockerfile
  - 📦 Image Smith - Understands layers, the build cache, and registries
  skills_unlocked:
  - 🛠️ Docker Image Authoring
  - 🧱 Container Lifecycle Management
  progression_points: 50
  unlocks_features:
  - Access to the Docker Compose Orchestration quest
layout: quest
---
*Greetings, brave adventurer! You have crossed into the **Adventurer tier**, and the salt air of the Container Coast fills your lungs. Here, applications no longer wander the host machine as homeless processes, fighting over libraries and ports. Instead, each one is sealed inside a tidy, portable crate that runs the same on your laptop, a teammate's machine, and a server in the cloud. This quest, **Container Fundamentals**, teaches you to forge those crates yourself.*

*Whether you have never typed `docker` before or you have copy-pasted Dockerfiles without truly understanding them, this adventure will give you a real mental model: what an image is, what a container is, how the two differ, and how layers, builds, and registries fit together.*

## 📖 The Legend Behind This Quest

*In the old days, shipping software meant shipping a list of incantations: "install this version of the runtime, then that library, then set these three environment variables, then pray." Every machine was subtly different, and the dreaded curse "but it works on my machine" haunted every release.*

*Then came the container. Borrowing its name from the steel boxes that revolutionized global shipping, a container packages an application together with everything it needs to run - code, runtime, libraries, and configuration - into one standardized, portable unit. The host no longer has to match the application's needs; the application brings its own world with it.*

*This quest teaches you the "why" behind every `docker` command, so that the rest of the Container Coast - Compose, CI/CD pipelines, and eventually Kubernetes - becomes a road you can actually read.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Images vs Containers** - Explain how a read-only image becomes a running container, and manage both lifecycles
- [ ] **Writing a Dockerfile** - Author a clear, correct Dockerfile from scratch for a real application
- [ ] **Build & Run Workflow** - Build an image with `docker build` and run it with `docker run`, mapping ports and passing environment
- [ ] **Image Layers & Cache** - Understand how each instruction creates a layer and how to order them for fast rebuilds

### Secondary Objectives (Bonus Achievements)
- [ ] **Registries** - Tag, push, and pull images from Docker Hub or another registry
- [ ] **Image Slimming** - Use a small base image and a multi-stage build to shrink your final image
- [ ] **Volumes & Logs** - Persist data with a volume and inspect a container's logs

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain the image/container distinction to another person without notes
- [ ] Write a Dockerfile for a new app and predict which instructions invalidate the cache
- [ ] Diagnose why a container exited and read its logs to find out
- [ ] Push an image to a registry and pull it onto a different machine

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Basic command line navigation (`cd`, `ls`, running a program)
- [ ] Comfort editing a plain text file in an editor
- [ ] A rough idea of what an application process or web server is

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Docker Engine or Docker Desktop installed and running
- [ ] A terminal and a text editor or IDE (VS Code recommended)
- [ ] Internet connection for pulling base images

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can run commands and read their output without fear
- [ ] You are willing to break a container and rebuild it
- [ ] Ready for 60-75 minutes of focused, hands-on learning

## 🌍 Choose Your Adventure Platform

*Docker behaves almost identically everywhere once it is installed - that is the whole point. The only difference between platforms is the installation step. Pick your path, install Docker, then verify with `docker run hello-world`.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install Docker Desktop (includes the engine, CLI, and a small VM)
brew install --cask docker

# Launch Docker Desktop once from Applications, then verify from the terminal
docker --version
docker run --rm hello-world
```

**macOS-Specific Notes:**
- Docker runs Linux containers inside a lightweight VM; this is automatic.
- A lighter alternative is `colima`: `brew install colima && colima start`.

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install Docker Desktop (uses the WSL 2 backend on Windows)
winget install Docker.DockerDesktop

# Restart if prompted, launch Docker Desktop, then verify
docker --version
docker run --rm hello-world
```

**Windows-Specific Notes:**
- Enable the WSL 2 backend for the best performance and Linux-container support.
- Run your `docker build` from a WSL 2 distro (e.g. Ubuntu) for fewer path surprises.

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Install Docker Engine via the convenience script (or your package manager)
curl -fsSL https://get.docker.com | sudo sh

# Add yourself to the docker group so you can run docker without sudo
sudo usermod -aG docker "$USER"   # log out and back in for this to take effect

# Verify
docker --version
docker run --rm hello-world
```

**Linux-Specific Notes:**
- On Linux, Docker runs natively - no VM, so it is the fastest path.
- Until you re-log after the `usermod`, prefix commands with `sudo`.

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# GitHub Codespaces and most cloud dev environments ship Docker preinstalled.
docker --version
docker run --rm hello-world

# No local install? Try the browser-based playground at https://labs.play-with-docker.com
```

**Cloud-Specific Notes:**
- Codespaces, Gitpod, and Cloud Shell let you complete this entire quest with zero local setup.
- Play with Docker gives you a throwaway Linux host for four hours per session.

</details>

## 🧙‍♂️ Chapter 1: Images vs Containers - The Blueprint and the Building

*Two words cause more confusion than any others when learning Docker. Conquer them now and everything else falls into place.*

### ⚔️ Skills You'll Forge in This Chapter
- The precise difference between an image and a container
- Running, listing, stopping, and removing containers
- Reading the output of `docker ps` and `docker images`

### 🏗️ The Blueprint and the Building

An **image** is a read-only template - a frozen snapshot of a filesystem plus the metadata needed to run a program. Think of it as the architectural blueprint, or a class in programming.

A **container** is a running (or stopped) instance of an image - a live process with its own isolated filesystem, network, and process tree. Think of it as the actual building, or an object instantiated from a class. You can run many containers from one image, just as you build many houses from one blueprint.

```bash
# Pull an image (downloads it; nothing runs yet)
docker pull nginx:alpine

# List images you have locally
docker images

# Run a container FROM that image, in the background, mapping host 8080 -> container 80
docker run --name web -d -p 8080:80 nginx:alpine

# See running containers
docker ps

# Visit http://localhost:8080 in your browser to see nginx serving its default page

# Stop and remove the container (the image stays behind)
docker stop web
docker rm web
```

The key insight: removing the *container* does not remove the *image*. The image is the reusable blueprint; the container is a disposable instance.

### 🔍 Knowledge Check: Images vs Containers
- [ ] If you run three containers from the `nginx:alpine` image, how many images exist?
- [ ] What does the `-p 8080:80` flag do, and which number is the host port?
- [ ] After `docker rm web`, is the `nginx:alpine` image still on your machine?

### ⚡ Quick Wins and Checkpoints
- [ ] **First container running**: `docker run hello-world` printed its success message
- [ ] **Served a page**: You reached an nginx container in your browser on port 8080
- [ ] **Cleaned up**: You stopped and removed a container without removing its image

## 🧙‍♂️ Chapter 2: The Dockerfile - Forging Your Own Image

*Pulling other people's images is useful, but the real power is building your own. The Dockerfile is the recipe: a plain text file of instructions that `docker build` executes top to bottom to produce an image.*

### ⚔️ Skills You'll Forge in This Chapter
- Writing the core Dockerfile instructions (`FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`)
- Building an image and tagging it
- Running your own image as a container

### 🏗️ Building Your First Real Image

Let's containerize a tiny Node.js web app. Create a project folder with three files.

**`app.js`** - the application:

```javascript
const http = require('http');
const PORT = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end(`Hello from inside a container! Host: ${require('os').hostname()}\n`);
});

server.listen(PORT, () => console.log(`Listening on port ${PORT}`));
```

**`package.json`** - so dependencies install cleanly (this app has none, but the file matters for caching):

```json
{
  "name": "container-hello",
  "version": "1.0.0",
  "main": "app.js",
  "scripts": { "start": "node app.js" }
}
```

**`Dockerfile`** - the recipe that turns the above into an image:

```dockerfile
# 1. Start from a small, official base image that already has Node.js
FROM node:20-alpine

# 2. Set the working directory inside the image
WORKDIR /usr/src/app

# 3. Copy ONLY the manifest first so dependency installs are cached separately
COPY package.json ./

# 4. Install dependencies (cached unless package.json changes)
RUN npm install --omit=dev

# 5. Now copy the rest of the source code
COPY . .

# 6. Document the port the app listens on
EXPOSE 3000

# 7. The default command run when a container starts
CMD ["node", "app.js"]
```

Now build and run it:

```bash
# Build an image and tag it "container-hello:1.0" (run from the project folder)
docker build -t container-hello:1.0 .

# Run it, mapping host port 3000 to the container's port 3000
docker run --name hello -d -p 3000:3000 container-hello:1.0

# Confirm it works
curl http://localhost:3000

# Override the PORT env var without rebuilding
docker run --rm -e PORT=4000 -p 4000:4000 container-hello:1.0
```

**Why copy `package.json` before the source?** Because of layer caching, covered next. If you copied everything at once, any code change would force a full reinstall of dependencies on every build.

### 🔍 Knowledge Check: The Dockerfile
- [ ] What does `FROM node:20-alpine` give you that you would otherwise have to install by hand?
- [ ] What is the difference between `RUN` and `CMD`?
- [ ] Why does `EXPOSE 3000` not actually publish the port to your host?

### ⚡ Quick Wins and Checkpoints
- [ ] **Built an image**: `docker build` finished with `naming to ... container-hello:1.0`
- [ ] **Ran your own image**: `curl http://localhost:3000` returned your greeting
- [ ] **Changed config**: You overrode `PORT` with `-e` without rebuilding

## 🧙‍♂️ Chapter 3: Layers, the Build Cache, and Registries - Mastery in Production

*Every Dockerfile instruction creates a layer - an immutable, stacked filesystem diff. Understanding layers makes your builds fast and your images small. Registries let you share those images with the world (or just your team).*

### ⚔️ Skills You'll Forge in This Chapter
- How layers and the build cache work, and how to order instructions to exploit them
- Shrinking images with small base images and multi-stage builds
- Tagging, pushing, and pulling from a registry

### 🏗️ Layers and the Build Cache

Each `FROM`, `COPY`, and `RUN` adds a layer. Docker caches each layer; on rebuild, it reuses every layer up to the first instruction whose inputs changed, then rebuilds from there down. This is exactly why `package.json` is copied before the source: editing `app.js` invalidates only the final `COPY . .` layer, not the expensive `npm install`.

```bash
# Inspect the layer history of your image
docker history container-hello:1.0

# Rebuild after editing only app.js — watch the dependency layer say "CACHED"
docker build -t container-hello:1.1 .
```

**Multi-stage builds** let you compile or bundle in one stage and ship only the result in a final, lean stage. This keeps build tools out of your production image:

```dockerfile
# ---- Stage 1: build ----
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build   # produces compiled output, e.g. in /app/dist

# ---- Stage 2: runtime (tiny, no build tools) ----
FROM node:20-alpine AS runtime
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY package.json ./
RUN npm install --omit=dev
EXPOSE 3000
CMD ["node", "dist/app.js"]
```

Pair this with a **`.dockerfile`-aware `.dockerignore`** so you never copy junk into the build context:

```text
node_modules
.git
*.log
Dockerfile
.dockerignore
```

### 🏗️ Registries: Sharing Your Image

A **registry** is a server that stores images. Docker Hub is the default public one; cloud providers and GitHub (GHCR) offer their own. An image name is really `registry/namespace/repository:tag`.

```bash
# Log in to Docker Hub (create a free account first)
docker login

# Tag your local image for your account (replace YOURNAME)
docker tag container-hello:1.0 YOURNAME/container-hello:1.0

# Push it to the registry
docker push YOURNAME/container-hello:1.0

# On any other machine, pull and run it — no source code needed
docker pull YOURNAME/container-hello:1.0
docker run --rm -p 3000:3000 YOURNAME/container-hello:1.0
```

That `pull` then `run` on a different machine is the entire promise of containers made real: the app runs identically, because it carries its own world.

### 🔍 Knowledge Check: Layers & Registries
- [ ] Why does editing `app.js` not trigger a re-run of `npm install` with the recommended COPY order?
- [ ] What does a multi-stage build keep *out* of your final image?
- [ ] In `YOURNAME/container-hello:1.0`, which part is the tag and which is the repository?

## 🧪 Chapter 4: The Live Development Loop - Editing on the Host, Running in the Crate

*So far you have rebuilt the image every time the code changes. That is correct for shipping, but painful while you are writing code. The trick for fast iteration is to **bind-mount** your project folder into the running container, so the container reads your live files instead of a frozen copy baked into the image. You edit in your editor on the host; the process inside the crate sees the change instantly.*

### ⚔️ Skills You'll Forge in This Chapter
- The difference between a **named volume** (managed data) and a **bind mount** (a host folder mapped in)
- A live-reload development loop without rebuilding the image
- Reading a container's logs while it runs

### 🏗️ Bind-Mount Your Source for Instant Feedback

A `-v <host-path>:<container-path>` flag maps a directory on your machine straight into the container. Combined with a tool that watches for file changes, this gives you edit-and-refresh development with no rebuild:

```bash
# Mount the current folder over the image's app directory, then run.
# Edits to app.js on the host are seen immediately inside the container.
docker run --name dev -d \
  -p 3000:3000 \
  -v "$(pwd)":/usr/src/app \
  container-hello:1.0

# Follow the logs in real time to watch requests and restarts
docker logs -f dev
```

Bind mounts are a **development convenience**, not a production pattern: in production the code lives *inside* the image so it travels with it. Use the mount only on your own machine for the tight feedback loop, then build a clean image to ship.

### 🏗️ One Command with Compose

Long `docker run` lines get unwieldy fast. A `compose.yaml` file records the same port mapping, volume, and environment once, so a single `docker compose up` launches everything:

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"        # host:container
    volumes:
      - .:/usr/src/app     # live bind mount of the source
    environment:
      - PORT=3000
```

```bash
docker compose up -d        # build (if needed) and start in the background
docker compose logs -f      # watch output
docker compose down         # stop and remove containers + network
```

This is your on-ramp to the next quest, where Compose wires *several* containers - an app, a database, a cache - into one application.

### 🔍 Knowledge Check: The Development Loop
- [ ] When would you bind-mount source instead of `COPY`-ing it into the image?
- [ ] Why is a bind mount a development-only trick rather than a way to ship code?
- [ ] What does `docker compose down` remove that simply stopping a container does not?

### ⚡ Quick Wins and Checkpoints
- [ ] **Edited live**: A change to `app.js` showed up without rebuilding the image
- [ ] **Followed logs**: `docker logs -f` streamed output while the container ran
- [ ] **Launched with Compose**: `docker compose up` started your app from one command

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Containerize a Static Site
**Objective**: Serve a single `index.html` you write yourself using an official nginx image.

**Requirements**:
- [ ] Write an `index.html`
- [ ] Write a Dockerfile that `FROM nginx:alpine` and `COPY`s your file into `/usr/share/nginx/html`
- [ ] Build, run with `-p 8080:80`, and view it in a browser

**Validation**: Run `curl http://localhost:8080` and see your HTML.

### 🟡 Intermediate Challenge: Slim and Configurable
**Objective**: Make the Node app from Chapter 2 read a greeting from an environment variable and build it on a small base image.

**Requirements**:
- [ ] App reads `GREETING` from the environment, defaulting to a sensible value
- [ ] Dockerfile uses an `alpine`-based image and a `.dockerignore`
- [ ] Run twice with two different `-e GREETING=...` values without rebuilding

**Validation**: Two runs return two different greetings; `docker images` shows a small image size.

### 🔴 Advanced Challenge: Multi-Stage and Published
**Objective**: Build an image with a multi-stage Dockerfile and push it to a registry.

**Requirements**:
- [ ] A two-stage Dockerfile (build stage + slim runtime stage)
- [ ] Tag it for Docker Hub or GHCR and `docker push` it
- [ ] Pull and run it in a fresh environment (or `docker system prune` first to prove the pull works)

**Validation**: A teammate (or a clean machine) can `docker run` your image with no source code present.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Containerwright** - You built and ran a container from your own Dockerfile
- 📦 **Image Smith** - You understand layers, the build cache, and registries

**🛠️ Skills Unlocked**:
- **Docker Image Authoring** - Write clear, cache-friendly Dockerfiles
- **Container Lifecycle Management** - Run, inspect, and clean up containers confidently

**🔓 Unlocked Quests**:
- Docker Compose Orchestration - Wire multiple containers into one application
- Frontend Docker - Containerize a full Jekyll + Bootstrap site

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Docker Compose Orchestration](/quests/0100/docker-compose-orchestration/) - Run an app, a database, and a cache together with one command

**Explore Side Adventures**:
- ⚔️ [Frontend Docker](/quests/0100/frontend-docker/) - Containerize a Jekyll + Bootstrap site

### Character Class Recommendations

**💻 Software Developer**: Continue to [Docker Compose Orchestration](/quests/0100/docker-compose-orchestration/)  
**🏗️ System Engineer**: Explore image hardening and registries in depth  
**🛡️ Security Specialist**: Study minimal base images and image scanning

## 📚 Resources

### Official Documentation
- [Docker: Get Started](https://docs.docker.com/get-started/) - The official onboarding guide
- [Dockerfile Reference](https://docs.docker.com/reference/dockerfile/) - Every instruction explained
- [Docker Build Cache](https://docs.docker.com/build/cache/) - How layer caching works

### Community Resources
- [Docker Hub](https://hub.docker.com/) - The default public image registry
- [Play with Docker](https://labs.play-with-docker.com/) - A free, browser-based Docker playground
- [Stack Overflow: docker tag](https://stackoverflow.com/questions/tagged/docker) - Q&A for when you get stuck

### Learning Materials
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/build/building/best-practices/) - Official guidance
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/) - Shrinking production images

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Built and ran a container from your own Dockerfile
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0100 - Frontend & Containers]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Unlocks:** [[Docker Compose Orchestration: Build Multi-Container Applications]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
