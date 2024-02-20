---
title: LaTex your CV
sub-title: ""
author: ""
excerpt: ""
description: ""
snippet: 2023-11-05T02:50:50.370Z
categories: []
tags: []
draft: 2023-11-05T02:50:50.370Z
lastmod: 2023-11-27T10:59:17.163Z
type: Article
---

Installing LaTeX on a Mac, integrating it with Visual Studio Code, and using GitHub for source control involves several steps. Below is a comprehensive manual detailing each step in the process.

Installing LaTeX on macOS using Terminal
Install Homebrew:
If you don't have Homebrew installed, open Terminal and run the following command:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.```sh)"
```

Follow the on-screen instructions to complete the installation.

Update Homebrew:
Before installing any package, it's good practice to update Homebrew:

```sh
brew update
Install MacTeX:
```

MacTeX is a full LaTeX distribution for macOS. You can install it using Homebrew by running:

```sh

brew install --cask mactex
```

This process may take a while, as MacTeX is a large download (~4GB).

Verify Installation:
To check if LaTeX has been installed successfully, run:

```sh
which latex
```

This should output the path to the LaTeX binary.

Integrating LaTeX with Visual Studio Code
Install Visual Studio Code:
If you don't have Visual Studio Code installed, you can download and install it from the official website, or install it via Homebrew:

```sh
brew install --cask visual-studio-code
```

Install LaTeX Workshop Extension:

Open Visual Studio Code.
Go to Extensions by clicking on the square icon on the left sidebar or pressing Cmd+Shift+X.
Search for "LaTeX Workshop".
Click on the install button next to the LaTeX Workshop extension.
Using LaTeX to Build a Resume
Create a LaTeX Resume Template:

Open Visual Studio Code.
Create a new file with the .tex extension, for example, resume.tex.
Write or paste your LaTeX resume code into this file.
Here's a simple example of a LaTeX resume template:

```latex

\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{enumitem}
\begin{document}

\begin{center}
  \textbf{\Large Your Name}\\
  \small \textit{Your Address | Your City, State, Zip | Your Email | Your Phone}
\end{center}

\section*{Experience}
\begin{itemize}[leftmargin=*]
  \item \textbf{Job Title} - Company Name, Month Year - Present \\
  Description of your role and accomplishments.
\end{itemize}

\section*{Education}
\begin{itemize}[leftmargin=*]
  \item \textbf{Degree} - University Name, Month Year \\
  Brief details about your educational background.
\end{itemize}

\section*{Skills}
\begin{itemize}[leftmargin=*]
  \item Skill 1
  \item Skill 2
  \item Skill 3
\end{itemize}

\end{document}
```

Build the Resume:

Save the resume.tex file.
Press Cmd+Alt+B or go to the TeX badge in the status bar at the bottom and click on Build LaTeX project to compile the .tex file to a PDF.
Using GitHub as a Source Code Repository
Install Git:
If Git is not installed on your Mac, install it via Homebrew:

```sh
brew install git
```

Configure Git:
Set up your user name and email address for your Git commits:

```sh
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Create a GitHub Repository:

Visit GitHub and sign in.
Click on the "+" icon at the top right and select "New repository".
Fill in the repository name, description, and set the visibility.
Click "Create repository".
Initialize Your Local Repository:

Go to the folder where your LaTeX project is located in Terminal.
Initialize the repository:

```sh
git init
```

Add the remote repository:

```sh
git remote add origin https://github.com/yourusername/yourrepository.git
```

Add, Commit, and Push Your Resume:

Add the files to your local repository:

```sh
git add resume.tex
```

Commit the changes:

```sh
git commit -m "Initial commit of my LaTeX resume"
```

Push the changes to GitHub:

```sh
git push -u origin master
```

You should now have LaTeX installed on your Mac, be able to edit and compile LaTeX files using Visual Studio Code, and store your LaTeX projects on GitHub.