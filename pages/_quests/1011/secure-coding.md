---
title: 'Secure Coding: Preventing the OWASP Top 10'
author: IT-Journey Team
description: 'Forge code that defeats the OWASP Top 10: master input validation, injection prevention, authentication, secrets handling, and dependency security.'
excerpt: Write secure code that defeats injection, broken access control, weak auth, and leaked secrets
preview: images/previews/secure-coding-practices-owasp-top-10-vulnerability.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1011'
difficulty: 🔴 Hard
estimated_time: 120-150 minutes
primary_technology: security
quest_type: main_quest
quest_series: Security Mastery
quest_line: The Warrior's Bastion
quest_arc: Forging the Hardened Codebase
quest_dependencies:
  required_quests:
  - /quests/1011/security-fundamentals/
  recommended_quests: []
  unlocks_quests:
  - /quests/1011/threat-modeling/
  - /quests/1011/penetration-testing/
skill_focus: security
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Completion of Security Fundamentals (recommended)
  - Comfort writing code in at least one language (examples use Python, JS, SQL)
  - Basic understanding of how web requests and databases interact
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A code editor or IDE (VS Code recommended)
  - A language runtime such as Python 3.10+ or Node.js 18+
  skill_level_indicators:
  - Comfortable building small applications and reading stack traces
  - Ready to refactor insecure code into secure equivalents
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - At least one vulnerable code snippet refactored into a secure version
  skill_demonstrations:
  - Can rewrite a SQL string concatenation as a parameterized query
  - Can hash a password correctly with a modern KDF
  knowledge_checks:
  - Understands the difference between authentication and authorization
  - Can explain why secrets must never be committed to source control
permalink: /quests/1011/secure-coding/
categories:
- Quests
- Security
- Hard
tags:
- '1011'
- security
- main_quest
- owasp
- input-validation
- hands-on
- gamified-learning
keywords:
  primary:
  - '1011'
  - security
  - main_quest
  secondary:
  - secure-coding
  - injection-prevention
  - dependency-security
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1011 (11) Quest: Main Quest - Secure Coding'
rewards:
  badges:
  - 🏆 Codesmith of the Bastion - Forged code that resists the OWASP Top 10
  - 🛡️ Injection Slayer - Eliminated injection at the source
  skills_unlocked:
  - 🛠️ Parameterized Queries & Output Encoding
  - 🔐 Secure Secrets and Credential Handling
  progression_points: 100
  unlocks_features:
  - Ability to harden real applications against common web attacks
layout: quest
---
*Greetings, brave adventurer! Having sworn the oath of the Bastion in **Security Fundamentals**, you now descend into the forge. Here, abstract principles become hardened steel: real code that input validation tempers, parameterized queries shield, and strong cryptography seals. This quest, **Secure Coding Practices**, turns you from someone who knows the OWASP Top 10 by name into someone who defeats it line by line.*

*Whether you write your first login form this week or maintain a sprawling production service, the patterns you forge here are the same: trust no input, separate code from data, prove identity before granting power, and never let a secret escape into the daylight.*

## 📖 The Legend Behind This Quest

*The greatest breaches in the chronicles were rarely caused by exotic magic. They were caused by a missing `?` placeholder, a password stored in plaintext, an API key committed to a public repository, or a dependency left to rot with a known curse (a CVE). The defenders who endured learned that secure code is not about cleverness - it is about discipline applied consistently, everywhere.*

*This quest teaches the handful of habits that prevent the overwhelming majority of real-world vulnerabilities.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Input Validation & Output Encoding** - Treat all external input as hostile and neutralize it
- [ ] **Injection Prevention** - Defeat SQL injection, command injection, and XSS at the source
- [ ] **Authentication & Authorization** - Verify identity with strong hashing and enforce least-privilege access
- [ ] **Secrets Handling** - Keep credentials out of source control and inject them safely at runtime
- [ ] **Dependency Security** - Find and remediate vulnerable third-party libraries

