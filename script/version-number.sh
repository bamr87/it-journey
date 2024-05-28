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