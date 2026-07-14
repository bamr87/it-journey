---
title: 'API Documentation: OpenAPI, Swagger, and Contract-First'
author: IT-Journey Team
description: 'Master API documentation using OpenAPI and Swagger: write a contract-first spec, add request and response examples, and render live docs.'
excerpt: Learn OpenAPI and Swagger, contract-first design, examples, and documentation tooling
preview: images/previews/api-documentation-openapi-swagger-contract-first.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0111'
difficulty: 🟡 Medium
estimated_time: 75-90 minutes
primary_technology: openapi
quest_type: main_quest
quest_series: API Design Mastery
quest_line: The Gatekeeper's Road
quest_arc: Stewards of the Interface
quest_dependencies:
  required_quests:
  - /quests/0111/rest-principles/
  recommended_quests:
  - /quests/0111/api-versioning/
  unlocks_quests: []
skill_focus: backend
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Completion of REST Principles (resources, methods, status codes)
  - Basic familiarity with YAML or JSON
  - Comfort making requests with curl
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A text editor (VS Code recommended)
  - Optional Node.js or Docker for the Swagger UI lab
  skill_level_indicators:
  - You can read and write YAML
  - You are ready to describe an API formally
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A valid OpenAPI document describing at least one endpoint
  skill_demonstrations:
  - Can write an OpenAPI path with parameters and responses
  - Can render docs from a spec with Swagger UI
  knowledge_checks:
  - Understands the contract-first workflow
  - Can add request and response examples to a spec
permalink: /quests/0111/api-documentation/
categories:
- Quests
- Backend
- Medium
tags:
- '0111'
- openapi
- main_quest
- backend
- hands-on
- gamified-learning
keywords:
  primary:
  - '0111'
  - openapi
  - main_quest
  secondary:
  - swagger
  - contract-first
  - documentation
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0111 (7) Quest: Main Quest - API Documentation'
rewards:
  badges:
  - 🏆 Scribe of the Interface - Authored a valid OpenAPI specification
  - 📖 Keeper of the Contract - Adopted a contract-first workflow
  skills_unlocked:
  - 🛠️ OpenAPI Authoring
  - 🧠 Contract-First Design
  progression_points: 60
  unlocks_features:
  - Completion of the Level 0111 API Development quest line
layout: quest
---
*Greetings, brave adventurer! You stand at the final gate of the API Development road. You have learned to call, design, secure, protect, and evolve APIs. Now you will learn to **describe** them - so precisely that machines can generate clients, validate requests, and render beautiful interactive docs from your words alone. This is the art of **API Documentation**.*

*The standard you will master is **OpenAPI** (formerly Swagger), a machine-readable contract for HTTP APIs. With it you can design **contract-first**: agree on the interface before writing a line of server code, then let tooling scaffold both sides. A well-documented API is one developers actually want to use.*

## 📖 The Legend Behind This Quest

*In the dark ages of APIs, documentation lived in a wiki that drifted out of date the moment code changed. Developers integrated by trial and error, poking endpoints to discover their shapes. Then the community gathered around a single machine-readable format - Swagger, later renamed OpenAPI - and everything changed. One document could now drive interactive docs, client SDKs in a dozen languages, request validation, and mock servers.*

*The greatest shift was philosophical: **contract-first** design. Write the OpenAPI document first, get every consumer to agree, and only then implement. The contract becomes the single source of truth that frontend, backend, and partners all build against in parallel.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **The OpenAPI Specification** - Understand what it describes and why it matters
- [ ] **Describing an Endpoint** - Write paths, methods, parameters, and responses
- [ ] **Schemas and Components** - Define and reuse data models
- [ ] **Examples** - Attach request and response examples to your spec
- [ ] **Contract-First Workflow** - Design the contract before the code

### Secondary Objectives (Bonus Achievements)
- [ ] **Swagger UI** - Render interactive docs from your spec
- [ ] **Validation and Linting** - Catch spec errors with tooling
- [ ] **Code Generation** - Generate clients or stubs from the contract

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Write a valid OpenAPI document for a small API from memory of the structure
- [ ] Reuse a schema with `$ref` instead of repeating yourself
- [ ] Render your spec in Swagger UI and try a request from the browser
- [ ] Explain why contract-first lets teams build in parallel

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] You have completed REST Principles or know resources, methods, and status codes
- [ ] You can read and write YAML or JSON
- [ ] You can make requests with curl

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A text editor (VS Code with an OpenAPI extension recommended)
- [ ] Optional: Node.js or Docker for the Swagger UI lab
- [ ] An internet connection

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can read and write YAML
- [ ] You can describe an endpoint's inputs and outputs
- [ ] Ready for 75-90 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*OpenAPI is just a text file, so any platform works. These setups let you render and validate your spec.*

