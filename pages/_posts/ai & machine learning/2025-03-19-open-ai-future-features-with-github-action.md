---
title: Open AI Future Features with Github Action
description: Automate GitHub Issues with OpenAI and GitHub Actions for structured feature requests and bug reports. Enhance your workflow effortlessly!
date: 2025-03-19T20:11:12.776Z
preview: ""
tags: []
categories: []
sub-title: null
excerpt: null
snippet: null
author: ""
layout: null
keywords: {}
lastmod: 2025-07-04T23:01:15.321Z
permalink: null
attachments: ""
comments: false
section: AI & Machine Learning
---

Here's a complete, detailed, and comprehensive **step-by-step tutorial** to implement automated, AI-driven structured GitHub Issues (**feature requests**, **bug reports**, **test plans**, etc.) using **GitHub Actions** and **OpenAI's GPT-4 API** for **any GitHub repository**.

* * * *

**📚 Tutorial: Automate Structured GitHub Issues with OpenAI & GitHub Actions**

This tutorial sets up a streamlined system where:

- Users create a new GitHub Issue (e.g., Feature or Bug).

- GitHub Actions automatically triggers, calls OpenAI's GPT-4 API.

- OpenAI generates structured sub-issues (e.g., Functional Requirements or Test Plans).

* * * *

**✅ 1. Prerequisites:**

- A **GitHub repository** (public or private).

- An **OpenAI account** ([openai.com](https://openai.com)) with API access.

* * * *

**✅ 2. Set Up OpenAI API Key:**

- Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

- Click **"Create new secret key"**.

- Copy your API Key immediately (you'll need it soon).

* * * *

**✅ 3. Configure GitHub Repository Secrets:**

- On your GitHub repo, go to:

```
Settings → Secrets and variables → Actions
```

- Click **"New repository secret"**:

- Name: OPENAI\_API\_KEY

- Paste the OpenAI key.

*Repeat if needed:*

- Add optional secret: OPENAI\_ORG\_ID (if multiple OpenAI organizations).

* * * *

**✅ 4. Repository Structure (Recommended):**

Create or verify your structure:

```
my-repo/
├── .github/
│   ├── workflows/
│   │   └── openai-issue-processing.yml
│   └── ISSUE_TEMPLATE/
│       ├── feature_request_generic.md
│       ├── feature_functional_requirements.md
│       ├── bug_report_generic.md
│       └── bug_test_plan.md
└── openai/
    ├── create_sub_issue.py
    ├── requirements.txt
    └── README.md
```

* * * *

**✅ 5. Define GitHub Issue Templates:**

**Example Generic Feature Template (feature\_request\_generic.md):**

```
---
name: Feature Request
about: Request a new feature
title: "[Feature Request]: "
labels: feature-request
---


## Feature Description
*(Clearly describe your desired feature here.)*
```

**Example Structured Sub-Issue Template (feature\_functional\_requirements.md):**

```
---
name: Feature Functional Requirements
about: AI-generated functional requirements
title: "[Functional Requirements]: "
labels: functional-requirements
prompt: |
  Generate structured functional requirements based on the original feature request provided.
---

## Overview of the Feature

## Functional Specifications
1.
2.
3.

## Acceptance Criteria
- Criteria 1:
- Criteria 2:

## Dependencies

## Risks & Mitigations
- Risk:
  Mitigation:
```

**(Repeat similarly for bugs and test plans)**

* * * *

**✅ 6. Create the GitHub Actions Workflow:**

Create .github/workflows/openai-issue-processing.yml:

```
name: OpenAI Unified Issue Processing

on:
  issues:
    types: [opened]

permissions:
  issues: write

jobs:
  process-issue:
    runs-on: ubuntu-latest
    env:
      GITHUB_TOKEN: ${{ secrets.PAT_TOKEN }}
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      OPENAI_ORG_ID: ${{ secrets.OPENAI_ORG_ID }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r openai/requirements.txt
      - name: Process Issue via OpenAI
        run: |
          python openai/create_sub_issue.py\
            --repo "${{ github.repository }}"\
            --parent-issue-number "${{ github.event.issue.number }}"
```

* * * *

**✅ 7. Create Python Script (openai/create\_sub\_issue.py):**

```
import os, requests, argparse, yaml, re
from openai import OpenAI

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def fetch_issue(repo, number):
    res = requests.get(f"https://api.github.com/repos/{repo}/issues/{number}", headers=HEADERS)
    res.raise_for_status()
    return res.json()

def extract_template(issue_body):
    match = re.search(r'', issue_body)
    if match:
        return match.group(1).strip()
    raise Exception("Template not found.")

def load_template(name):
    with open(f".github/ISSUE_TEMPLATE/{name}") as f:
        content = f.read()
    front_matter = re.search(r'^---(.*?)---', content, re.DOTALL)
    yaml_content = yaml.safe_load(front_matter.group(1))
    return (
        yaml_content['prompt'].strip(),
        content[front_matter.end():].strip(),
        yaml_content.get('title', '[Structured]: ')
    )

def call_openai(prompt, issue_content, structure):
    full_prompt = f"{prompt}\n\nIssue:\n{issue_content}\n\nStructure:\n{structure}"
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.2,
        max_tokens=2500
    )
    return response.choices[0].message.content.strip()

def create_sub_issue(repo, title, body, parent):
    res = requests.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers=HEADERS,
        json={"title": title, "body": body+f"\n\n_Parent Issue: #{parent}_", "labels":["ai-generated"]}
    )
    res.raise_for_status()
    return res.json()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--parent-issue-number", required=True)
    args = parser.parse_args()

    issue = fetch_issue(args.repo, args.parent_issue_number)
    template = extract_template(issue['body'])
    prompt, structure, prefix = load_template(template)

    content = call_openai(prompt, issue['body'], structure)
    sub_issue = create_sub_issue(args.repo, prefix+issue['title'], content, args.parent_issue_number)

    print(f"Created: {sub_issue['html_url']}")

if __name__ == "__main__":
    main()
```

* * * *

**✅ 8. Python Dependencies (openai/requirements.txt):**

```
requests
openai>=1.0.0
pyyaml
```

* * * *

**✅ 9. Push Changes & Test:**

- Commit all files and push to GitHub.

- Create a new issue using your **generic template**.

- GitHub Actions will automatically create a structured sub-issue.

* * * *

**✅ 10. Common Issues & Solutions:**

- **403 Forbidden Error:**

Set workflow permissions explicitly in YAML (permissions: issues: write).

- **OpenAI API Error:**

Confirm API key is correct and has sufficient balance/permissions.

* * * *

**🔑 Security & Maintenance Tips:**

- Rotate your OpenAI keys regularly.

- Avoid committing keys or sensitive info directly into source control.

- Regularly update OpenAI libraries and dependencies.

* * * *

🎉 **You're Done!** Now your GitHub repository has powerful automation for structured, high-quality issues leveraging AI, enhancing developer productivity and project clarity.

If you run into any issues, feel free to reach out!