### Secondary Objectives (Bonus Achievements)
- [ ] **Secure Session Management** - Harden cookies and tokens against theft
- [ ] **Security Headers** - Apply CSP, HSTS, and friends to shrink the attack surface
- [ ] **Automated Scanning** - Wire SAST and dependency scanning into your workflow

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Refactor a string-concatenated query into a parameterized one from memory
- [ ] Explain why `bcrypt`/`argon2` beats a raw SHA-256 for passwords
- [ ] Move a hard-coded secret into an environment variable or vault
- [ ] Run a dependency scan and interpret the results

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Completion of [Security Fundamentals](/quests/1011/security-fundamentals/) (recommended)
- [ ] Ability to read and write code in at least one language
- [ ] Basic understanding of HTTP requests, databases, and HTML

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A code editor or IDE (VS Code recommended)
- [ ] Python 3.10+ or Node.js 18+ installed

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can build and run a small application
- [ ] You are comfortable refactoring existing code
- [ ] Ready for 120-150 minutes of focused, hands-on work

## 🌍 Choose Your Adventure Platform

*The secure-coding patterns are language-agnostic. Set up a runtime so you can run the examples.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Python toolchain plus a couple of security tools
brew install python node
python3 -m pip install --upgrade pip bcrypt bandit pip-audit
python3 --version
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install Python.Python.3.12 OpenJS.NodeJS
py -3 -m pip install --upgrade pip bcrypt bandit pip-audit
py -3 --version
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y python3-pip nodejs npm   # Debian/Ubuntu
python3 -m pip install --upgrade pip bcrypt bandit pip-audit
python3 --version
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Any container or Codespace with Python works
# (no -it: this runs non-interactively in scripts/CI without a TTY)
docker run --rm python:3.12-slim bash -lc \
  "pip install bcrypt bandit pip-audit && python --version"
```

</details>

## 🧙‍♂️ Chapter 1: Trust No Input - Validation, Encoding, and Injection

*Nearly every injection flaw shares one root cause: untrusted input is allowed to change the structure of a command. The cure is to keep **data** and **code** strictly separated.*

### ⚔️ Skills You'll Forge in This Chapter
- Allowlist input validation
- Parameterized queries to kill SQL injection
- Safe subprocess invocation to kill command injection
- Output encoding to kill cross-site scripting (XSS)

### 🏗️ SQL Injection - The Cardinal Sin

```python
# ❌ VULNERABLE: user input is concatenated into the SQL string.
# Input  "' OR '1'='1"  turns this query into "always true".
username = request.args["username"]
cursor.execute("SELECT * FROM users WHERE name = '" + username + "'")

# ✅ SECURE: a parameterized query. The driver sends the SQL and the
# values separately, so input can never alter the query's structure.
cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
```

The same rule holds in every language - use bound parameters, an ORM, or prepared statements. Never build SQL by string-joining user input.

### 🏗️ Command Injection - Don't Hand the Shell to Strangers

```python
import subprocess

# ❌ VULNERABLE: shell=True with interpolated input.
# Input "report.txt; rm -rf /" runs a second command.
subprocess.run(f"cat {filename}", shell=True)

# ✅ SECURE: pass an argument list, no shell. The filename can never
# be parsed as additional commands.
subprocess.run(["cat", filename])
```

### 🏗️ Cross-Site Scripting (XSS) - Encode on Output

```javascript
// ❌ VULNERABLE: raw user content injected into the DOM.
element.innerHTML = userComment; // <script>...</script> executes

// ✅ SECURE: treat it as text, not markup. The browser will not run it.
element.textContent = userComment;
```

For server-rendered HTML, rely on a template engine with **auto-escaping enabled** (Jinja2, ERB, Razor) and add a Content-Security-Policy header as a second layer.

### 🏗️ Allowlist Validation

```python
import re

# ✅ Validate against a strict allowlist, reject everything else.
def validate_account_id(value: str) -> str:
    if not re.fullmatch(r"[A-Z]{2}\d{6}", value):
        raise ValueError("invalid account id")
    return value