> **Heads-up:** the `redocly lint` and `redocly build-docs` commands below act on an `openapi.yaml` file that you author in Chapters 1–2. Install the tooling now, but run the lint/render commands *after* the spec exists (or create an empty `openapi.yaml` placeholder first) — running them in an empty directory fails with `openapi.yaml does not exist`.

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install the Redocly CLI to lint and preview OpenAPI docs
brew install node
npm install -g @redocly/cli

# Validate a spec, then render it as a docs site
redocly lint openapi.yaml
redocly build-docs openapi.yaml -o docs.html   # static HTML (or: redocly preview for a live server)
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install OpenJS.NodeJS
npm install -g @redocly/cli

# Lint and render your OpenAPI document
redocly lint openapi.yaml
redocly build-docs openapi.yaml -o docs.html   # or: redocly preview for a live server
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y nodejs npm
npm install -g @redocly/cli
redocly lint openapi.yaml && redocly build-docs openapi.yaml -o docs.html
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Serve Swagger UI in a container and mount your spec into it
docker run --rm -p 8080:8080 \
  -e SWAGGER_JSON=/spec/openapi.yaml \
  -v "$PWD:/spec" swaggerapi/swagger-ui
# Open http://localhost:8080 to explore the interactive docs
```

</details>

## 🧙‍♂️ Chapter 1: What Is OpenAPI and Contract-First Design?

*OpenAPI is a standard, language-agnostic description of an HTTP API written in YAML or JSON. One file tells tools everything: the endpoints, their parameters, the shapes of requests and responses, and the auth they require.*

### ⚔️ Skills You'll Forge in This Chapter
- What an OpenAPI document contains
- The contract-first workflow
- Why one document drives so many tools

### 🏗️ The Shape of an OpenAPI Document

Every OpenAPI 3.x document has a few top-level sections: `openapi` (the version), `info`, `servers`, `paths`, and reusable `components`.

```yaml
openapi: 3.1.0
info:
  title: Bookstore API
  version: 1.0.0
  description: A tiny API for managing books.
servers:
  - url: https://api.example.com/v1
paths: {}        # endpoints go here (next chapter)
components: {}   # reusable schemas go here
```

**Contract-first** means you write this document *before* the implementation. The team reviews and agrees on the contract, then frontend, backend, and partner teams build against it in parallel - the frontend mocks responses from the spec while the backend implements them. The alternative, **code-first**, generates the spec from annotations in already-written code; it is convenient but lets the implementation, not a deliberate design, dictate the contract.

```text
Contract-first flow:
  design openapi.yaml  ->  review & agree  ->  generate mocks + stubs
                       ->  build frontend & backend in parallel  ->  test against the contract
```

### 🔍 Knowledge Check: OpenAPI Basics
- [ ] Name the top-level sections of an OpenAPI document.
- [ ] What is the difference between contract-first and code-first?
- [ ] Why can one OpenAPI file drive docs, mocks, and SDKs at once?

### ⚡ Quick Wins and Checkpoints
- [ ] **Scaffolded a spec**: You wrote a valid `info` and `servers` block
- [ ] **Understood the flow**: You can explain contract-first in one sentence

## 🧙‍♂️ Chapter 2: Describing Endpoints, Schemas, and Examples

*The heart of the document is `paths`: each endpoint, its parameters, its request body, and every response it can return. Reusable data models live in `components/schemas` and are referenced with `$ref`.*

### ⚔️ Skills You'll Forge in This Chapter
- Writing a path with parameters and responses
- Defining and reusing schemas
- Adding examples

### 🏗️ A Fully Described Endpoint

Here is `GET /books/{id}` and `POST /books`, with a reusable `Book` schema and examples:

```yaml
# Declare an empty default security requirement so redocly's
# security-defined rule is satisfied (these demo endpoints need no auth)
security: []
paths:
  /books/{id}:
    get:
      summary: Get a book by id
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: The requested book
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Book'   # reuse, do not repeat
              example:
                id: 1
                title: The Pragmatic Programmer
                author: Hunt and Thomas
        '404':
          description: No book with that id
  /books:
    post:
      summary: Create a book
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Book'
      responses:
        '201':
          description: The created book

components:
  schemas:
    Book:
      type: object
      required: [title, author]
      properties:
        id:     { type: integer, readOnly: true }
        title:  { type: string,  example: Clean Code }
        author: { type: string,  example: Robert C. Martin }
