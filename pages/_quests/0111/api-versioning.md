---
title: 'API Versioning: URI, Headers, and Backward Compatibility'
author: IT-Journey Team
description: Master API versioning strategies including URI versus header versioning, backward compatibility, breaking versus non-breaking changes, and graceful deprecation.
excerpt: Learn URI vs header versioning, backward compatibility, and how to deprecate an API gracefully
preview: images/previews/api-versioning-uri-headers-compatibility.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0111'
difficulty: 🟡 Medium
estimated_time: 60-90 minutes
primary_technology: rest
quest_type: main_quest
quest_series: API Design Mastery
quest_line: The Gatekeeper's Road
quest_arc: Stewards of the Interface
quest_dependencies:
  required_quests:
  - /quests/0111/rest-principles/
  recommended_quests:
  - /quests/0111/error-handling/
  unlocks_quests:
  - /quests/0111/api-documentation/
skill_focus: backend
learning_style: conceptual
prerequisites:
  knowledge_requirements:
  - Completion of REST Principles (resources, methods)
  - Understanding of HTTP headers
  - Comfort making requests with curl
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - curl installed
  - Optional jq for inspecting responses
  skill_level_indicators:
  - You can design resource URLs
  - You are ready to think about change over time
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A change classified as breaking or non-breaking with a versioning plan
  skill_demonstrations:
  - Can choose between URI and header versioning with justification
  - Can classify a change as breaking or non-breaking
  knowledge_checks:
  - Understands backward compatibility
  - Can describe a graceful deprecation timeline
permalink: /quests/0111/api-versioning/
categories:
- Quests
- Backend
- Medium
tags:
- '0111'
- rest
- main_quest
- backend
- conceptual
- gamified-learning
keywords:
  primary:
  - '0111'
  - rest
  - main_quest
  secondary:
  - versioning
  - deprecation
  - backward-compatibility
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0111 (7) Quest: Main Quest - API Versioning'
rewards:
  badges:
  - 🏆 Steward of Change - Evolved an API without breaking its clients
  - 📅 Keeper of the Sunset - Designed a graceful deprecation timeline
  skills_unlocked:
  - 🛠️ Versioning Strategy Selection
  - 🧠 Breaking-Change Analysis
  progression_points: 60
  unlocks_features:
  - Access to the API Documentation quest
layout: quest
---
*Greetings, brave adventurer! An API is a promise to everyone who calls it. The moment a client depends on your endpoint, you owe them stability - yet your API must still grow. This tension is the heart of **API Versioning**: how do you change an interface without shattering the systems built on top of it?*

*This quest teaches you to tell a breaking change from a harmless one, to choose between URI versioning (`/v2/users`) and header versioning, to keep old clients working through backward compatibility, and to retire old versions gracefully with a deprecation timeline that no one curses you for.*

## 📖 The Legend Behind This Quest

*Every successful API eventually faces the same crossroads. A new feature demands a new shape for the data; a field must be renamed; an endpoint must split in two. Make the change carelessly and a thousand client applications break at once, support tickets flood in, and trust evaporates. Refuse to change and the API ossifies, unable to grow.*

*The masters learned a third way: evolve additively when you can, version explicitly when you must, and always give clients a long, well-signposted runway before anything is removed. This quest hands you that map.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Breaking vs Non-Breaking** - Classify any change by its impact on clients
- [ ] **Backward Compatibility** - Add features without disturbing existing callers
- [ ] **URI Versioning** - Use `/v1/`, `/v2/` and know its trade-offs
- [ ] **Header / Media-Type Versioning** - Version via `Accept` headers and its trade-offs
- [ ] **Graceful Deprecation** - Sunset an old version with warning headers and a timeline

### Secondary Objectives (Bonus Achievements)
- [ ] **Semantic Versioning** - Apply MAJOR.MINOR.PATCH thinking to APIs
- [ ] **The Robustness Principle** - Be conservative in what you send, liberal in what you accept
- [ ] **Deprecation Headers** - Use the `Deprecation` and `Sunset` HTTP headers

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Look at a proposed change and instantly say "breaking" or "safe"
- [ ] Defend a choice between URI and header versioning for a given API
- [ ] Design a deprecation timeline with clear milestones
- [ ] Add a field to a response and prove it breaks nobody

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] You have completed REST Principles or can design resource URLs
- [ ] You understand HTTP headers
- [ ] You can make requests with curl

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] `curl` available in your terminal
- [ ] Optional: `jq` for inspecting JSON responses
- [ ] An internet connection

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can design and read resource URLs
- [ ] You are ready to reason about change over time
- [ ] Ready for 60-90 minutes of focused learning

## 🌍 Choose Your Adventure Platform