```

Prefer allowlists ("only these are valid") over denylists ("block these bad ones") - attackers are endlessly creative at evading denylists.

### 🔍 Knowledge Check: Injection
- [ ] Why does a parameterized query stop SQL injection where escaping might not?
- [ ] What makes `shell=True` dangerous?
- [ ] Why is output encoding the right defense against XSS rather than input filtering alone?

## 🧙‍♂️ Chapter 2: Authentication, Authorization, and Sessions

*Authentication asks "who are you?"; authorization asks "what are you allowed to do?". Confusing or skipping either is the heart of OWASP A01 and A07.*

### ⚔️ Skills You'll Forge in This Chapter
- Hashing passwords with a modern key-derivation function
- Enforcing authorization on every sensitive action
- Hardening sessions and tokens

### 🏗️ Store Passwords Correctly

```python
import bcrypt

# ❌ NEVER store plaintext, and don't use plain SHA-256/MD5 — they are
# too fast and trivially brute-forced.

# ✅ Use a slow, salted, adaptive hash (bcrypt, scrypt, or argon2id).
def hash_password(plaintext: str) -> bytes:
    return bcrypt.hashpw(plaintext.encode(), bcrypt.gensalt(rounds=12))

def verify_password(plaintext: str, stored_hash: bytes) -> bool:
    return bcrypt.checkpw(plaintext.encode(), stored_hash)
```

bcrypt salts automatically and is deliberately slow, which makes offline cracking expensive. Pair it with multi-factor authentication for high-value accounts.

### 🏗️ Enforce Authorization Server-Side

```python
# ❌ Broken Access Control (OWASP A01): trusting a client-supplied id.
@app.get("/invoices/<invoice_id>")
def get_invoice(invoice_id):
    return db.get_invoice(invoice_id)  # any user can read any invoice!

# ✅ Always check that the CURRENT user owns the resource.
@app.get("/invoices/<invoice_id>")
@login_required
def get_invoice(invoice_id):
    invoice = db.get_invoice(invoice_id)
    if invoice.owner_id != current_user.id:
        abort(403)
    return invoice
```

Authorization must be enforced on the server for **every** request. Never rely on hiding a button in the UI.

### 🏗️ Harden Sessions

- Set cookies with `HttpOnly` (block JS access), `Secure` (HTTPS only), and `SameSite=Lax/Strict` (mitigate CSRF).
- Rotate the session id on login to prevent session fixation.
- Give tokens a short lifetime and support revocation.

### 🔍 Knowledge Check: AuthN/AuthZ
- [ ] Why is bcrypt preferable to SHA-256 for passwords?
- [ ] Where must authorization checks live, and why never the client?
- [ ] What does the `HttpOnly` cookie flag defend against?

## 🧙‍♂️ Chapter 3: Secrets and the Supply Chain

*The last two great weaknesses are leaked secrets and rotten dependencies. Both are mundane, both are devastating, and both are preventable with tooling.*

### ⚔️ Skills You'll Forge in This Chapter
- Keeping secrets out of source control
- Scanning dependencies for known vulnerabilities
- Running static analysis on your own code

### 🏗️ Never Commit Secrets

```python
# ❌ VULNERABLE: a hard-coded credential. Once committed, it lives in
# git history forever, even if you delete the line later.
API_KEY = "sk_live_51H8xQ2eZvKYlo2C..."

# ✅ SECURE: read from the environment (or a secrets manager).
import os
API_KEY = os.environ["API_KEY"]
```

```bash
# Add an ignore rule so secret files never get staged
echo ".env" >> .gitignore

# Scan a repository for accidentally committed secrets before pushing
pip install detect-secrets

# detect-secrets scans files tracked by git (via `git ls-files`). Outside a git
# repo it silently scans nothing and produces a clean-looking baseline, so make
# sure your files are in git first.
git init -q
git add .
detect-secrets scan > .secrets.baseline
```

If a secret ever lands in git history, treat it as compromised: **rotate it immediately**, do not just delete the line.

### 🏗️ Audit Your Dependencies

```bash
# Python: list dependencies with known CVEs
pip-audit

# Node.js: the same idea for npm
npm audit
npm audit fix

