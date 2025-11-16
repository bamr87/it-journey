---
title: "Working Directories: Backbone of Software Builds"
description: How working directories shape tooling, builds, tests, deployments—and how directory assumptions can break or harden pipelines.
date: 2025-11-16T00:50:00.488Z
preview: /images/post-preview-working-directory.png
tags:
    - devops
    - build-systems
    - filesystem
    - debugging
    - best-practices
categories:
    - Posts
    - DevOps
    - Tutorials
sub-title: How current directories quietly shape your tools, tests, and CI pipelines
excerpt: Working directories look trivial—`cd` and forget—but they define how tools resolve paths, load configs, cache artifacts, and can make builds reproducible or fragile. This article dissects their power, pitfalls, and best practices.
snippet: Every build has a working directory; the best ones don’t surprise you.
author: IT-Journey Team
layout: journals
keywords:
    primary:
        - working-directory
        - build-systems
    secondary:
        - ci-cd
        - path-resolution
        - tooling
lastmod: 2025-11-16T02:42:33.708Z
permalink: /posts/working-directories-in-software-development/
attachments: ""
comments: true
difficulty: 🟡 Intermediate
estimated_reading_time: 20-30 minutes
prerequisites:
    - Basic command-line experience (cd, ls, pwd)
    - Familiarity with project structures and build tools (npm, Maven, Make, etc.)
learning_outcomes:
    - 🎯 Explain what a working directory is across OSes and shells.
    - ⚡ Predict how tools will resolve relative paths and configs.
    - 🛠️ Design build scripts that are robust to directory changes.
    - 🔗 Identify and fix working-directory-related flakiness in builds and CI.
content_series: DevOps Foundations
related_posts: []
validation_methods:
    - Reproduce common working-directory bugs and apply fixes described in the article.
    - Refactor an existing build script to be directory-agnostic and compare behavior.
    - Run the same build pipeline locally and in CI to confirm consistent results.
---

## Introduction

If you ask developers where their app "runs," many will talk about servers, containers, or cloud regions. Far fewer will mention the quiet constant that shapes nearly every command: the **working directory**.

The working directory (also called the *current directory*) is where your process *thinks it is* in the filesystem. It decides how `"./scripts/build.sh"` is resolved, which `config.yml` a tool picks, where logs end up, and whether your CI pipeline passes or fails.

In this article we’ll go deep on:

- What a working directory is in operating systems, shells, and runtimes
- How it affects compilers, test runners, package managers, and CLIs
- How build systems, containers, and CI pipelines rely on it—often implicitly
- Classic misuses that lead to flaky builds and "works on my machine" bugs
- Practical patterns for making working-directory behavior explicit and robust

### 🌟 Why This Matters

Working directories feel trivial: `cd project && run-something`. But in modern software development, they sit at the intersection of **build reproducibility**, **security**, and **maintainability**:

- CI jobs often run in different working directories than local commands.
- Relative paths in scripts can silently break when you reorganize a repo.
- Tools can load the "wrong" config or cache because you started them in the wrong place.
- Misconfigured working directories can leak secrets, write logs to unexpected locations, or corrupt caches.

Understanding this concept deeply turns working directories from a hidden source of bugs into a tool you use deliberately.

### 🎯 What You’ll Learn

By the end of this article, you’ll be able to:

- Define the working directory precisely and inspect it in common environments.
- Predict how tools like `git`, `npm`, `pytest`, `mvn`, `make`, and `docker` use it.
- Spot brittle assumptions in scripts and CI pipelines related to `cd` and relative paths.
- Refactor build logic to be directory-agnostic and reproducible.

### 📋 Before We Begin

You’ll get the most out of this article if you:

- Are comfortable in a terminal on macOS, Linux, or Windows (WSL/PowerShell).
- Have used at least one build or package tool (e.g., `npm`, `yarn`, `maven`, `gradle`, `make`, `dotnet`, `cargo`).

We’ll show shell snippets in `bash`/`zsh`, but the ideas apply across environments.

## 1. What Is a Working Directory, Really?

At any moment, a running process has a *current working directory* (CWD): a path the OS associates with that process. When the process accesses a **relative path** (like `"logs/app.log"`), the OS interprets it relative to that directory.

Formally, if a process has working directory $D$ and opens a path $p$:

- If $p$ is **absolute** (e.g., `/var/log/app.log`), the OS uses $p$ as-is.
- If $p$ is **relative** (e.g., `logs/app.log`), the OS resolves it as $D/p$.