*Versioning is a design discipline. These setups let you observe how real APIs version themselves.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# GitHub versions its API via an Accept header (header versioning)
brew install jq
curl -s -D - -o /dev/null \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/octocat | grep -i 'api-version'
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Send the version header GitHub expects
curl.exe -s -H "X-GitHub-Api-Version: 2022-11-28" `
  https://api.github.com/octocat
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y curl jq
# Compare a URI-versioned call: many APIs expose /v1/ and /v2/ paths
curl -s https://api.github.com/zen   # GitHub root; observe headers and shape
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Any container with curl can probe versioned endpoints
docker run --rm curlimages/curl:latest -s \
  -H "X-GitHub-Api-Version: 2022-11-28" https://api.github.com/octocat
```

</details>

## 🧙‍♂️ Chapter 1: Breaking vs Non-Breaking Changes

*The single most important skill in versioning is knowing whether a change will break clients. Get this right and most changes need no new version at all.*

### ⚔️ Skills You'll Forge in This Chapter
- Classifying changes by client impact
- The robustness principle
- Why additive change is your friend

### 🏗️ Classifying Changes

| Non-breaking (safe, additive) | Breaking (needs a new version) |
| --- | --- |
| Adding a new optional field to a response | Removing or renaming a field |
| Adding a new endpoint | Removing or renaming an endpoint |
| Adding a new optional request parameter | Making an optional parameter required |
| Adding a new enum value (if clients tolerate unknowns) | Changing a field's type or meaning |
| Relaxing a validation rule | Tightening a validation rule |
| | Changing the format of an existing field |

