---
title: Setting up Django and Git
author: Cloud Quest Guide
description: Learn how to efficiently set up Django with Git for seamless version
  control and project management in your web development journey.
excerpt: null
snippet: null
preview: /images/git-django.png
date: 2025-03-08 17:00:07.564000+00:00
lastmod: 2025-03-12 15:24:58.701000+00:00
level: '0010'
difficulty: 🟢 Easy
estimated_time: 30-60 minutes
primary_technology: Django
quest_type: main_quest
quest_series: Tools Collection
skill_focus:
- Development
- Git
- Programming
- Python
- Web Development
learning_style: hands-on
permalink: /quests/level-0010-django-and-git/
categories:
- Development
- Git
- Programming
- Python
- Web Development
tags:
- Django
- Git
- how-to
- python
- tutorial
keywords:
- Django
- Git
- how-to
- python
- tutorial
fmContentType: quest
comments: false
attachments: ''
sub-title: null
---
**Setting Up a GitHub Repository for Your Django Project**

**A Magical Adventure with VS Code**

🎩✨ Welcome, young sorcerer, to the mystical art of **Django Deployment**! Before your project can roam the digital realm freely, it must be contained in the enchanted vaults of **GitHub**. And who better to assist you than the powerful IDE known as **VS Code**?

So, grab your wand (*ahem*, keyboard) and let's begin this magical journey! 🧙‍♂️🐍

**Step 1: Summon Your Terminal (Command Line Magic!)**

First, navigate to your Django project directory. If you don't have one yet, conjure it with:

```
mkdir django-magic && cd django-magic
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install django
django-admin startproject myproject .
```

Poof! Your Django project is now alive! 🎇

**Step 2: Initialize the Git Spell**

In your terminal (*or the VS Code integrated terminal*), whisper the sacred words to initialize Git in your project folder:

```
git init
```

Your project is now under the watchful eye of Git, the guardian of version control. 🏰✨

**Step 3: Create a .gitignore Scroll**

Before pushing your secrets to GitHub, you must **ward off unnecessary files** from being tracked. Create a .gitignore file and add these forbidden artifacts:

```
# .gitignore
venv/
__pycache__/
db.sqlite3
.env
```

This prevents your **virtual environment** and **secret files** from escaping into the wild. Trust me, you don't want goblins (*or hackers*) meddling with your .env file. 🏴‍☠️

**Step 4: Summon GitHub and Create a Repository**

