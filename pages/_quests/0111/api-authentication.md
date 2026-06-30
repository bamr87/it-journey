---
title: 'API Authentication: Keys, Tokens, OAuth2, and JWT'
author: IT-Journey Team
description: Master API authentication including API keys, sessions versus tokens, JSON Web Tokens, OAuth2 flows, and scopes so you can secure and consume protected APIs.
excerpt: Learn API keys, sessions vs tokens, JWT, OAuth2 flows, and scopes for securing APIs
preview: images/previews/api-authentication-keys-tokens-oauth2-jwt.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0111'
difficulty: 🔴 Hard
estimated_time: 90-120 minutes
primary_technology: oauth2
quest_type: main_quest
quest_series: API Design Mastery
quest_line: The Gatekeeper's Road
quest_arc: Guardians of the Interface
quest_dependencies:
  required_quests:
  - /quests/0111/api-fundamentals/
  recommended_quests:
  - /quests/0111/rest-principles/
  unlocks_quests:
  - /quests/0111/error-handling/
  - /quests/0111/rate-limiting/
skill_focus: security
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Completion of API Fundamentals (HTTP headers, status codes)
  - Comfort making requests with curl
  - Awareness of what HTTPS protects
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - curl installed
  - Optional Python 3 with the PyJWT library for the token lab
  skill_level_indicators:
  - You can read and set HTTP headers
  - You are ready to reason about who can do what
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - Authenticated against a real API using a token in a header
  skill_demonstrations:
  - Can explain the difference between authentication and authorization
  - Can describe the OAuth2 authorization code flow step by step
  knowledge_checks:
  - Understands the structure of a JWT and what it does and does not protect
  - Can explain why tokens beat server sessions for APIs
permalink: /quests/0111/api-authentication/
categories:
- Quests
- Security
- Hard
tags:
- '0111'
- oauth2
- main_quest
- security
- hands-on
- gamified-learning
keywords:
  primary:
  - '0111'
  - oauth2
  - main_quest
  secondary:
  - jwt
  - api-keys
  - scopes
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0111 (7) Quest: Main Quest - API Authentication'
rewards:
  badges:
  - 🏆 Keeper of the Keys - Authenticated against a protected API
  - 🛡️ Token Warden - Can read and reason about JWTs and OAuth2 flows
  skills_unlocked:
  - 🛠️ Token-Based Authentication
  - 🧠 OAuth2 Flow Selection
  progression_points: 75
  unlocks_features:
  - Access to the Error Handling and Rate Limiting quests
layout: quest
---
*Greetings, brave adventurer! Every gate worth guarding needs a guardian. An API that anyone can call without identifying themselves is a treasury with its doors flung open. This quest, **API Authentication**, teaches you to prove who you are when you call an API - and to demand proof when you build one.*

*You will wield API keys, understand why tokens defeated server sessions in the API era, dissect a JSON Web Token by hand, and walk the full OAuth2 authorization code dance that powers "Log in with Google." Master this, and no protected endpoint can turn you away.*

## 📖 The Legend Behind This Quest

*Authentication asks "who are you?"; authorization asks "what may you do?" In the early web, servers answered both by remembering you - a session stored in server memory, a cookie in your browser. But APIs are called by phones, scripts, other servers, and third parties, often across organizations. Storing every caller's session on one server does not scale and does not federate.*

*The answer was the **bearer token**: a self-contained credential the client carries and presents on every request. Whoever bears the token is granted its access - which is exactly why tokens must travel only over HTTPS and must expire. This quest teaches you to use them safely.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Authentication vs Authorization** - Distinguish "who you are" from "what you may do"
- [ ] **API Keys** - Use and protect a static API key, and know its limits
- [ ] **Sessions vs Tokens** - Explain why stateless tokens won for APIs
- [ ] **JSON Web Tokens** - Read a JWT's three parts and understand its signature
- [ ] **OAuth2 and Scopes** - Walk the authorization code flow and grant least-privilege scopes

### Secondary Objectives (Bonus Achievements)
- [ ] **Refresh Tokens** - Trade a short-lived access token for a fresh one without re-login
- [ ] **PKCE** - Understand why public clients need Proof Key for Code Exchange
- [ ] **Token Storage** - Reason about where it is safe to keep a token

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Authenticate to a real API using a bearer token in an `Authorization` header
- [ ] Decode a JWT and explain what its signature does and does not guarantee
- [ ] Draw the OAuth2 authorization code flow from memory
- [ ] Choose the right scopes for an integration and justify the minimum

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] You have completed API Fundamentals or know HTTP headers and status codes
- [ ] You can set headers on a curl request
- [ ] You understand that HTTPS encrypts traffic in transit

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] `curl` available in your terminal
- [ ] Optional: Python 3 with `PyJWT` for the token lab
- [ ] An internet connection

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You are comfortable with HTTP headers and JSON
- [ ] You are ready to reason carefully about security trade-offs
- [ ] Ready for 90-120 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*Authentication concepts are universal. These setups give you tools to decode and forge tokens locally so you can see what is inside them.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Python ships with macOS; install the JWT library for the lab
python3 -m pip install pyjwt