```

The `$ref` keyword is the key to DRY documentation: define `Book` once and reference it from every place a book appears. **Examples** make the docs come alive - a developer can copy a realistic payload instead of guessing. Validate the document with tooling before you trust it:

```bash
# Lint the spec; zero errors means tools can rely on it.
# redocly may still print advisory *warnings* (e.g. a missing license,
# an example.com server, or a missing operationId) — those do not fail the run.
redocly lint openapi.yaml
```

### 🔍 Knowledge Check: Endpoints & Schemas
- [ ] What does `$ref: '#/components/schemas/Book'` accomplish?
- [ ] Where do you declare which fields are required?
- [ ] Why attach examples to responses?

## 🧙‍♂️ Chapter 3: Tooling, Swagger UI, and Code Generation

*A spec's value multiplies through tooling. The same `openapi.yaml` renders interactive docs, generates client SDKs, and validates incoming requests against the contract.*

### ⚔️ Skills You'll Forge in This Chapter
- Rendering interactive docs with Swagger UI
- Generating clients from the contract
- Keeping docs and code in sync

### 🏗️ From Spec to Living Documentation

**Swagger UI** turns your document into a web page where developers read every endpoint and even fire test requests from the browser. Serve it with one Docker command:

```bash
# Mount your spec and browse interactive docs at http://localhost:8080
docker run --rm -p 8080:8080 \
  -e SWAGGER_JSON=/spec/openapi.yaml \
  -v "$PWD:/spec" swaggerapi/swagger-ui
```

**Code generation** reads the same contract and emits a typed client in your language, so consumers never hand-write request code:

```bash
# Generate a Python client from the contract
npx @openapitools/openapi-generator-cli generate \
  -i openapi.yaml -g python -o ./client
```

The golden rule is to keep the spec and the implementation in sync. Contract-first teams treat the spec as the source of truth and run **contract tests** in CI that replay the spec's examples against the live server, failing the build if the implementation drifts from the documented behavior. Whether you go contract-first (spec drives code) or code-first (annotations generate the spec), the spec must never silently lie about the API.

### 🔍 Knowledge Check: Tooling
- [ ] What can a developer do in Swagger UI besides read?
- [ ] What does an OpenAPI code generator produce?
- [ ] How do contract tests stop docs from drifting from reality?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Describe One Endpoint
**Objective**: Write a valid OpenAPI fragment for a single endpoint.

**Requirements**:
- [ ] Describe `GET /books/{id}` with a path parameter
- [ ] Define a `200` and a `404` response
- [ ] Lint it with `redocly lint` until it passes

**Validation**: The linter reports no errors.

### 🟡 Intermediate Challenge: Reuse a Schema
**Objective**: Add a second endpoint that reuses a shared schema.

**Requirements**:
- [ ] Define a `Book` schema under `components/schemas`
- [ ] Reference it with `$ref` from both a GET and a POST
- [ ] Attach a realistic response example

**Validation**: No schema is duplicated; examples render in Swagger UI.

### 🔴 Advanced Challenge: Contract-First Build
**Objective**: Run a full contract-first cycle on a small API.

**Requirements**:
- [ ] Author the complete `openapi.yaml` before writing server code
- [ ] Render it in Swagger UI and generate a client with the generator
- [ ] Describe how a contract test would verify the implementation matches

**Validation**: The generated client and rendered docs both come from your single spec.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Scribe of the Interface** - You authored a valid OpenAPI specification
- 📖 **Keeper of the Contract** - You adopted a contract-first workflow

**🛠️ Skills Unlocked**:
- **OpenAPI Authoring** - Describe any HTTP API precisely
- **Contract-First Design** - Let the contract drive parallel development

**🔓 Unlocked Quests**:
- You have completed the Level 0111 API Development quest line - advance to Level 1000, Cloud Computing

**📊 Progression Points**: +60 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 Advance to Level 1000 - Cloud Computing - deploy the APIs you have learned to build

**Explore Side Adventures**:
- ⚔️ [API Versioning](/quests/0111/api-versioning/) - Document your versions in the spec
- ⚔️ [Error Handling](/quests/0111/error-handling/) - Describe your error responses formally

### Character Class Recommendations

**💻 Software Developer**: Advance to Level 1000 - Cloud Computing  
**🏗️ System Engineer**: Explore [API Versioning](/quests/0111/api-versioning/)  
**🛡️ Security Specialist**: Revisit [API Authentication](/quests/0111/api-authentication/) and document its security schemes

## 📚 Resources

### Official Documentation
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - The authoritative standard
- [OpenAPI Initiative](https://www.openapis.org/) - The governing body and learning hub
- [Swagger UI](https://swagger.io/tools/swagger-ui/) - Interactive documentation tooling

### Community Resources
- [Swagger Editor](https://editor.swagger.io/) - Write and preview specs in the browser
- [Redocly OpenAPI docs](https://redocly.com/docs/) - Linting and docs generation
- [OpenAPI Generator](https://openapi-generator.tech/) - Generate clients and servers

### Learning Materials
- [Learn OpenAPI (openapi-map)](https://openapi-map.apihandyman.io/) - Visual map of the spec
- [Stoplight: Contract-first API design](https://stoplight.io/api-design-guide) - The workflow in depth
- [JSON Schema](https://json-schema.org/) - The schema language OpenAPI builds on

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Authored a valid OpenAPI document
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0111 - API Development]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[REST Principles: Constraints, Resources, and Richardson Maturity]]
**Unlocks:** [[Level 1000 - Cloud Computing]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