Now, visit [GitHub](https://github.com) and **create a new repository**. Give it a name, like **Django-Magic**, and **DO NOT** initialize it with a README (we'll do that ourselves).

Copy the provided **repository link**--- you'll need it in a moment! 🔗

**Step 5: Link Your Project to GitHub**

Now, cast the binding spell to connect your local project to the remote repository:

```
git remote add origin https://github.com/YOUR_USERNAME/Django-Magic.git
```

Check if the link is established:

```
git remote -v
```

Your project is now tethered to GitHub, ready to be uploaded into the sky! 🌩️☁️

**Step 6: First Commit -- Engraving the Scrolls**

It's time to **record your progress** and push it into the vast cosmos of GitHub!

```
git add .
git commit -m "Initial commit - A wizard is never late!"
```

Your work is now sealed in the **Git Grimoire**. 📜✨

**Step 7: Pushing Your Magic to GitHub**

With your spells in place, send your Django project to GitHub:

```
git branch -M main
git push -u origin main
```

🎆 **BOOM!** Your code now floats in the ethereal GitHub realm, safe and accessible from anywhere in the multiverse.

**Final Step: Open Your Project in VS Code**

To ensure everything is set up properly, open VS Code and use the **magic command**:

```
code .
```

From here, you can use VS Code's **source control panel** (the little Git icon on the sidebar) to monitor, commit, and push changes with ease.

**Congratulations, Sorcerer! 🎩🔮**

You've successfully **summoned**, **bound**, and **pushed** your Django project to GitHub. Now, your code is ready for collaboration, deployment, and world domination (*or at least, a solid website*).

May the **Git Force** be with you! 🚀🔥

Need help with the next step, like deploying this mystical project? Ask away, and we shall embark on another adventure! 🏰✨

```bash
#!/bin/bash

# ==========================
# 🔮 CONFIGURATION SECTION 🔮
# ==========================
PROJECT_NAME="django-magic"  # Change this to your project name
APP_NAME="magic"  # Change this to your Django app name
GITHUB_USERNAME="bamr87"  # Your GitHub username
GITHUB_REPO="https://github.com/$GITHUB_USERNAME/$PROJECT_NAME.git"  # GitHub repository URL
PYTHON_VERSION="python3"  # Change to "python" if using Python 2 (not recommended)
BRANCH_NAME="main"  # Default branch
VENV_NAME="venv"  # Virtual environment name


# ==========================
# 🚀 NAVIGATION SECTION 🚀
# ==========================
echo "🚀 Navigating to ~/github directory..."<end_o
cd ~/github || error_exit "Failed to navigate to ~/github directory."

# ==========================
# 🚀 HELPER FUNCTIONS
# ==========================
error_exit() {
    echo "❌ Error: $1"
    exit 1
}

check_command() {
    command -v "$1" >/dev/null 2>&1 || error_exit "$1 is not installed. Please install it first."
}

# ==========================
# 🔥 SETTING UP DJANGO PROJECT
# ==========================
echo "✨ Ensuring project directory exists: $PROJECT_NAME..."
mkdir -p $PROJECT_NAME && cd $PROJECT_NAME || error_exit "Failed to navigate to project directory."

echo "🐍 Checking virtual environment..."
if [ ! -d "$VENV_NAME" ]; then
    check_command $PYTHON_VERSION
    echo "🚀 Creating virtual environment..."
    $PYTHON_VERSION -m venv $VENV_NAME || error_exit "Failed to create virtual environment."
else
    echo "✅ Virtual environment already exists."
fi

echo "🧙‍♂️ Activating virtual environment..."
source $VENV_NAME/bin/activate || error_exit "Failed to activate virtual environment."

echo "📦 Checking Django installation..."
if ! python -c "import django" 2>/dev/null; then
    echo "🚀 Installing Django..."
    pip install django || error_exit "Failed to install Django."
else
    echo "✅ Django is already installed."
fi

if [ ! -d $PROJECT_NAME ]; then
    echo "🚀 Starting Django project..."
    django-admin startproject $APP_NAME . || error_exit "Failed to start Django project."
else
    echo "✅ Django project already exists."
fi

# ==========================
# 🔥 INITIALIZING GIT
# ==========================
if [ ! -d ".git" ]; then
    echo "🎩 Initializing Git repository..."
    git init || error_exit "Failed to initialize Git repository."
else
    echo "✅ Git repository already initialized."
fi

echo "⚡ Ensuring .gitignore exists..."
cat <<EOL > .gitignore
$VENV_NAME/
__pycache__/
db.sqlite3
.env
EOL
echo "✅ .gitignore updated."

echo "📜 Adding files to Git..."
git add . || error_exit "Failed to add files to Git."

if ! git rev-parse HEAD >/dev/null 2>&1; then
    echo "🖊️ Making initial commit..."
    git commit -m "Initial commit - A wizard is never late!" || error_exit "Failed to commit changes."
else
    echo "✅ Changes are already committed."
fi

# ==========================
# 🕸️ CREATING GITHUB REPO (AUTOMATIC)
# ==========================
check_command gh
echo "🔗 Checking if repository exists on GitHub..."
if ! gh repo view $GITHUB_USERNAME/$PROJECT_NAME >/dev/null 2>&1; then
    echo "⚡ Repository does not exist. Creating on GitHub..."
    gh repo create $GITHUB_USERNAME/$PROJECT_NAME --public --source=. --remote=origin || error_exit "Failed to create GitHub repository."
else
    echo "✅ Repository already exists on GitHub."
fi

# ==========================
# 🕸️ LINKING TO GITHUB
# ==========================
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "🔗 Adding remote repository..."
    git remote add origin $GITHUB_REPO || error_exit "Failed to add GitHub remote."
else
    echo "✅ Remote repository already set."
fi

echo "📡 Verifying remote link..."
git remote -v || error_exit "Failed to verify remote link."

if ! git rev-parse --abbrev-ref HEAD | grep -q "^$BRANCH_NAME$"; then
    echo "🌿 Renaming branch to $BRANCH_NAME..."
    git branch -M $BRANCH_NAME || error_exit "Failed to rename branch."
else
    echo "✅ Branch is already set to $BRANCH_NAME."
fi

echo "🚀 Pushing code to GitHub..."
git push -u origin $BRANCH_NAME || echo "⚠️ Failed to push code. Make sure you are authenticated with GitHub."

# ==========================
# 🎉 FINAL MESSAGE
# ==========================
echo "✨ All done! Your Django project is now safely stored in GitHub! 🚀"
echo "🎩 To start working on your project, use:"
echo "    cd $PROJECT_NAME && source $VENV_NAME/bin/activate && code ."
echo "🛠️ Happy coding, sorcerer! 🧙‍♂️"
```