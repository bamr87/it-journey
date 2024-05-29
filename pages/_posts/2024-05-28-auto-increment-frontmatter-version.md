---
title: Auto Increment Frontmatter Version
description: How to automatically increment the version number in the frontmatter of a markdown file after every commit.
date: 2024-05-28T21:36:50.132Z
preview: null
draft: true
tags:
    - git
categories: []
sub-title: null
excerpt: null
snippet: null
author: bamr87
layout: null
keywords: {}
lastmod: 2024-05-28T21:40:13.289Z
slug: null
permalink: null
attachments: ""
type: posts
---

bamr87: how can i automatically increment this version frontmatter after every commit? in other words, whenever i commit changes, i want the version number to be the next increment from the last commit of this file

GitHub Copilot: You can achieve this by using a Git hook. Git hooks are scripts that Git executes before or after events such as `commit`, `push`, and so on. In your case, you can use a `pre-commit` hook to increment the version number in your markdown file.

Here's a step-by-step plan:

1. Create a bash script that will increment the version number in your markdown file.
2. Set this script as a `pre-commit` hook.

Here's the bash script:

```bash
#!/bin/bash

# Get the current version from the markdown file
current_version=$(grep -oP 'version: \K.*' zer0.md)

# Split the version into an array
IFS='.' read -ra version_parts <<< "$current_version"

# Increment the last part of the version
version_parts[-1]=$((version_parts[-1] + 1))

# Join the version parts back together
new_version=$(IFS=. ; echo "${version_parts[*]}")

# Replace the version in the markdown file
sed -i '' -e "s/version: $current_version/version: $new_version/g" zer0.md

# Add the updated file to the commit
git add zer0.md
```

To set this script as a `pre-commit` hook, follow these steps:

1. Save the script in a file named `pre-commit` in your `.git/hooks` directory.
2. Make the script executable by running `chmod +x .git/hooks/pre-commit`.

Now, every time you commit, the version number in your markdown file will be incremented.

bamr87: this is too complicated. try again

GitHub Copilot: I understand. Let's simplify this. We'll use a Python script for the `pre-commit` hook instead of a bash script. This script will increment the version number by 0.1 each time a commit is made.

Here's the Python script:

```python
import re

# Open the markdown file
with open('zer0.md', 'r+') as f:
    content = f.read()

    # Find the version number
    version = re.search(r'version: (\d+\.\d+)', content).group(1)

    # Increment the version number
    new_version = str(float(version) + 0.1)

    # Replace the old version number with the new one
    content = content.replace(f'version: {version}', f'version: {new_version}')

    # Write the new content back to the file
    f.seek(0)
    f.write(content)
    f.truncate()

# Add the updated file to the commit
git add zer0.md
```

To set this script as a `pre-commit` hook, follow these steps:

1. Save the script in a file named `pre-commit` in your `.git/hooks` directory.
2. Make the script executable by running `chmod +x .git/hooks/pre-commit`.

Now, every time you commit, the version number in your markdown file will be incremented by 0.1.

bamr87: this script should work on only the files being staged during commit. this should also narrow the scope to only the front matter.

GitHub Copilot: You're right. The script should only affect the files being staged for commit. We can modify the script to loop over the staged files and only process the ones that are markdown files. We'll also narrow the scope to only the front matter.

Here's the updated script:

```bash
#!/bin/bash

# Get the staged files
staged_files=$(git diff --cached --name-only)

# Loop over the staged files
for file in $staged_files; do
    # Only process markdown files
    if [[ $file == *.md ]]; then
        # Get the front matter
        front_matter=$(sed -n '/---/,/---/p' $file)

        # Get the current version from the front matter
        current_version=$(echo "$front_matter" | grep -oP 'version: \K.*')

        # If a version was found
        if [[ $current_version ]]; then
            # Split the version into an array
            IFS='.' read -ra version_parts <<< "$current_version"

            # Increment the last part of the version
            version_parts[-1]=$((version_parts[-1] + 1))

            # Join the version parts back together
            new_version=$(IFS=. ; echo "${version_parts[*]}")

            # Replace the version in the front matter
            sed -i '' -e "/---/,/---/ s/version: $current_version/version: $new_version/" $file

            # Add the updated file to the commit
            git add $file
        fi
    fi
done
```

This script will only increment the version number in the front matter of the markdown files being staged for commit.

bamr87: how would this work with the vscode extention for source control?

GitHub Copilot: The Git hooks work at the Git level, so they are independent of the client you're using to interact with Git. This means that the hooks will work whether you're using the command line, VS Code, or any other Git client.

When you stage and commit changes using the Source Control extension in VS Code, it's essentially doing the same thing as running `git add` and `git commit` in the terminal. So, the `pre-commit` hook will still be triggered.

Here's how you can set it up:

1. Save the script in a file named `pre-commit` in your `.git/hooks` directory.
2. Make the script executable by running `chmod +x .git/hooks/pre-commit` in the terminal.

Now, every time you commit changes using the Source Control extension in VS Code, the `pre-commit` hook will be triggered, and the version number in your markdown file will be incremented.

bamr87: does the bash file require an extension?

GitHub Copilot: No, Bash script files do not require an extension. In fact, it's common for Bash scripts used as Git hooks (like `pre-commit`) to not have any extension. The important part is that the file has the correct permissions to be executable. This can be set with the command `chmod +x filename`, where `filename` is the name of your script.

