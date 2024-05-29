import re

issue_title = "${{ github.event.issue.title }}"
issue_body = "${{ github.event.issue.body }}"
issue_number = "${{ github.event.issue.number }}"
repo_url = "https://github.com/${{ github.repository }}/issues/"

# Read the markdown file
with open("it-journey/pages/_about/features/index.md", "r") as file:
    lines = file.readlines()

# Find the line number of the "Requested features" header
header_line = next(i for i, line in enumerate(lines) if "Requested features" in line)

# Find the line number of the next header (or the end of the file)
next_header_line = next((i for i, line in enumerate(lines[header_line+1:], start=header_line+1) if re.match(r"^## ", line)), len(lines))

# Insert the new feature request before the next header
lines.insert(next_header_line, f"| {issue_title} | {issue_body} | [{issue_number}]({repo_url}{issue_number}) |\n")

# Write the modified lines back to the file
with open("it-journey/pages/_about/features/index.md", "w") as file:
    file.writelines(lines)