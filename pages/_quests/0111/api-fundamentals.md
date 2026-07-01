---
title: 'API Fundamentals: HTTP, Requests, and JSON'
author: IT-Journey Team
description: Master the fundamentals of web APIs including HTTP methods, status codes, request/response anatomy, headers, and JSON so you can call and reason about any API.
excerpt: Learn what an API is, the HTTP request/response cycle, methods, status codes, and JSON
preview: images/previews/api-fundamentals-http-requests-json.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0111'
difficulty: 🟢 Easy
estimated_time: 60-90 minutes
primary_technology: http
quest_type: main_quest
quest_series: API Design Mastery
quest_line: The Gatekeeper's Road
quest_arc: Foundations of the Interface
quest_dependencies:
  required_quests: []
  recommended_quests: []
  unlocks_quests:
  - /quests/0111/rest-principles/
  - /quests/0111/api-authentication/
skill_focus: backend
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Basic command line navigation
  - Comfort reading code in at least one language (examples use Bash, Python, JavaScript)
  - General awareness that web browsers talk to servers
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - curl installed (ships with macOS and most Linux distributions)
  - Optional Python 3 or Node.js for the scripted examples
  skill_level_indicators:
  - You have used a terminal before
  - You are ready to make your first real API call
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - Successfully called a public API and parsed its JSON response
  skill_demonstrations:
  - Can name the parts of an HTTP request and response
  - Can choose the correct HTTP method for a given action
  knowledge_checks:
  - Understands the meaning of 2xx, 4xx, and 5xx status codes
  - Can read and write a simple JSON document
permalink: /quests/0111/api-fundamentals/
categories:
- Quests
- Backend
- Easy
tags:
- '0111'
- http
- main_quest
- backend
- hands-on
- gamified-learning
keywords:
  primary:
  - '0111'
  - http
  - main_quest
  secondary:
  - rest
  - json
  - http-methods
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0111 (7) Quest: Main Quest - API Fundamentals'
rewards:
  badges:
  - 🏆 Gatekeeper - Made your first real API call and understood the response
  - 📜 Reader of Requests - Can decode any HTTP request and response by hand
  skills_unlocked:
  - 🛠️ HTTP Request Crafting
  - 🧠 JSON Reading and Writing
  progression_points: 50
  unlocks_features:
  - Access to the REST Principles and API Authentication quests
layout: quest
---
*Greetings, brave adventurer! You stand at the gates of **Level 0111 - API Development**, the road that connects every kingdom you have ever built. An API - an Application Programming Interface - is the spoken language between programs, the way one service asks another for what it needs. This quest, **API Fundamentals**, teaches you that language from its very first word.*

*By the end you will speak HTTP fluently: you will know how a request is shaped, how a response answers it, what the cryptic three-digit status codes mean, and how to read the JSON that flows between them. Every later quest in this level builds on what you forge here.*

## 📖 The Legend Behind This Quest

*In the early web, pages were static scrolls - a server handed your browser a finished document and the conversation ended. Then developers realized the same protocol that delivered web pages, **HTTP**, could deliver structured data just as easily. A program could ask a server a question and receive a machine-readable answer. The API was born, and with it the modern era of services that talk to services.*

*Today an API is the universal handshake. Your weather app, your bank's mobile login, the map in your car, and the AI you chat with all speak through APIs. Learn this language and you can wire any two systems together.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **What an API Is** - Explain in plain language what an API does and why services use them
- [ ] **The HTTP Request/Response Cycle** - Describe every part of a request and the response it earns
- [ ] **HTTP Methods** - Choose the right verb (GET, POST, PUT, PATCH, DELETE) for an action
- [ ] **Status Codes** - Read 2xx, 3xx, 4xx, and 5xx codes and know who is at fault
- [ ] **JSON** - Read and write JSON, the lingua franca of modern APIs

### Secondary Objectives (Bonus Achievements)
- [ ] **Headers** - Use `Content-Type`, `Accept`, and `Authorization` correctly
- [ ] **Query Parameters vs Body** - Know where data belongs in a request
- [ ] **Calling APIs from Code** - Make the same request from the terminal, Python, and JavaScript

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Sketch a full HTTP request and response on a whiteboard from memory
- [ ] Pick the correct method and status code for a new endpoint without looking them up
- [ ] Read an unfamiliar API's JSON response and extract the field you need
- [ ] Explain to a teammate why an API returned `404` instead of `500`

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] You can open and use a terminal
- [ ] You have seen code in at least one language before
- [ ] You understand that the web involves clients (browsers) and servers

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] `curl` available in your terminal
- [ ] Optional: Python 3 or Node.js for the scripted examples
- [ ] An internet connection (we call free public APIs)

### 🧠 Skill Level Indicators
This **🟢 Easy** quest expects:
- [ ] No prior API experience - we start from zero
- [ ] Willingness to run commands and read their output
- [ ] Ready for 60-90 minutes of focused, hands-on learning