# Authenticate to GitHub's API with a personal access token in a header
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user | head
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install the JWT library
python -m pip install pyjwt

# Authenticate using a token held in an environment variable
curl.exe -s -H "Authorization: Bearer $env:GITHUB_TOKEN" https://api.github.com/user
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y python3-pip curl
python3 -m pip install pyjwt

# Authenticate with a bearer token
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user | head
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Run the JWT lab in a throwaway Python container
docker run --rm -it python:3.12-slim sh -c "pip install pyjwt && python"
```

> 🔐 Never commit tokens to source control or paste them into shared chats. Store them in environment variables or a secrets manager.

</details>

## 🧙‍♂️ Chapter 1: API Keys and the Authorization Header

*The simplest credential is the **API key**: a long random string a service issues you. You attach it to every request, usually in a header. Anyone holding the key acts as you - so treat it like a password.*

### ⚔️ Skills You'll Forge in This Chapter
- Sending an API key safely
- Why keys are simple but limited
- Authentication vs authorization

### 🏗️ Using an API Key

Keys travel in a header (preferred) or sometimes a query parameter (worse, because URLs leak into logs):

```bash
# ✅ Preferred: key in a header
curl -s -H "Authorization: Bearer YOUR_API_KEY" https://api.example.com/v1/data

# A custom header is also common
curl -s -H "X-API-Key: YOUR_API_KEY" https://api.example.com/v1/data

# ❌ Avoid: key in the URL - it ends up in server logs and browser history
curl -s "https://api.example.com/v1/data?api_key=YOUR_API_KEY"
```

API keys identify the *application*, rarely a specific user, and usually cannot express fine-grained permissions or expire on their own. They are great for server-to-server calls, weak for delegated user access - which is exactly the gap OAuth2 fills.

**Authentication** is proving identity (the key proves the caller is a known app). **Authorization** is deciding what that identity may do (whether this app may read or also write).

### 🔍 Knowledge Check: Keys
- [ ] Why is a key in a header safer than a key in the URL?
- [ ] What does an API key typically identify - a user or an app?
- [ ] State the difference between authentication and authorization.

### ⚡ Quick Wins and Checkpoints
- [ ] **Authenticated a call**: You sent a key and received protected data
- [ ] **Defined the terms**: You can separate authn from authz in one sentence

## 🧙‍♂️ Chapter 2: Sessions vs Tokens and the JWT

*Before APIs, servers tracked you with a **session**: state in server memory keyed by a cookie. APIs prefer **tokens**: self-contained credentials the client carries, so the server stays stateless.*

### ⚔️ Skills You'll Forge in This Chapter
- Why tokens beat sessions for APIs
- The three parts of a JWT
- What a JWT signature does and does not protect

### 🏗️ Sessions vs Tokens

| | Server session | Bearer token (e.g. JWT) |
| --- | --- | --- |
| State lives | On the server | In the token itself |
| Scales horizontally | Needs shared session store | Any server can validate |
| Works across domains | Awkward (cookies) | Naturally (header) |
| Revocation | Easy (delete session) | Harder (needs a blocklist or short expiry) |

A **JWT** (JSON Web Token) has three base64url parts separated by dots: `header.payload.signature`. The header names the algorithm, the payload holds **claims** (data), and the signature proves the token was not tampered with.

```python
import jwt  # PyJWT

secret = "super-secret-signing-key"

# Issue a token with claims (sub = subject, exp = expiry)
token = jwt.encode(
    {"sub": "user-42", "scope": "read:profile", "exp": 1999999999},
    secret,
    algorithm="HS256",
)
print(token)  # eyJhbGciOi...  (three dot-separated parts)

# Verify and decode it - raises if the signature or expiry is invalid
claims = jwt.decode(token, secret, algorithms=["HS256"])
print(claims["sub"], claims["scope"])  # user-42 read:profile
```

Crucially, a JWT payload is **encoded, not encrypted** - anyone can read it. The signature only proves it has not been *altered*. Never put secrets in a JWT payload, and always verify the signature server-side. Decode the parts yourself to see this:

```bash
# Split a JWT on dots and base64-decode the payload - it is plainly readable
echo "$JWT" | cut -d. -f2 | base64 -d 2>/dev/null
```

### 🔍 Knowledge Check: Tokens & JWT
- [ ] Why can any server in a fleet validate a JWT but not a server session?
- [ ] What are the three parts of a JWT?
- [ ] Is a JWT payload secret? What does its signature actually guarantee?

## 🧙‍♂️ Chapter 3: OAuth2 Flows and Scopes

*OAuth2 is the framework behind "Log in with Google" and third-party API access. It lets a user grant an app limited access to their data **without sharing their password**. The most important flow is the **authorization code flow**.*

### ⚔️ Skills You'll Forge in This Chapter
- The roles in OAuth2
- The authorization code flow, step by step
- Scopes and least privilege

### 🏗️ The Authorization Code Flow

OAuth2 has four roles: the **resource owner** (the user), the **client** (the app), the **authorization server** (issues tokens), and the **resource server** (the API). The flow:

```text
1. Client redirects user to the authorization server with requested scopes
   GET https://auth.example.com/authorize
       ?response_type=code&client_id=APP&scope=read:profile&redirect_uri=...
