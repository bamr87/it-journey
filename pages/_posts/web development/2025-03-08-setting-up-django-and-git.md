---
title: "Setting Up Django and Git: A Magical Beginner's Guide"
description: "Learn to set up a Django project with Git version control and push it to GitHub from VS Code — a fun, wizard-themed walkthrough."
date: 2025-03-13T14:00:43.000Z
preview: /images/git-django.png
tags:
    - django
    - git
    - python
    - tutorial
    - beginner
categories:
    - Posts
    - Web Development
sub-title: "From zero to GitHub in one magical session"
excerpt: "A step-by-step guide to initializing a Django project, setting up Git, and pushing your code to GitHub — all wrapped in a wizard theme."
snippet: "Grab your wand (keyboard) and conjure a Django project bound to GitHub in minutes."
author: Cloud Quest Guide
draft: false
layout: article
keywords:
    primary:
        - django setup
        - git version control
    secondary:
        - github repository
        - python virtual environment
        - vs code
        - web development
lastmod: 2025-03-12T18:24:53.477Z
permalink: /setting-up-django-and-git/
attachments: ""
comments: true
difficulty: "🟢 Beginner"
estimated_reading_time: "8-10 minutes"
prerequisites:
    - "Python 3 installed on your system"
    - "Git installed and configured"
    - "A GitHub account"
    - "VS Code (recommended) or any text editor"
learning_outcomes:
    - "🎯 Create a Django project from scratch with a virtual environment"
    - "⚡ Initialize Git and configure .gitignore properly"
    - "🛠️ Push a local repository to GitHub"
    - "🔗 Understand the end-to-end workflow of project initialization"
section: Web Development
---

## Introduction

Welcome, young sorcerer, to the mystical art of **Django Deployment**! Before your project can roam the digital realm freely, it must be contained in the enchanted vaults of **GitHub**. And who better to assist you than the powerful IDE known as **VS Code**?

### 🎯 What You'll Learn

- How to create a Django project with a Python virtual environment
- How to initialize Git and protect secrets with `.gitignore`
- How to link a local repository to GitHub and push your first commit
- How to verify everything inside VS Code

### 📋 Before We Begin

Make sure you have **Python 3**, **Git**, and a **GitHub account** ready. VS Code is recommended but not required.

---

## Step-by-Step Implementation

### 🏗️ Phase 1: Create Your Django Project

#### Step 1: Set Up the Project Directory and Virtual Environment

**Objective**: Create a project folder, virtual environment, and install Django.

```bash
mkdir django-magic && cd django-magic
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install django
django-admin startproject myproject .
```

**Expected Result**: A `django-magic/` directory containing a `venv/` folder and the Django project files (`manage.py`, `myproject/`).

> **Windows Users**: Replace `source venv/bin/activate` with `venv\Scripts\activate`.

---

### 🔧 Phase 2: Initialize Git and Configure Tracking

#### Step 2: Initialize a Git Repository

**Objective**: Place your project under version control.

```bash
git init
```

Your project is now under the watchful eye of Git, the guardian of version control.

#### Step 3: Create a `.gitignore` File

**Objective**: Prevent sensitive and unnecessary files from being tracked.

Create a `.gitignore` file in the project root with the following contents:

```text
# .gitignore
venv/
__pycache__/
db.sqlite3
.env
```

**Why this matters**: This keeps your virtual environment, compiled bytecode, local database, and secrets out of version control — protecting your project from accidental exposure.

#### Step 4: Stage and Commit Your Files

**Objective**: Record the initial state of your project in Git history.

```bash
git add .
git commit -m "Initial commit - A wizard is never late!"
```

---

### ⚡ Phase 3: Push to GitHub

#### Step 5: Create a GitHub Repository