### 1.1 Inspecting the Working Directory

In a shell, your interactive session is itself a process with a working directory.

```bash
pwd           # print working directory
cd /tmp       # change to /tmp
pwd           # now /tmp
```

Most shells also expose `$PWD` as an environment variable that tracks the current directory:

```bash
echo "Current dir is: $PWD"
```

Inside many languages, you can query the CWD as well:

```python
import os
print(os.getcwd())
```

```javascript
// Node.js
console.log(process.cwd());
```

```java
System.out.println(System.getProperty("user.dir"));
```

These APIs matter because tools and frameworks often call them under the hood.

### 1.2 How the Working Directory Is Set

The working directory always comes from somewhere:

- When your shell launches, it typically starts in your home directory.
- When you run a command, the child process inherits the shell’s current working directory by default.
- Programs can call APIs like `chdir()` (POSIX) or `SetCurrentDirectory()` (Windows) to change their own working directory.

This means that just typing `cd` before a command can **change the behavior of that command** without changing any of its arguments.

```bash
cd /path/to/project
npm test         # runs with CWD=/path/to/project

cd /path/to/project/submodule
npm test         # same command, different working tree and config discovery
```

## 2. How Working Directories Shape Real-World Tools

Let’s look at concrete ways tools depend on the working directory.

### 2.1 Version Control: `git`

`git` discovers the repository by walking *up* from the working directory until it finds a `.git` directory.

- Run `git status` from inside `project/` or any subdirectory: it operates on the same repo.
- Run `git status` from a parent directory that’s not part of the repo: you’ll get an error.

This is why many workflows say "`cd` into the repo, then run git commands." The working directory anchors repo discovery.

### 2.2 Build and Test Tools

Many build systems read config files and resolve paths relative to the working directory:

- **Node.js / npm / yarn**
	- `npm install`, `npm test`, and many scripts expect to run where `package.json` lives.
	- Tools like ESLint or Jest often auto-discover configs (`.eslintrc`, `jest.config`) by walking up from the working directory.

- **Python tools**
	- `pytest` discovers tests relative to the CWD and may auto-add it to `sys.path`.
	- `pip` and `flit` commands often assume you’re in the project root where `pyproject.toml` or `setup.cfg` live.

- **Java / JVM tools**
	- `mvn` and `gradle` read `pom.xml` or `build.gradle` from the working directory.
	- Changing the CWD changes *which project* you’re operating on.

- **C/C++ / systems builds**
	- `make` uses `Makefile` from the working directory (or parent directories via `-C` / `include`).
	- Many CMake workflows assume you’re in a `build/` directory when running `cmake` and `make`.

In all of these, the working directory is part of the "project identity"—it decides which project you’re actually building.

### 2.3 CLIs and Config Discovery

Lots of CLIs implement an "implicit config" pattern: start from the working directory and look for config files, often walking upward:

- Linters (`eslint`, `flake8`, `stylelint`)
- Formatters (`prettier`, `black`)
- Static analyzers and security tools

Example with `eslint`:

```bash
cd project/frontend
npx eslint src

cd project
npx eslint frontend/src
```

Same codebase, different CWDs, potentially different `.eslintrc` inheritance chains.

### 2.4 Logging, Temp Files, and Artifacts

Many applications log to relative paths like `logs/app.log` or write temp files into `./tmp`.

If the CWD changes:

- Logs may be written into unexpected directories.
- Temporary files may clutter CI workspace roots or system temp directories.
- Cleanup scripts that assume a specific structure might miss or delete the wrong files.

In production, that can mean losing important logs or filling disks in unexpected places.

## 3. Working Directories in Build Pipelines

Build systems and CI platforms embed working-directory assumptions directly into their execution models.

### 3.1 Local Builds vs. CI Builds

Locally, you often run:

```bash
cd /Users/you/dev/my-app
npm run build
```

In CI, the platform might:

- Check out the repo into `/home/runner/work/my-app/my-app`.
- Change the working directory explicitly before steps.
- Run commands from nested directories.

For example, GitHub Actions:

```yaml
jobs:
	build:
		runs-on: ubuntu-latest
		steps:
			- uses: actions/checkout@v4
			- name: Install deps
				run: npm ci
				working-directory: frontend
```

If your scripts assume `CWD=repo-root`, they’ll break when CI sets `working-directory: frontend`.

### 3.2 Monorepos and Nested Working Directories

In monorepos, you often have multiple packages:

```text
repo/
	package-a/
	package-b/
	tools/
```