The guiding rule is the **robustness principle** (Postel's Law): *be conservative in what you send, liberal in what you accept.* A well-built client ignores fields it does not recognize, which is exactly what lets you add fields safely.

```bash
# A client should still work when the response GAINS a new field it ignores.
# Old client reads only .id and .name; the new "nickname" field is harmless.
curl -s https://jsonplaceholder.typicode.com/users/1 | jq '{id, name}'
```

If you must make a breaking change, you have only two honest options: never make it, or **version**. The rest of the quest is about doing the latter well.

### 🔍 Knowledge Check: Change Classification
- [ ] Is adding a new optional response field breaking? Why?
- [ ] Is renaming a field breaking? Why?
- [ ] State the robustness principle in your own words.

### ⚡ Quick Wins and Checkpoints
- [ ] **Classified changes**: You sorted a list into breaking and non-breaking
- [ ] **Saw additive safety**: You proved an ignored new field harms nothing

## 🧙‍♂️ Chapter 2: URI vs Header Versioning

*When you must version, you choose where the version lives: in the URL path, or in a header. Each has loud advocates and real trade-offs.*

### ⚔️ Skills You'll Forge in This Chapter
- URI versioning and its trade-offs
- Header and media-type versioning and theirs
- Choosing deliberately

### 🏗️ The Two Main Strategies

**URI versioning** puts the version in the path:

```bash
# Version is visible, explicit, and trivially testable in a browser
curl -s https://api.example.com/v1/users/42
curl -s https://api.example.com/v2/users/42
```

**Header / media-type versioning** keeps the URL stable and selects the version with a header (often `Accept`):

```bash
# Same URL; the Accept header picks the representation version
curl -s https://api.example.com/users/42 \
  -H "Accept: application/vnd.example.v2+json"
```

Compare them:

| | URI versioning (`/v2/`) | Header versioning (`Accept`) |
| --- | --- | --- |
| Visibility | Obvious in logs, browsers, docs | Hidden in headers |
| Caching/routing | Simple - distinct URLs | Needs `Vary: Accept` awareness |
| REST purity | A URL should name a resource, not a version | More "correct" by REST theory |
| Ease for callers | Easiest - just change the path | Requires setting headers |
| Adoption | Most common in practice (GitHub, Stripe, Twilio) | Common in hypermedia-strict APIs |

There is no universally right answer. **URI versioning wins on simplicity and is the most common choice;** header versioning is favored when REST purity and stable URLs matter more. GitHub even uses a **date-based** version (`2022-11-28`) sent in a header - a third pragmatic flavor.

### 🔍 Knowledge Check: Strategies
- [ ] What does URI versioning make easy that header versioning does not?
- [ ] Why does header versioning need attention to the `Vary` header?
- [ ] Name a major API that uses each style.

## 🧙‍♂️ Chapter 3: Backward Compatibility and Graceful Deprecation

*Shipping `v2` is the easy part. The hard part is retiring `v1` without an uprising. Graceful deprecation is a timeline, not an event.*

### ⚔️ Skills You'll Forge in This Chapter
- Maintaining backward compatibility
- The deprecation lifecycle
- The `Deprecation` and `Sunset` headers

### 🏗️ The Deprecation Lifecycle

You keep old versions alive while clients migrate, and you warn loudly before removal. A typical timeline:

```text
1. ANNOUNCE   Publish v2, document the migration, mark v1 "deprecated" in docs.
2. WARN       Every v1 response carries Deprecation and Sunset headers.
3. OVERLAP    Run v1 and v2 side by side for a long, fixed window (e.g. 6-12 months).
4. SUNSET     On the announced date, v1 returns 410 Gone (or 301 to v2 if it can map).
```

The standard HTTP headers make the warning machine-readable so client tooling can flag it automatically:

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Wed, 31 Dec 2026 23:59:59 GMT
Link: <https://api.example.com/v2/users/42>; rel="successor-version"
```

`Deprecation` signals the endpoint is on its way out; `Sunset` gives the exact removal date; the `Link` header points to the replacement. After the sunset date, a removed endpoint should return **`410 Gone`** (it is intentionally gone) rather than a confusing `404`.

Watch a real API advertise its version policy:

```bash
# GitHub echoes the API version it served, helping clients detect drift
curl -s -D - -o /dev/null \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/octocat | grep -i 'github-api-version'
```

Throughout, **backward compatibility** within a version is sacred: once `v1` is published, you only add to it - never break it - until its sunset.

### 🔍 Knowledge Check: Deprecation
- [ ] What do the `Deprecation` and `Sunset` headers each communicate?
- [ ] Why return `410 Gone` instead of `404` for a removed endpoint?
- [ ] Why must changes within a published version be additive only?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Sort the Changes
**Objective**: Classify a list of proposed changes.

**Requirements**:
- [ ] Classify: add field, rename field, add endpoint, make a parameter required, relax validation
- [ ] State which require a new version
- [ ] Justify each using the robustness principle

**Validation**: Every classification matches the breaking/non-breaking table.

### 🟡 Intermediate Challenge: Choose a Strategy
**Objective**: Pick a versioning strategy for two scenarios.

**Requirements**:
- [ ] Choose for a public developer API used by thousands of partners
- [ ] Choose for a strict hypermedia API with stable URLs
- [ ] Justify each choice against the trade-off table

**Validation**: Each choice is defended with at least two trade-offs.

### 🔴 Advanced Challenge: Deprecation Plan
**Objective**: Write a complete deprecation plan for `v1`.

**Requirements**:
- [ ] Define announce, warn, overlap, and sunset milestones with dates
- [ ] Specify the headers each `v1` response will carry
- [ ] State the status code `v1` returns after the sunset date

**Validation**: A client team could plan their migration from your timeline alone.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Steward of Change** - You evolved an API without breaking its clients
- 📅 **Keeper of the Sunset** - You designed a graceful deprecation timeline

**🛠️ Skills Unlocked**:
- **Versioning Strategy Selection** - Choose URI or header versioning deliberately
- **Breaking-Change Analysis** - Judge any change by its client impact

**🔓 Unlocked Quests**:
- API Documentation - Describe your versions and deprecations formally

**📊 Progression Points**: +60 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [API Documentation](/quests/0111/api-documentation/) - Document versions with OpenAPI

**Explore Side Adventures**:
- ⚔️ [Error Handling](/quests/0111/error-handling/) - The `410 Gone` and friends
- ⚔️ [Rate Limiting](/quests/0111/rate-limiting/) - Another contract you must keep

### Character Class Recommendations

**💻 Software Developer**: Continue to [API Documentation](/quests/0111/api-documentation/)  
**🏗️ System Engineer**: Explore [Error Handling](/quests/0111/error-handling/)  
**🛡️ Security Specialist**: Check out [API Authentication](/quests/0111/api-authentication/)

## 📚 Resources

### Official Documentation
- [RFC 9745: The Deprecation HTTP Header Field](https://www.rfc-editor.org/rfc/rfc9745) - Standard deprecation signaling
- [RFC 8594: The Sunset HTTP Header Field](https://www.rfc-editor.org/rfc/rfc8594) - Announcing removal dates
- [MDN: 410 Gone](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/410) - The intentionally-removed status

### Community Resources
- [GitHub: API versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions) - Date-based header versioning in practice
- [Stripe: API versioning](https://docs.stripe.com/api/versioning) - Pinned, dated versions
- [Microsoft REST API Guidelines: Versioning](https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#12-versioning) - Production conventions

### Learning Materials
- [Semantic Versioning](https://semver.org/) - MAJOR.MINOR.PATCH applied to contracts
- [Postel's Law (robustness principle)](https://en.wikipedia.org/wiki/Robustness_principle) - The compatibility mindset
- [Google API Design: Versioning](https://cloud.google.com/apis/design/versioning) - Compatibility rules at scale

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Classified a change and wrote a versioning plan
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0111 - API Development]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Prerequisites:** [[REST Principles: Constraints, Resources, and Richardson Maturity]] **Unlocks:** [[API Documentation: OpenAPI, Swagger, and Contract-First]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
