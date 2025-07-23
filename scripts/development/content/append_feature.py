import os
import re

# Use os.getenv to get the environment variables
issue_title = os.getenv("ISSUE_TITLE")
issue_number = os.getenv("ISSUE_NUMBER")
repo_url = os.getenv("REPO_URL")

# Construct the absolute path to the markdown file
file_path = os.path.join(os.getenv("GITHUB_WORKSPACE"), "pages/_about/features/index.md")

# Read the markdown file
with open(file_path, "r") as file:
    lines = file.readlines()

# Remove trailing empty lines
while lines[-1].strip() == '':
    lines.pop()

# Find the line number of the "Requested features" header
header_line = next(i for i, line in enumerate(lines) if "Requested features" in line)

# Find the line number of the next header (or the end of the file)
next_header_line = next((i for i, line in enumerate(lines[header_line+1:], start=header_line+1) if re.match(r"^## ", line)), len(lines))

# Insert the new feature request and a blank line before the next header
lines.insert(next_header_line, f"{issue_title} - FR{issue_number} | [{issue_number}]({repo_url}{issue_number})\n\n")

# Write the updated content back to the markdown file
with open(file_path, "w") as file:
    file.writelines(lines)