2. User logs in and consents to the requested scopes
3. Auth server redirects back to the client with a one-time CODE
   GET https://app.example.com/callback?code=ONE_TIME_CODE
4. Client exchanges the code (plus its secret) for tokens, server-to-server
   POST https://auth.example.com/token  -> { access_token, refresh_token }
5. Client calls the API with the access token
   GET /me  Authorization: Bearer ACCESS_TOKEN
```

Step 4 happens on the back channel so the access token never passes through the browser. Exchange the code like this:

```bash
# Step 4: trade the one-time code for an access token
curl -s -X POST https://auth.example.com/token \
  -d grant_type=authorization_code \
  -d code=ONE_TIME_CODE \
  -d client_id=APP \
  -d client_secret=APP_SECRET \
  -d redirect_uri=https://app.example.com/callback
```

**Scopes** express least privilege: the client asks only for what it needs (`read:profile`, not `admin:everything`). The user sees and approves the exact scopes. A **refresh token** lets the client obtain a new short-lived access token when it expires, without bothering the user again. For mobile and single-page apps that cannot keep a secret, **PKCE** (Proof Key for Code Exchange) replaces the client secret with a per-request dynamic proof.

### 🔍 Knowledge Check: OAuth2
- [ ] What is the one-time code exchanged for, and why does that happen server-to-server?
- [ ] What problem do scopes solve?
- [ ] Why do single-page apps need PKCE?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Authenticate for Real
**Objective**: Call a protected endpoint using a bearer token.

**Requirements**:
- [ ] Create a GitHub personal access token with the `read:user` scope
- [ ] Call `https://api.github.com/user` with the token in an `Authorization` header
- [ ] Confirm you receive your own profile, then remove the scope and observe the change

**Validation**: The authenticated call returns your account; an unscoped call is rejected.

### 🟡 Intermediate Challenge: Dissect a JWT
**Objective**: Forge and decode a JWT, then tamper with it.

**Requirements**:
- [ ] Issue a JWT with `sub` and `scope` claims using PyJWT
- [ ] Decode the payload by hand (base64) to prove it is readable
- [ ] Change one character of the token and show that verification now fails

**Validation**: You can explain why tampering is detected but the payload was never secret.

### 🔴 Advanced Challenge: Diagram the Flow
**Objective**: Document a complete OAuth2 authorization code flow for a real provider.

**Requirements**:
- [ ] Pick a provider (Google, GitHub, Auth0) and list its authorize and token URLs
- [ ] Diagram all five steps with the roles labeled
- [ ] Choose the minimum scopes for "read the user's email" and justify them

**Validation**: A teammate could implement the flow from your diagram.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Keeper of the Keys** - You authenticated against a protected API
- 🛡️ **Token Warden** - You can read and reason about JWTs and OAuth2 flows

**🛠️ Skills Unlocked**:
- **Token-Based Authentication** - Carry and present credentials statelessly
- **OAuth2 Flow Selection** - Choose the right grant for the right client

**🔓 Unlocked Quests**:
- Error Handling - Return clean `401`/`403` responses
- Rate Limiting - Throttle authenticated callers fairly

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Error Handling](/quests/0111/error-handling/) - Respond to auth failures cleanly

**Explore Side Adventures**:
- ⚔️ [Rate Limiting](/quests/0111/rate-limiting/) - Protect your API from abuse
- ⚔️ [REST Principles](/quests/0111/rest-principles/) - Design the API you are securing

### Character Class Recommendations

**💻 Software Developer**: Continue to [Error Handling](/quests/0111/error-handling/)  
**🏗️ System Engineer**: Explore [Rate Limiting](/quests/0111/rate-limiting/)  
**🛡️ Security Specialist**: Advance to [Error Handling](/quests/0111/error-handling/)

## 📚 Resources

### Official Documentation
- [RFC 6749: The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749) - The OAuth2 spec
- [RFC 7519: JSON Web Token (JWT)](https://www.rfc-editor.org/rfc/rfc7519) - The JWT spec
- [RFC 7636: PKCE](https://www.rfc-editor.org/rfc/rfc7636) - Proof Key for Code Exchange

### Community Resources
- [OAuth.com](https://www.oauth.com/) - A readable, illustrated OAuth2 guide
- [jwt.io](https://jwt.io/) - Decode and inspect JWTs in the browser
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) - Secure practices

### Learning Materials
- [MDN: Authorization header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization) - The header you will use constantly
- [Auth0: Which OAuth2 flow should I use?](https://auth0.com/docs/get-started/authentication-and-authorization-flow) - Choosing a grant
- [PyJWT documentation](https://pyjwt.readthedocs.io/) - The library used in the lab

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Authenticated to a real API with a bearer token
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0111 - API Development]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[API Fundamentals: HTTP, Requests, and JSON]]
**Unlocks:** [[Error Handling: Status Codes, Problem Details, and Idempotency]] · [[Rate Limiting: Token Buckets, 429s, and Quotas]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