bamr87: it didn't work

GitHub Copilot: I apologize for the inconvenience. Let's try to debug the issue.

The script you posted should work as expected, but there might be some issues related to your specific setup. Here are a few things you can check:

1. Make sure the `pre-commit` file is in the correct location. It should be in the `.git/hooks` directory at the root of your repository.

2. Ensure the `pre-commit` file is executable. You can do this by running `chmod +x .git/hooks/pre-commit` in the terminal.

3. Check if the `pre-commit` hook is being triggered at all. You can do this by adding a line like `echo "pre-commit hook triggered"` at the beginning of your script. Then, when you make a commit, you should see this message in the terminal.

4. Make sure the `pre-commit` script is correctly getting the list of staged files. You can check this by adding a line like `echo "Staged files: $staged_files"` after the `staged_files=$(git diff --cached --name-only)` line.

5. Check if the script is correctly finding and incrementing the version number. You can do this by adding `echo` statements in the relevant parts of the script.

If you're still having issues after checking these things, please provide more details about what's not working, and I'll do my best to help you troubleshoot the issue.

bamr87: is this format for the version number in the front matter correct?

GitHub Copilot: Yes, the format for the version number in the front matter of your markdown file is correct. The version number is typically represented as `MAJOR.MINOR.PATCH`, where:

- `MAJOR` version when you make incompatible API changes,
- `MINOR` version when you add functionality in a backwards-compatible manner, and
- `PATCH` version when you make backwards-compatible bug fixes.

This is in line with the Semantic Versioning specification. In your case, `0.0.0` is a valid version number, representing the initial development phase.

bamr87: here;s the error: 2024-05-28 15:29:46.407 [info] pre-commit hook triggered
grep: invalid option -- P
usage: grep [-abcdDEFGHhIiJLlMmnOopqRSsUVvwXxZz] [-A num] [-B num] [-C[num]]
	[-e pattern] [-f file] [--binary-files=value] [--color=when]
	[--context[=num]] [--directories=action] [--label] [--line-buffered]
	[--null] [pattern] [file ...]

GitHub Copilot: The error message indicates that the `grep` command in your script is using an invalid option `-P`. The `-P` option is used in `grep` to interpret the pattern as a Perl regular expression. This option is not supported in all implementations of `grep`, including the one on macOS.

We can replace the `grep` command with a `sed` command to extract the version number. Here's the updated script:

```bash
#!/bin/bash

# Get the staged files
staged_files=$(git diff --cached --name-only)

# Loop over the staged files
for file in $staged_files; do
    # Only process markdown files
    if [[ $file == *.md ]]; then
        # Get the front matter
        front_matter=$(sed -n '/---/,/---/p' $file)

        # Get the current version from the front matter
        current_version=$(echo "$front_matter" | sed -n 's/version: \([0-9]*\.[0-9]*\.[0-9]*\)/\1/p')

        # If a version was found
        if [[ $current_version ]]; then
            # Split the version into an array
            IFS='.' read -ra version_parts <<< "$current_version"

            # Increment the last part of the version
            version_parts[-1]=$((version_parts[-1] + 1))

            # Join the version parts back together
            new_version=$(IFS=. ; echo "${version_parts[*]}")

            # Replace the version in the front matter
            sed -i '' -e "/---/,/---/ s/version: $current_version/version: $new_version/" $file

            # Add the updated file to the commit
            git add $file
        fi
    fi
done
```

This script should work on macOS and increment the version number in the front matter of your markdown files.

bamr87: now i'm getting this error: .git/hooks/pre-commit: line 25: version_parts: bad array subscript
.git/hooks/pre-commit: line 25: version_parts[-1]: bad array subscript


GitHub Copilot: The error message indicates that the array subscript is not working as expected. This is likely because the version of Bash you're using does not support negative array indices. Negative array indices (like `-1` for the last element) are a feature of Bash 4.0 and later, but macOS ships with Bash 3.2 for licensing reasons.

We can modify the script to work with Bash 3.2 by using `${#array[@]}` to get the length of the array and then subtracting 1 to get the index of the last element.

Here's the updated script:

```bash
#!/bin/bash

# Get the staged files
staged_files=$(git diff --cached --name-only)

# Loop over the staged files
for file in $staged_files; do
    # Only process markdown files
    if [[ $file == *.md ]]; then
        # Get the front matter
        front_matter=$(sed -n '/---/,/---/p' $file)

        # Get the current version from the front matter
        current_version=$(echo "$front_matter" | sed -n 's/version: \([0-9]*\.[0-9]*\.[0-9]*\)/\1/p')

        # If a version was found
        if [[ $current_version ]]; then
            # Split the version into an array
            IFS='.' read -ra version_parts <<< "$current_version"

            # Increment the last part of the version
            last_index=$((${#version_parts[@]}-1))
            version_parts[$last_index]=$((${version_parts[$last_index]} + 1))

            # Join the version parts back together
            new_version=$(IFS=. ; echo "${version_parts[*]}")

            # Replace the version in the front matter
            sed -i '' -e "/---/,/---/ s/version: $current_version/version: $new_version/" $file

            # Add the updated file to the commit
            git add $file
        fi
    fi
done
```

This script should work on macOS and increment the version number in the front matter of your markdown files.