## 🌍 Choose Your Adventure Platform

*Every platform can make HTTP requests. Choose the path that matches your setup; the API calls themselves are identical everywhere.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# curl ships with macOS. Confirm it is present:
curl --version

# Optional: install jq to pretty-print and query JSON responses
brew install jq

# Your first API call - fetch a sample post as JSON
curl https://jsonplaceholder.typicode.com/posts/1
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# curl.exe ships with Windows 10+. Confirm it:
curl.exe --version

# Optional: install jq for JSON querying
winget install jqlang.jq

# Your first API call
curl.exe https://jsonplaceholder.typicode.com/posts/1
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# Install curl and jq if you do not already have them
sudo apt update && sudo apt install -y curl jq   # Debian/Ubuntu
# sudo dnf install -y curl jq                     # Fedora/RHEL

# Your first API call
curl https://jsonplaceholder.typicode.com/posts/1
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Any container or Codespace with curl works identically.
docker run --rm curlimages/curl:latest \
  https://jsonplaceholder.typicode.com/posts/1
```

</details>

## 🧙‍♂️ Chapter 1: What Is an API and What Is HTTP?

*An **API** is a contract: "send me a request shaped like this, and I will send you a response shaped like that." On the web, that contract is carried over **HTTP** (HyperText Transfer Protocol), a simple text-based protocol where a client sends a request and a server returns a response.*

### ⚔️ Skills You'll Forge in This Chapter
- The mental model of client, request, server, response
- The anatomy of an HTTP request
- The anatomy of an HTTP response

### 🏗️ The Anatomy of a Request and Response

Every HTTP request has four parts: a **method**, a **URL** (path + query), **headers**, and an optional **body**. Use `curl -v` to see the raw conversation:

```bash
# -v shows the request we send (>) and the response we receive (<)
curl -v https://jsonplaceholder.typicode.com/posts/1
```

The request line looks like this (the `>` lines):

```http
GET /posts/1 HTTP/1.1
Host: jsonplaceholder.typicode.com
Accept: */*
```

And the response (the `<` lines) carries a **status line**, **headers**, and a **body**:

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident",
  "body": "quia et suscipit..."
}
```

That is the whole game: you send a method + path + headers (+ maybe a body), and you get back a status code + headers + body.

### 🔍 Knowledge Check: Anatomy
- [ ] What are the four parts of an HTTP request?
- [ ] Which response header tells you the body is JSON?
- [ ] What does the `Host` header identify?

### ⚡ Quick Wins and Checkpoints
- [ ] **First call made**: You received a `200 OK` from a public API
- [ ] **Saw the raw HTTP**: You read the `>` request and `<` response lines

## 🧙‍♂️ Chapter 2: HTTP Methods - The Verbs of the Web

*The **method** declares your intent. The five you will use constantly map cleanly to the things you do with data.*

### ⚔️ Skills You'll Forge in This Chapter
- The five core HTTP methods and what each means
- Which methods are safe and which are idempotent

### 🏗️ The Core Methods

| Method | Intent | Safe? | Idempotent? | Example |
| --- | --- | --- | --- | --- |
| **GET** | Read a resource | Yes | Yes | `GET /posts/1` |
| **POST** | Create a new resource | No | No | `POST /posts` |
| **PUT** | Replace a resource entirely | No | Yes | `PUT /posts/1` |
| **PATCH** | Update part of a resource | No | No | `PATCH /posts/1` |
| **DELETE** | Remove a resource | No | Yes | `DELETE /posts/1` |

**Safe** means the request does not change server state (a GET should never delete anything). **Idempotent** means making the request twice has the same effect as making it once (deleting the same record twice still leaves it deleted).

Try a `POST` that creates a resource and sends a JSON body:

```bash
# -X sets the method, -H sets a header, -d sends the request body
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "body": "Hello API", "userId": 1}'
```

The server replies `201 Created` and echoes the new resource, including the `id` it assigned.

### 🔍 Knowledge Check: Methods
- [ ] Which method would you use to read a list of users?
- [ ] Why is `DELETE` idempotent but `POST` is not?
- [ ] What is the difference between `PUT` and `PATCH`?

## 🧙‍♂️ Chapter 3: Status Codes and JSON

*Every response carries a three-digit **status code** that tells you what happened. The first digit is the category - learn the five categories and you can interpret any code on sight.*

### ⚔️ Skills You'll Forge in This Chapter
- The five status code families and who is to blame
- Reading and writing JSON
- Making the same call from three languages

### 🏗️ Status Code Families

| Range | Meaning | Common examples |
| --- | --- | --- |
| **1xx** | Informational | `100 Continue` |
| **2xx** | Success | `200 OK`, `201 Created`, `204 No Content` |
| **3xx** | Redirection | `301 Moved Permanently`, `304 Not Modified` |
| **4xx** | Client error - *you* sent something wrong | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `429 Too Many Requests` |
| **5xx** | Server error - the *server* broke | `500 Internal Server Error`, `503 Service Unavailable` |

The crucial instinct: **4xx means fix your request; 5xx means the server failed.** Ask for a code explicitly:

```bash
# -o /dev/null discards the body; -w prints only the status code
curl -s -o /dev/null -w "%{http_code}\n" \
  https://jsonplaceholder.typicode.com/posts/9999
# -> 404, because post 9999 does not exist
```

**JSON** (JavaScript Object Notation) is how almost all modern APIs encode data. It has six types: object `{}`, array `[]`, string, number, boolean, and `null`:

```json
{
  "id": 1,
  "name": "Ada Lovelace",
  "active": true,
  "roles": ["admin", "author"],
  "manager": null
}
```

Now make the identical request from three languages. First **Python**:

```python
import requests

# GET a resource and parse the JSON body into a dict
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)        # 200
data = response.json()             # parse JSON -> Python dict
print(data["title"])               # access a field by key
```

Then **JavaScript** (Node 18+ or any modern browser, using the built-in `fetch`):

```javascript
// fetch returns a Promise; await it, then parse the JSON body
const response = await fetch("https://jsonplaceholder.typicode.com/posts/1");
console.log(response.status);      // 200
const data = await response.json();// parse JSON -> object
console.log(data.title);           // access a field
```

And the same with **curl + jq** to extract one field:

```bash
# Pipe the JSON response into jq and pull out the .title field
curl -s https://jsonplaceholder.typicode.com/posts/1 | jq '.title'
```

### 🔍 Knowledge Check: Status & JSON
- [ ] A request returns `503`. Whose problem is it, yours or the server's?
- [ ] What status code should creating a new resource return?
- [ ] Name the six JSON value types.

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Read a Public API
**Objective**: Call a free public API and extract one field from its JSON.

**Requirements**:
- [ ] Use `curl` to GET `https://api.github.com/users/octocat`
- [ ] Identify the status code returned
- [ ] Extract the `public_repos` field (use `jq` or read it by eye)

**Validation**: You can state the status code and the field's value.

### 🟡 Intermediate Challenge: Create and Inspect
**Objective**: Send a `POST` with a JSON body and inspect the response.

**Requirements**:
- [ ] POST a new post to `https://jsonplaceholder.typicode.com/posts`
- [ ] Send a correct `Content-Type` header
- [ ] Record the status code and the `id` the server assigned

**Validation**: You receive `201 Created` and a new `id`.

### 🔴 Advanced Challenge: Method and Code Mapping
**Objective**: For a hypothetical "library" API, design the endpoints.

**Requirements**:
- [ ] Choose method + path for: list books, get one book, add a book, update a book, delete a book
- [ ] State the success status code each should return
- [ ] State which status code a request for a missing book returns

**Validation**: Every choice matches the method/status conventions from this quest.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Gatekeeper** - You made your first real API call and understood the response
- 📜 **Reader of Requests** - You can decode any HTTP request and response by hand

**🛠️ Skills Unlocked**:
- **HTTP Request Crafting** - Build requests with the right method, headers, and body
- **JSON Reading and Writing** - Parse and produce the data format the web runs on

**🔓 Unlocked Quests**:
- REST Principles - Turn raw HTTP into well-designed resource APIs
- API Authentication - Prove who you are when you call an API

**📊 Progression Points**: +50 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [REST Principles](/quests/0111/rest-principles/) - Design APIs the right way

**Explore Side Adventures**:
- ⚔️ [API Authentication](/quests/0111/api-authentication/) - Keys, tokens, and OAuth2
- ⚔️ [Error Handling](/quests/0111/error-handling/) - Status codes and clean error responses

### Character Class Recommendations

**💻 Software Developer**: Continue to [REST Principles](/quests/0111/rest-principles/)  
**🏗️ System Engineer**: Explore [API Authentication](/quests/0111/api-authentication/)  
**🛡️ Security Specialist**: Check out [API Authentication](/quests/0111/api-authentication/)

## 📚 Resources

### Official Documentation
- [MDN: An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) - The canonical HTTP primer
- [MDN: HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) - Every status code explained
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html) - The authoritative specification

### Community Resources
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - The free fake API used in this quest
- [HTTPBin](https://httpbin.org/) - A request-and-response testing service
- [Public APIs list](https://github.com/public-apis/public-apis) - Hundreds of free APIs to practice on

### Learning Materials
- [MDN: Working with JSON](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON) - JSON syntax and parsing
- [curl documentation](https://curl.se/docs/) - The command-line HTTP client
- [jq manual](https://jqlang.github.io/jq/manual/) - Query and transform JSON

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Made a real API call and parsed its JSON
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0111 - API Development]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Unlocks:** [[REST Principles: Constraints, Resources, and Richardson Maturity]] · [[API Authentication: Keys, Tokens, OAuth2, and JWT]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