1. Visit [github.com/new](https://github.com/new)
2. Name your repository (e.g., `Django-Magic`)
3. **Do NOT** initialize it with a README — we already have local files
4. Copy the repository URL

#### Step 6: Link and Push

**Objective**: Connect your local project to GitHub and upload the code.

```bash
git remote add origin https://github.com/YOUR_USERNAME/Django-Magic.git
git remote -v  # Verify the remote link
git branch -M main
git push -u origin main
```

**Expected Result**: Your code is now live on GitHub. Visit your repository URL to confirm.

#### Step 7: Open in VS Code

```bash
code .
```

Use VS Code's **Source Control panel** (the Git icon in the sidebar) to monitor, commit, and push future changes with a graphical interface.

---

## Automation Script

For repeat use, here is a complete Bash script that automates the entire workflow:

```bash
#!/bin/bash

# ==========================
# 🔮 CONFIGURATION SECTION 🔮
# ==========================
PROJECT_NAME="django-magic"
GITHUB_USERNAME="YourGitHubUsername"
GITHUB_REPO="https://github.com/$GITHUB_USERNAME/$PROJECT_NAME.git"
PYTHON_VERSION="python3"
BRANCH_NAME="main"
VENV_NAME="venv"

# ==========================
# 🏗️ SETTING UP DJANGO PROJECT
# ==========================
echo "✨ Creating project directory: $PROJECT_NAME..."
mkdir "$PROJECT_NAME" && cd "$PROJECT_NAME"

echo "🐍 Creating virtual environment..."
$PYTHON_VERSION -m venv "$VENV_NAME"

echo "🧙‍♂️ Activating virtual environment..."
source "$VENV_NAME/bin/activate"

echo "📦 Installing Django..."
pip install django

echo "🚀 Starting Django project..."
django-admin startproject myproject .

# ==========================
# 🔥 INITIALIZING GIT
# ==========================
echo "🎩 Initializing Git repository..."
git init

echo "⚡ Creating .gitignore..."
cat <<EOL > .gitignore
$VENV_NAME/
__pycache__/
db.sqlite3
.env
EOL

echo "📜 Adding files to Git..."
git add .

echo "🖊️ Committing changes..."
git commit -m "Initial commit - A wizard is never late!"

# ==========================
# 🕸️ LINKING TO GITHUB
# ==========================
echo "🔗 Adding remote repository..."
git remote add origin "$GITHUB_REPO"

echo "📡 Verifying remote link..."
git remote -v

echo "🌿 Renaming branch to $BRANCH_NAME..."
git branch -M "$BRANCH_NAME"

echo "🚀 Pushing code to GitHub..."
git push -u origin "$BRANCH_NAME"

# ==========================
# 🎉 DONE
# ==========================
echo "✨ All done! Your Django project is now safely stored in GitHub! 🚀"
echo "🎩 To start working on your project, use:"
echo "    cd $PROJECT_NAME && source $VENV_NAME/bin/activate && code ."
echo "🛠️ Happy coding, sorcerer! 🧙‍♂️"
```

> **Note**: Update `GITHUB_USERNAME` and `PROJECT_NAME` before running.

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| `python: command not found` | Use `python3` instead, or verify your Python installation |
| `git: command not found` | Install Git via [git-scm.com](https://git-scm.com) or your package manager |
| Push rejected / permission denied | Verify your GitHub credentials and remote URL with `git remote -v` |
| `venv\Scripts\activate` fails on Windows | Use PowerShell or run `Set-ExecutionPolicy RemoteSigned` first |

---

## Key Takeaways

- **Virtual environments** isolate your project dependencies — always use one.
- **`.gitignore`** is essential to keep secrets and large files out of your repository.
- **Conventional commits** (like `feat:`, `fix:`) help maintain a clean Git history as your project grows.
- **VS Code's Source Control panel** makes Git operations visual and beginner-friendly.

---

## Next Steps

- Add a Django app: `python manage.py startapp myapp`
- Set up a `.env` file with [python-dotenv](https://pypi.org/project/python-dotenv/) for secret management
- Explore deploying your project to a cloud platform (Heroku, AWS, Azure)
- Learn about [GitHub Actions](https://docs.github.com/en/actions) for CI/CD automation

May the **Git Force** be with you! 🚀