CI might run different jobs with different working directories:

- `cd package-a && npm test`
- `cd package-b && npm test`

If shared scripts in `tools/` assume they’re always run from the repo root, they may fail when invoked from `package-a`.

### 3.3 Containers and `WORKDIR`

In Docker and similar runtimes, `WORKDIR` sets the process working directory *inside* the container:

```dockerfile
FROM node:20-alpine
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm ci
COPY . .
CMD ["npm", "start"]
```

Here:

- `WORKDIR /usr/src/app` ensures all subsequent `COPY`, `RUN`, and `CMD` instructions run relative to `/usr/src/app`.
- If you forget to set `WORKDIR`, commands may run from `/`, and relative paths like `COPY . .` or `npm start` may behave unexpectedly.

In docker-compose or Kubernetes, you may also override working directories per container, leading to subtle differences between local Docker runs and other environments.

## 4. Common Misuses and Pitfalls

Now to the painful parts: how working directories get misused and how that breaks builds.

### 4.1 Implicit `cd` in Scripts

Scripts that silently `cd` without clear boundaries are a classic source of flakiness:

```bash
#!/usr/bin/env bash
cd ..
rm -rf build
mkdir build
cd build
cmake .. && make
```

Problems:

- If the script is called from a different directory than expected, `cd ..` might move to the wrong place.
- Error handling is missing—if a `cd` fails, the script continues in the *old* directory.

Better:

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."

cd "${ROOT_DIR}"
rm -rf build
mkdir build
cd build
cmake .. && make
```

Here we:

- Anchor relative paths to the location of the script (not the caller’s CWD).
- Fail fast if any step breaks.

### 4.2 Relative Paths in CI Without Anchoring

CI configs sometimes use relative paths assuming a particular working directory that isn’t guaranteed:

```yaml
steps:
	- name: Run tests
		run: ./scripts/run-tests.sh
```

If the CI platform changes its default working directory or you move the script, the build breaks.

Safer patterns:

- Explicitly set `working-directory` in the CI step.
- Or have the script compute the repo root relative to its own location.

### 4.3 Mixed Expectations Across Teams

One person runs:

```bash
./scripts/build.sh
```

Another runs:

```bash
cd scripts
./build.sh
```

If `build.sh` assumes one of these, the other path may fail. This leads to "it works for me" inconsistencies.

To avoid this, scripts should be **caller-agnostic**:

- They should not assume where they are invoked from.
- They should anchor themselves to a known directory (script directory or repo root).

### 4.4 Overloading the Project Root

Some projects treat the repo root as a dumping ground:

- Logs written directly into `.`
- Temporary build artifacts cluttering the root
- Tools expecting to run only from root

This creates pressure to always run commands from the root, making it harder to create multi-package or layered builds.

Better approaches:

- Use dedicated `build/`, `dist/`, `logs/`, and `tmp/` directories.
- Reference them via environment variables or config, not hard-coded relative paths.

### 4.5 Security Pitfalls

Careless working-directory use can introduce security issues:

- Running scripts from untrusted directories that contain malicious binaries or scripts (e.g., `./gradlew` in a repo you haven’t audited).
- Using relative include paths in languages like C/C++ that may pick up headers from unintended directories.
- Using `PATH=.:$PATH` and then running commands that may execute from the current directory.

Anchoring paths and avoiding dangerous PATH manipulations reduces these risks.

## 5. Best Practices for Working-Directory-Aware Builds

Let’s turn these pitfalls into patterns.

### 5.1 Make the Working Directory Explicit

In CI and automation:

- Always specify `working-directory` (or the equivalent) for steps.
- Document expected CWD in script headers and CONTRIBUTING docs.

Example (GitHub Actions):

```yaml
steps:
	- uses: actions/checkout@v4
	- name: Install frontend deps
		run: npm ci
		working-directory: frontend

	- name: Run backend tests
		run: npm test
		working-directory: backend
```

### 5.2 Anchor Scripts to Their Own Location

Instead of relying on the caller’s CWD, compute paths relative to the script file:

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}/.."

cd "${REPO_ROOT}"

echo "Repo root: $(pwd)"
```

This pattern makes the script usable whether the user is in the repo root, a subdirectory, or even calling it via an absolute path.

### 5.3 Prefer Absolute Paths in Internal Logic

Where practical:

- Compute absolute paths once (e.g., for the repo root, build directory, cache directory).
- Use those in your script logic, not ad-hoc `../..` chains.

Example:

```bash
BUILD_DIR="${REPO_ROOT}/build"
LOG_DIR="${REPO_ROOT}/logs"

mkdir -p "${BUILD_DIR}" "${LOG_DIR}"

cmake -S "${REPO_ROOT}" -B "${BUILD_DIR}"
cmake --build "${BUILD_DIR}" | tee "${LOG_DIR}/build.log"
```

Even if something `cd`s unexpectedly, your commands still reference the right locations.

### 5.4 Use Tooling Flags Instead of `cd` When Possible

Many tools let you specify a directory explicitly:

- `pytest path/to/tests`
- `npm --prefix frontend test`
- `mvn -f module/pom.xml test`
- `git -C /path/to/repo status`

Using these flags can be clearer than juggling multiple `cd` calls in a script, especially when running commands against multiple directories in one go.

### 5.5 Keep Build Artifacts in Designated Directories

Decide where build outputs belong and enforce it:

- `build/` or `out/` for compiled artifacts
- `dist/` for distributable bundles
- `logs/` for logs, `tmp/` for temporary files

Make sure scripts and tools write there **regardless of the working directory**:

```bash
ARTIFACT_DIR="${REPO_ROOT}/dist"
mkdir -p "${ARTIFACT_DIR}"

cp "${BUILD_DIR}/my-app" "${ARTIFACT_DIR}/"
```

### 5.6 Validate Working-Directory Behavior in Tests

To avoid "mystery failures" later, test commands from multiple directories:

- From the repo root
- From nested package directories
- From outside the repo (for globally installed CLI tools)

If a script fails in some of these contexts, decide whether that’s acceptable. If not, fix the assumptions.

## 6. Diagnosing Working-Directory-Related Build Failures

When something behaves differently in CI than locally, consider the working directory first.

### 6.1 Symptoms to Watch For

- "File not found" errors for configs or test files that *do* exist.
- Tools using a default config instead of your project-specific one.
- Logs showing up in odd directories.
- CI logs referencing paths that don’t match your repo structure.

### 6.2 Debugging Techniques

Add explicit logging early in your scripts and CI steps:

```bash
echo "PWD=$(pwd)"
ls -al
```

In CI, log the workspace layout:

```bash
find . -maxdepth 3 -type d | sort
```

If a tool supports verbose or debug modes, enable them to see which paths and configs it is using.

### 6.3 Reproducing CI Environments Locally

If CI is using `/home/runner/work/project/project`, try to approximate it:

```bash
mkdir -p /tmp/ci-sim
cd /tmp/ci-sim
git clone https://github.com/example/project.git
cd project
"$(cat .ci-script.sh)" # or run the same commands as CI
```

The goal is to narrow down differences in CWD, environment variables, and file layout.

## ✅ Validation and Practice

To cement this knowledge, try a few exercises in a project you care about.

### Exercise 1: Map Your Tooling to Working Directories

1. Pick one project (any language).
2. List the core commands you run (`build`, `test`, `lint`, etc.).
3. For each command, answer:
	 - What is the expected working directory?
	 - Which config files does it load from there?
	 - Where do logs and artifacts go?
4. Document this in your project’s README or CONTRIBUTING guide.

### Exercise 2: Make a Script Caller-Agnostic

1. Find a script that fails if you run it from the "wrong" directory.
2. Refactor it to:
	 - Compute its own directory.
	 - Anchor to repo root or a known base.
	 - Use absolute paths internally.
3. Test it by calling it from:
	 - Repo root
	 - A subdirectory
	 - An absolute path from elsewhere on your system

### Exercise 3: Harden a CI Job Against Directory Changes

1. Find a CI job that uses relative paths without `working-directory`.
2. Add explicit `working-directory` settings or directory-agnostic scripts.
3. Simulate a small repo reorganization (e.g., move a directory) and confirm the job still passes or fails in a predictable way.

## 🚀 Next Steps and Further Learning

Working directories are just one aspect of **build determinism** and **DevOps hygiene**, but mastering them pays off quickly.

- Explore how environment variables (like `PATH`, `NODE_PATH`, `PYTHONPATH`) interact with the working directory.
- Look into tools that help define reproducible environments: Docker, Nix, `direnv`, and language-specific tooling.
- Incorporate working-directory checks into your onboarding docs so new contributors get fewer "it doesn’t work for me" moments.

Every build runs somewhere. Once you treat the working directory as a first-class concept—not an afterthought—you’ll write scripts, builds, and CI pipelines that are far more predictable, portable, and pleasant to work with.