# Apply only safe, non-breaking fixes; review the rest manually.
```

Pin versions, keep a lockfile in source control, and enable automated update PRs (e.g., Dependabot or Renovate).

### 🏗️ Static Analysis (SAST)

```bash
# Bandit finds common security anti-patterns in Python source
bandit -r ./src

# Wire it into CI so insecure patterns fail the build
bandit -r ./src --severity-level medium
```

### 🔍 Knowledge Check: Secrets & Supply Chain
- [ ] Why is deleting a committed secret insufficient?
- [ ] What does `pip-audit` / `npm audit` actually check?
- [ ] What is the difference between SAST and a dependency scan?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Parameterize a Query
**Objective**: Take a vulnerable string-concatenated SQL query and refactor it to use bound parameters.

**Requirements**:
- [ ] Identify the injection point
- [ ] Rewrite with parameter binding
- [ ] Confirm the input `' OR '1'='1` no longer changes the result

**Validation**: Run `bandit -r .` and confirm the SQL warning disappears.

### 🟡 Intermediate Challenge: Build a Secure Login
**Objective**: Implement registration and login that hashes passwords with bcrypt and reads its secret from the environment.

**Requirements**:
- [ ] Passwords stored only as bcrypt hashes
- [ ] No secret hard-coded in source
- [ ] Authorization check on a protected route
- [ ] Cookies set `HttpOnly`, `Secure`, `SameSite`

**Validation**: `detect-secrets scan` reports no secrets; the protected route returns 403 for the wrong user.

### 🔴 Advanced Challenge: Harden a Real Repo
**Objective**: Take an existing small project and run a full pass: secrets scan, dependency audit, and SAST.

**Requirements**:
- [ ] Remediate at least one finding from each tool
- [ ] Add a CI step that runs all three
- [ ] Document the before/after

**Validation**: The CI job fails on a planted vulnerability and passes once fixed.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Codesmith of the Bastion** - You forge code that resists the OWASP Top 10
- 🛡️ **Injection Slayer** - You eliminate injection at the source

**🛠️ Skills Unlocked**:
- **Parameterized Queries & Output Encoding** - Structural defenses against injection
- **Secure Secrets and Credential Handling** - Keep keys out of the codebase

**🔓 Unlocked Quests**:
- Threat Modeling - Find these flaws systematically before you write the code
- Penetration Testing - Verify your defenses by attacking them ethically

**📊 Progression Points**: +100 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Threat Modeling](/quests/1011/threat-modeling/) - Design out whole classes of bugs

**Explore Side Adventures**:
- ⚔️ [Penetration Testing](/quests/1011/penetration-testing/) - Attack your own work
- ⚔️ [Compliance Standards](/quests/1011/compliance-standards/) - Prove your controls to auditors

### Character Class Recommendations

**💻 Software Developer**: Continue to [Threat Modeling](/quests/1011/threat-modeling/)  
**🏗️ System Engineer**: Explore [Compliance Standards](/quests/1011/compliance-standards/)  
**🛡️ Security Specialist**: Advance to [Penetration Testing](/quests/1011/penetration-testing/)

## 📚 Resources

### Official Documentation
- [OWASP Top 10 (2021)](https://owasp.org/www-project-top-ten/) - The risk categories you are defending against
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) - Per-topic secure-coding guidance
- [OWASP Proactive Controls](https://owasp.org/www-project-proactive-controls/) - The defensive techniques developers should apply

### Community Resources
- [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/)

### Tools & Utilities
- [Bandit](https://bandit.readthedocs.io/) - Python static analysis for security
- [pip-audit](https://pypi.org/project/pip-audit/) and [npm audit](https://docs.npmjs.com/cli/v10/commands/npm-audit) - Dependency vulnerability scanners
- [detect-secrets](https://github.com/Yelp/detect-secrets) - Catch secrets before they are committed

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Refactored at least one vulnerable snippet into a secure version
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1011 - Security & Compliance]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Prerequisites:** [[Security Fundamentals: CIA Triad and Defense in Depth Strategies]] **Unlocks:** [[Threat Modeling: STRIDE Framework and Attack Trees Analysis]] · [[Penetration Testing: Tools and Ethical Hacking Methodologies]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
