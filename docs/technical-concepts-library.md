# Technical Concepts Library

> A reference library of engineering concepts (design patterns, programming principles, systems management, DevOps, ITSM, AI-assisted development) mapped to the IT-Journey pillars, with examples from this repository. Line references are as of 2026-10-29.

A reference library of engineering concepts mapped to the IT-Journey pillars. Examples cite real repo files (`path:line`) where they exist; others are marked **General**. Companion docs: [pillars-in-practice.md](pillars-in-practice.md), [kis-kiss-fix.md](kis-kiss-fix.md), [PRD](../PRD.md), [feature catalog](../features/features.yml).

## Table of contents

- [Pillar legend](#pillar-legend)
- [Design patterns](#design-patterns)
- [Programming principles](#programming-principles)
- [Systems management](#systems-management)
- [DevOps lifecycle](#devops-lifecycle)
- [ITSM](#itsm)
- [AI-assisted development](#ai-assisted-development)
- [Index](#index)
- [Subject areas and certifications](#subject-areas-and-certifications)
- [Harnesses and loops for consistency](#harnesses-and-loops-for-consistency)
- [Second brain](#second-brain)
- [To-dos and follow-ups](#to-dos-and-follow-ups)

## Pillar legend

- **DFF-F**: Don't Forget the Fundamentals: hygiene (monitoring, backups, runbooks, pinning, warn-don't-fail).
- **DFF-D**: Designed for Failure (about.md's *Design for Failure*): resilience, graceful degradation, fault tolerance.
- **DRY**: Don't Repeat Yourself.
- **KIS**: Keep It Simple (canonical spelling; KISS is the industry name).
- **REnO-R**: Reduce, Eliminate, Normalize, Optimize: the improvement loop.
- **REnO-E**: Release Early and Often (about.md's reading): shipping cadence.
- **MVP**: Minimum Viable Product.
- **COLAB**: Collaboration.
- **AIPD**: AI-Powered Development.
- **PoLR**: Path of Least Resistance (approach).
- **OSAP**: Open Source As Possible (approach).

## Design patterns

### Singleton

- **Definition:** Ensures a class has exactly one instance with a global access point.
- **When to use:** Use for one truly shared resource such as a config or logger, sparingly.
- **Example:** General: a single `Config` object loaded once per process.
- **Pillars:** KIS

### Factory

- **Definition:** Centralizes object creation behind a method or class so callers don't depend on concrete types.
- **When to use:** Use when the type to build depends on input or configuration.
- **Example:** General: `make_notifier("slack")` returns the right notifier class.
- **Pillars:** DRY, KIS

### Observer

- **Definition:** Subscribers register with a subject and are notified when events occur.
- **When to use:** Use when many components must react to one event without coupling to it.
- **Example:** GitHub Actions `on:` triggers subscribe workflows to repo events, e.g. Quest Idea Intake reacts to `issues: labeled` (`.github/workflows/quest-idea-intake.yml:40-42`).
- **Pillars:** COLAB, DFF-D

### Strategy

- **Definition:** Encapsulates interchangeable algorithms behind one interface, selected at runtime.
- **When to use:** Use when behavior varies by context and you want to swap it without branching everywhere.
- **Example:** Per-step model routing via the `AI_MODEL` env or `model` input (`.github/workflows/README.md:19`).
- **Pillars:** KIS, AIPD

### Decorator

- **Definition:** Wraps an object to add behavior without changing its class.
- **When to use:** Use to layer cross-cutting behavior (logging, caching, auth) onto existing code.
- **Example:** General: a Python `@retry` decorator around an HTTP call.
- **Pillars:** DRY

### Adapter

- **Definition:** Converts one interface into another that clients expect.
- **When to use:** Use to integrate a component whose interface doesn't match yours.
- **Example:** `_plugins/preview_generator.rb` adapts content to the Front Matter CMS `/preview/` mirror (`AGENTS.md:135`).
- **Pillars:** DRY

### Facade

- **Definition:** Provides one simple interface over a complex subsystem.
- **When to use:** Use to give contributors a single entry point to many tools.
- **Example:** Make targets front the build and audit tooling: done means `make build-ci` and `make content-audit` pass (`AGENTS.md:9`, `AGENTS.md:31`).
- **Pillars:** KIS, PoLR

### Proxy

- **Definition:** A stand-in object that controls access to another (lazy loading, caching, access control).
- **When to use:** Use to add access control or caching transparently.
- **Example:** General: a caching HTTP proxy in front of a slow API.
- **Pillars:** DFF-D

### Command

- **Definition:** Encapsulates a request as an object or named action so it can be queued, logged or replayed.
- **When to use:** Use for repeatable, auditable operations.
- **Example:** The `quest-normalize` Make target packages a normalization run as one named command (`Makefile:242-243`).
- **Pillars:** REnO-R, DRY

### Iterator

- **Definition:** Provides sequential access to a collection without exposing its structure.
- **When to use:** Use to traverse data uniformly or lazily.
- **Example:** General: a Python generator yielding quest files one at a time.
- **Pillars:** KIS

### MVC / MVVM

- **Definition:** Separates data (model), presentation (view) and control or binding logic (controller or view-model).
- **When to use:** Use for UI apps where data, display and interaction change independently.
- **Example:** Jekyll splits data (`_data/`), content collections under `pages/` (`_config.yml:634`) and layouts from the remote theme (`_config.yml:36`); an MVC-like split.
- **Pillars:** KIS, DRY

### Repository

- **Definition:** Mediates between domain logic and data storage behind a collection-like interface.
- **When to use:** Use to decouple business logic from persistence.
- **Example:** Loosely, `_data/brand/values.yml` is the single store that guides read from instead of restating values (`_data/brand/values.yml:30-31`).
- **Pillars:** DRY

### Dependency Injection

- **Definition:** Supplies a component's dependencies from outside instead of creating them internally.
- **When to use:** Use to make components testable and configurable.
- **Example:** Workflows inject the model and credentials into the shared `claude-run` action via inputs, env and secrets (`.github/workflows/README.md:19`, `.github/workflows/issue-autopilot.yml:91`).
- **Pillars:** DRY, AIPD

## Programming principles

### Single Responsibility Principle

- **Definition:** A module should have one reason to change.
- **When to use:** Use when a unit mixes unrelated concerns.
- **Example:** Planning is a separate job from acting in `.github/workflows/agent-plan-then-act.yml:7`.
- **Pillars:** KIS

### Open/Closed Principle

- **Definition:** Software should be open for extension but closed for modification.
- **When to use:** Use when adding variants keeps forcing edits to stable code.
- **Example:** General: add a new exporter class instead of editing a switch statement.
- **Pillars:** DRY

### Liskov Substitution Principle

- **Definition:** Subtypes must be usable wherever their base type is expected without breaking behavior.
- **When to use:** Use when designing inheritance hierarchies.
- **Example:** General: a `Square` that breaks `Rectangle.set_width` violates LSP.
- **Pillars:** DFF-D

### Interface Segregation Principle

- **Definition:** Clients should not depend on methods they don't use; prefer small, focused interfaces.
- **When to use:** Use when one interface serves very different clients.
- **Example:** General: split `Printer` and `Scanner` instead of one `Machine` interface.
- **Pillars:** KIS

### Dependency Inversion Principle

- **Definition:** High-level modules depend on abstractions, not concrete implementations.
- **When to use:** Use to decouple policy from mechanism.
- **Example:** `ci.yml` depends on the versioned reusable-workflow interface, not its internals (`.github/workflows/ci.yml:28`).
- **Pillars:** DRY

### DRY

- **Definition:** Every piece of knowledge has one authoritative representation.
- **When to use:** Use whenever logic, config or content would otherwise be copied.
- **Example:** Shared CI and the AI runner are consumed by reference, never copied (`AGENTS.md:152`, `.github/workflows/ci.yml:28`).
- **Pillars:** DRY

### KISS

- **Definition:** Prefer the simplest design that works. The repo's canonical pillar spelling is KIS (see `docs/kis-kiss-fix.md`).
- **When to use:** Use as a default tie-breaker between designs.
- **Example:** `_data/brand/values.yml:32-37` (KIS) and `:72-74` (KISS approach).
- **Pillars:** KIS

### YAGNI

- **Definition:** Don't build functionality until it's actually needed.
- **When to use:** Use when tempted to add speculative features.
- **Example:** General: skip a plugin system until a second plugin exists.
- **Pillars:** MVP, KIS

### Separation of Concerns

- **Definition:** Divide a system so each part addresses a distinct concern.
- **When to use:** Use when changes in one area keep rippling into others.
- **Example:** Content lives in `pages/` collections, theme in `remote_theme`, data in `_data/` (`_config.yml:634`, `_config.yml:36`).
- **Pillars:** KIS, DRY

### Law of Demeter

- **Definition:** A unit should talk only to its immediate collaborators, not reach through chains.
- **When to use:** Use to reduce coupling (avoid `a.b().c().d()`).
- **Example:** General: `order.ship()` instead of `order.customer.address.city`.
- **Pillars:** KIS

### Composition over Inheritance

- **Definition:** Build behavior by combining small parts rather than deep class hierarchies.
- **When to use:** Use when inheritance trees grow brittle.
- **Example:** Workflows compose fleet reusable workflows and actions (`.github/workflows/conformance.yml:23`, `.github/workflows/zer0-doctor.yml:47`).
- **Pillars:** DRY, KIS

### Fail Fast

- **Definition:** Detect and report errors at the earliest point instead of continuing in a bad state.
- **When to use:** Use for validation of inputs and invariants.
- **Example:** Placeholder content fails validation unless `draft: true` (`AGENTS.md:97`); stale generated data fails CI (`AGENTS.md:103`).
- **Pillars:** DFF-F, DFF-D

### Idempotency

- **Definition:** Running an operation many times has the same effect as running it once.
- **When to use:** Use for retries, scheduled jobs and deploys.
- **Example:** `make quest-data` regenerates the same outputs from frontmatter (`AGENTS.md:103`); `concurrency:` guards in `.github/workflows/sync-gh-pages.yml:40`.
- **Pillars:** DFF-D

### Immutability

- **Definition:** Data isn't modified after creation; changes produce new values.
- **When to use:** Use to avoid shared-state bugs, especially with concurrency.
- **Example:** General: Python tuples or frozen dataclasses; immutable release tags.
- **Pillars:** DFF-D, KIS

### Pure functions

- **Definition:** Output depends only on inputs, with no side effects.
- **When to use:** Use for logic that must be easy to test and reason about.
- **Example:** General: `slugify(title)` returns the same slug every time.
- **Pillars:** KIS

### Defensive programming

- **Definition:** Anticipate misuse and bad inputs, and handle them explicitly.
- **When to use:** Use at trust boundaries and with external input.
- **Example:** A run with no credentials is a clean no-op rather than a crash (`.github/workflows/README.md:19`).
- **Pillars:** DFF-D

### Graceful degradation

- **Definition:** Keep partial service when a dependency fails.
- **When to use:** Use for optional features and external services.
- **Example:** Lanes idle green on broken AI credentials so deploys aren't blocked (`.github/workflows/quest-perfection.yml:201`); the About page falls back to a default email (`pages/_about/about.md:151`).
- **Pillars:** DFF-D

### Retries with backoff

- **Definition:** Retry transient failures with growing delays (often with jitter).
- **When to use:** Use for network calls and rate-limited APIs.
- **Example:** Retry-on-next-schedule (`.github/workflows/quest-fix-loop.yml:146`, `.github/workflows/sync-gh-pages.yml:189`) and rebase-and-retry (`.github/workflows/dependabot-auto-merge.yml:130`); there's no explicit exponential backoff (gap).
- **Pillars:** DFF-D

## Systems management

### Monitoring vs observability

- **Definition:** Monitoring watches known signals; observability lets you ask new questions of a system from its logs, metrics and traces.
- **When to use:** Use monitoring for known failure modes and observability for unknown ones.
- **Example:** Scheduled monitors: `.github/workflows/link-checker.yml:13-14`, `.github/workflows/zer0-doctor.yml:33-34`. No tracing or observability stack (general).
- **Pillars:** DFF-F

### SLIs

- **Definition:** Service Level Indicators are measured signals of service health, e.g. success rate or latency.
- **When to use:** Use to quantify reliability.
- **Example:** General: % of requests served under 300 ms.
- **Pillars:** DFF-F

### SLOs

- **Definition:** Service Level Objectives are internal targets for SLIs.
- **When to use:** Use to decide when reliability work beats feature work.
- **Example:** General: 99.9% of page loads succeed per 30 days.
- **Pillars:** DFF-F, REnO-E

### SLAs

- **Definition:** Service Level Agreements are contractual commitments, with penalties, to customers.
- **When to use:** Use when external parties depend on your service.
- **Example:** General: a hosting provider's 99.95% uptime credit policy.
- **Pillars:** DFF-F

### Error budgets

- **Definition:** The allowed unreliability (1 - SLO) that can be spent on change.
- **When to use:** Use to balance release speed against stability.
- **Example:** General: if the budget is exhausted, freeze features and fix reliability.
- **Pillars:** DFF-D, REnO-E

### Incident management

- **Definition:** A structured response to restore service quickly: detect, triage, mitigate, communicate.
- **When to use:** Use whenever users are impacted.
- **Example:** Broken AI credentials are surfaced and tracked by a `quest-loop-health` issue (`.github/workflows/quest-perfection.yml:201`).
- **Pillars:** DFF-D, COLAB

### Runbooks

- **Definition:** Step-by-step operational procedures for known tasks and failures.
- **When to use:** Use for any recurring ops task or alert.
- **Example:** Gap: no site runbooks; they're only planned (`docs/ROADMAP.md:554`) and taught in quests (`_data/quests/network.yml:696`).
- **Pillars:** DFF-F

### Backups and disaster recovery

- **Definition:** Copies of data plus a tested plan to restore service after major loss.
- **When to use:** Use for any data you can't recreate.
- **Example:** Gap: no backup process. General: nightly snapshot plus a quarterly restore test.
- **Pillars:** DFF-F, DFF-D

### RTO / RPO

- **Definition:** Recovery Time Objective (how fast) and Recovery Point Objective (how much data loss) for DR.
- **When to use:** Use to size backup and DR investment.
- **Example:** General: RTO 4 h, RPO 15 min for a primary database.
- **Pillars:** DFF-D

### Capacity planning

- **Definition:** Forecasting the resources needed to meet demand.
- **When to use:** Use before growth events or when nearing limits.
- **Example:** AI lanes hit rate limits and soft-skip (`.github/workflows/quest-video.yml:298`); turn sizing is adaptive (`.github/workflows/quest-perfection.yml:626-629`).
- **Pillars:** DFF-F, REnO-R

### Configuration management

- **Definition:** Keeping system configuration declared, versioned and consistent.
- **When to use:** Use for any environment that must be reproducible.
- **Example:** Site config in `_config.yml`; theme ref at `_config.yml:36`; Dependabot config in `.github/dependabot.yml`.
- **Pillars:** DRY, DFF-F

### Dependency pinning

- **Definition:** Locking dependencies to exact versions or SHAs for reproducibility.
- **When to use:** Use for builds that must be repeatable and supply-chain safe.
- **Example:** Pinned: `standard-ci.yml@v2` (`.github/workflows/ci.yml:28`). Floating: `@main` (`.github/workflows/conformance.yml:23`); no SHA pins (gap).
- **Pillars:** DFF-F

### Secrets management

- **Definition:** Storing and injecting credentials securely, never in code.
- **When to use:** Use for any token, key or password.
- **Example:** `CLAUDE_CODE_OAUTH_TOKEN` comes from repo secrets (`.github/workflows/issue-autopilot.yml:91`).
- **Pillars:** DFF-F

### Least privilege

- **Definition:** Grant only the permissions needed for a task.
- **When to use:** Use for every token, role and workflow.
- **Example:** Explicit `permissions:` blocks (`.github/workflows/ci.yml:19`, `.github/workflows/issue-autopilot.yml:42`).
- **Pillars:** DFF-D

### Zero trust

- **Definition:** Never trust by network location; verify every request's identity and context.
- **When to use:** Use for distributed or remote-access systems.
- **Example:** General: identity-aware proxy with per-request auth instead of a VPN.
- **Pillars:** DFF-D

## DevOps lifecycle

### CI/CD

- **Definition:** Automatically build, test and deliver every change.
- **When to use:** Use on every repo with more than one change a week.
- **Example:** `.github/workflows/ci.yml:28` (fleet standard CI) and main-to-gh-pages delivery (`.github/workflows/sync-gh-pages.yml:146`).
- **Pillars:** REnO-E, DFF-F

### Trunk-based development

- **Definition:** Short-lived branches merged frequently into one main trunk.
- **When to use:** Use to minimize merge pain and release continuously.
- **Example:** Short-lived `feature/`, `fix/` and `docs/` branches off `main` (`AGENTS.md:55`).
- **Pillars:** REnO-E

### Trunk vs branch workflows

- **Definition:** Trunk-based (short branches, fast merges) versus long-lived branch models like GitFlow (release and develop branches).
- **When to use:** Use trunk for continuous delivery; GitFlow for slow, versioned release trains.
- **Example:** it-journey is trunk-style with a deploy branch `gh-pages` (`AGENTS.md:55`, `.github/workflows/sync-gh-pages.yml:146`).
- **Pillars:** REnO-E, KIS

### Feature flags

- **Definition:** Toggle behavior at runtime without redeploying.
- **When to use:** Use to ship dark, ramp gradually or kill-switch risky features.
- **Example:** AI lanes are gated by repo variables such as `CONTENT_FACTORY_ENABLED` (`.github/workflows/content-factory.yml:12`, `AGENTS.md:128`).
- **Pillars:** REnO-E, DFF-D

### Blue-green deployment

- **Definition:** Run two identical environments and switch traffic from old (blue) to new (green) at once.
- **When to use:** Use when you need instant rollback.
- **Example:** General: swap a load-balancer target group after smoke tests.
- **Pillars:** DFF-D, REnO-E

### Canary deployment

- **Definition:** Release to a small slice of traffic first and expand if healthy.
- **When to use:** Use for risky changes with real-user signals.
- **Example:** Closest in-repo analogue is the staged lane ramp (`scripts/ai/README.md:198`); a true traffic canary is general.
- **Pillars:** DFF-D, REnO-E

### Infrastructure as Code

- **Definition:** Define infrastructure in versioned, reviewable code.
- **When to use:** Use for any environment that must be reproducible.
- **Example:** `Dockerfile` and `docker-compose.yml` define the dev environment; no cloud IaC (general: Terraform).
- **Pillars:** DRY, DFF-F

### Chaos engineering

- **Definition:** Deliberately inject failures to verify resilience.
- **When to use:** Use once basics (monitoring, rollback) are solid.
- **Example:** Gap: none in repo. General: kill a random pod in staging weekly.
- **Pillars:** DFF-D

### GitOps

- **Definition:** Git is the source of truth; automation reconciles the live state to it.
- **When to use:** Use for declarative deployments.
- **Example:** The `gh-pages` branch is reconciled from `main` by PR (`.github/workflows/sync-gh-pages.yml:146`).
- **Pillars:** DRY, REnO-E

### Release automation

- **Definition:** Versioning, changelogs and releases produced by tooling, not by hand.
- **When to use:** Use whenever releases are recurring.
- **Example:** release-please (`.github/workflows/release.yml:3-6`; `AGENTS.md:56`).
- **Pillars:** REnO-E

### Semantic versioning

- **Definition:** MAJOR.MINOR.PATCH, signaling breaking, feature and fix changes.
- **When to use:** Use for anything others depend on.
- **Example:** `.release-please-manifest.json` tracks the version; `@v2` refs (`.github/workflows/ci.yml:28`).
- **Pillars:** REnO-E

### Conventional Commits

- **Definition:** Structured commit messages (`feat:`, `fix:`) that drive changelogs and versions.
- **When to use:** Use with automated releases.
- **Example:** `AGENTS.md:55`; `CONTRIBUTING.md:72`.
- **Pillars:** REnO-E, COLAB

### Small PRs and auto-merge

- **Definition:** Merge small, green, in-scope changes automatically.
- **When to use:** Use for low-risk, high-volume changes.
- **Example:** `.github/workflows/content-auto-merge.yml:2`; `.github/workflows/dependabot-auto-merge.yml`.
- **Pillars:** REnO-E, KIS

### Twelve-factor app

- **Definition:** Twelve practices for portable cloud apps (config in env, stateless processes, etc.).
- **When to use:** Use when designing deployable services.
- **Example:** General: read the DB URL from `DATABASE_URL`, not a file in the repo.
- **Pillars:** DRY, KIS

### DORA metrics

- **Definition:** Deployment frequency, lead time for changes, change failure rate and time to restore.
- **When to use:** Use to measure delivery performance.
- **Example:** General: no DORA tracking in repo (gap).
- **Pillars:** REnO-E, DFF-D

## ITSM

### ITIL overview

- **Definition:** ITIL 4 is a framework of service-management practices organized around a service value system.
- **When to use:** Use as a shared vocabulary for running IT services.
- **Example:** General: map tickets to incident, request and change practices.
- **Pillars:** DFF-F, COLAB

### Change management (change enablement)

- **Definition:** Assess, authorize and schedule changes to reduce risk.
- **When to use:** Use for any production change.
- **Example:** Every change goes through a reviewed PR (`AGENTS.md:9`); `needs-human` forces manual handling (`AGENTS.md:52`).
- **Pillars:** COLAB, DFF-D

### Problem vs incident

- **Definition:** An incident is a service disruption to restore now; a problem is its underlying cause to fix permanently.
- **When to use:** Use to separate firefighting from root-cause work.
- **Example:** General: restart the service (incident), then fix the memory leak (problem).
- **Pillars:** DFF-D, REnO-R

### Service request management

- **Definition:** Handling standard, pre-approved user requests.
- **When to use:** Use for routine asks with a known path.
- **Example:** Issue forms such as `.github/ISSUE_TEMPLATE/quest-idea.yml` route requests to Quest Idea Intake.
- **Pillars:** COLAB

### Knowledge management

- **Definition:** Capturing and sharing information so it's reusable.
- **When to use:** Use to cut repeat questions and onboarding time.
- **Example:** `docs/`, `AGENTS.md` and this library; generated `docs/reference/make-targets.md` (`AGENTS.md:31`).
- **Pillars:** DRY, COLAB

### Continual improvement

- **Definition:** An ongoing cycle of measuring and improving services.
- **When to use:** Use as the default operating rhythm.
- **Example:** Normalizers and consolidations (`Makefile:242`, `.github/workflows/content-auto-merge.yml:4-5`).
- **Pillars:** REnO-R

### CMDB

- **Definition:** Configuration Management Database: an inventory of configuration items and their relationships.
- **When to use:** Use when you must understand impact across many systems.
- **Example:** Closest analogue: the hub's project registry `_data/projects.yml` (`AGENTS.md:152`) and the agent registry `_data/agents/registry.yml`.
- **Pillars:** DRY, DFF-F

### On-call rotation

- **Definition:** A schedule of who responds to alerts and when.
- **When to use:** Use for any service with users outside business hours.
- **Example:** General: weekly primary and secondary rotation with escalation policy.
- **Pillars:** DFF-F, COLAB

### Postmortems

- **Definition:** Blameless written reviews of incidents: timeline, causes, actions.
- **When to use:** Use after every significant incident.
- **Example:** General: postmortem doc with 5-whys and owned action items. Git archaeology reports are a related practice (`docs/git-archaeology/000-first-steps/report.md`).
- **Pillars:** DFF-D, COLAB, REnO-R

## AI-assisted development

### Prompt engineering

- **Definition:** Designing instructions and context to get reliable model output.
- **When to use:** Use whenever a model is part of a workflow.
- **Example:** Reusable prompts in `.github/prompts/` and instruction files in `.github/instructions/`.
- **Pillars:** AIPD, DRY

### Agentic workflows

- **Definition:** AI agents plan and act in multiple steps with tools, under policy.
- **When to use:** Use for multi-step tasks with clear guardrails.
- **Example:** Plan-then-act pipeline (`.github/workflows/agent-plan-then-act.yml:4-7`); issue autopilot (`.github/workflows/issue-autopilot.yml:113`).
- **Pillars:** AIPD, COLAB

### Human-in-the-loop review

- **Definition:** A person approves AI output before it takes effect.
- **When to use:** Use for anything shipped to users.
- **Example:** A reviewer merges the PR (`AGENTS.md:9`); `human-review` and `needs-human` labels (`AGENTS.md:52`); autonomy policy in `_data/agents/autonomy-matrix.yml`.
- **Pillars:** AIPD, COLAB

### AI-generated code review

- **Definition:** Models review diffs for bugs, style and standards.
- **When to use:** Use as a first-pass reviewer, not the final gate.
- **Example:** `content-review.yml` and `agentic-quest-review.yml` lanes; rules in `.github/instructions/ai-content-review.instructions.md`.
- **Pillars:** AIPD, COLAB

### Evals for AI output

- **Definition:** Systematic scoring of model output against criteria or tests.
- **When to use:** Use before trusting or changing a model or prompt.
- **Example:** Quests are scored by `test/quest-validator/agentic_validate.py` and overruns are recorded as scored fails (`.github/workflows/quest-perfection.yml:629-631`).
- **Pillars:** AIPD, DFF-D

## Index

| Concept | Domain | Pillars |
|---|---|---|
| [Singleton](#singleton) | Design patterns | KIS |
| [Factory](#factory) | Design patterns | DRY, KIS |
| [Observer](#observer) | Design patterns | COLAB, DFF-D |
| [Strategy](#strategy) | Design patterns | KIS, AIPD |
| [Decorator](#decorator) | Design patterns | DRY |
| [Adapter](#adapter) | Design patterns | DRY |
| [Facade](#facade) | Design patterns | KIS, PoLR |
| [Proxy](#proxy) | Design patterns | DFF-D |
| [Command](#command) | Design patterns | REnO-R, DRY |
| [Iterator](#iterator) | Design patterns | KIS |
| [MVC / MVVM](#mvc--mvvm) | Design patterns | KIS, DRY |
| [Repository](#repository) | Design patterns | DRY |
| [Dependency Injection](#dependency-injection) | Design patterns | DRY, AIPD |
| [Single Responsibility Principle](#single-responsibility-principle) | Programming principles | KIS |
| [Open/Closed Principle](#openclosed-principle) | Programming principles | DRY |
| [Liskov Substitution Principle](#liskov-substitution-principle) | Programming principles | DFF-D |
| [Interface Segregation Principle](#interface-segregation-principle) | Programming principles | KIS |
| [Dependency Inversion Principle](#dependency-inversion-principle) | Programming principles | DRY |
| [DRY](#dry) | Programming principles | DRY |
| [KISS](#kiss) | Programming principles | KIS |
| [YAGNI](#yagni) | Programming principles | MVP, KIS |
| [Separation of Concerns](#separation-of-concerns) | Programming principles | KIS, DRY |
| [Law of Demeter](#law-of-demeter) | Programming principles | KIS |
| [Composition over Inheritance](#composition-over-inheritance) | Programming principles | DRY, KIS |
| [Fail Fast](#fail-fast) | Programming principles | DFF-F, DFF-D |
| [Idempotency](#idempotency) | Programming principles | DFF-D |
| [Immutability](#immutability) | Programming principles | DFF-D, KIS |
| [Pure functions](#pure-functions) | Programming principles | KIS |
| [Defensive programming](#defensive-programming) | Programming principles | DFF-D |
| [Graceful degradation](#graceful-degradation) | Programming principles | DFF-D |
| [Retries with backoff](#retries-with-backoff) | Programming principles | DFF-D |
| [Monitoring vs observability](#monitoring-vs-observability) | Systems management | DFF-F |
| [SLIs](#slis) | Systems management | DFF-F |
| [SLOs](#slos) | Systems management | DFF-F, REnO-E |
| [SLAs](#slas) | Systems management | DFF-F |
| [Error budgets](#error-budgets) | Systems management | DFF-D, REnO-E |
| [Incident management](#incident-management) | Systems management | DFF-D, COLAB |
| [Runbooks](#runbooks) | Systems management | DFF-F |
| [Backups and disaster recovery](#backups-and-disaster-recovery) | Systems management | DFF-F, DFF-D |
| [RTO / RPO](#rto--rpo) | Systems management | DFF-D |
| [Capacity planning](#capacity-planning) | Systems management | DFF-F, REnO-R |
| [Configuration management](#configuration-management) | Systems management | DRY, DFF-F |
| [Dependency pinning](#dependency-pinning) | Systems management | DFF-F |
| [Secrets management](#secrets-management) | Systems management | DFF-F |
| [Least privilege](#least-privilege) | Systems management | DFF-D |
| [Zero trust](#zero-trust) | Systems management | DFF-D |
| [CI/CD](#cicd) | DevOps lifecycle | REnO-E, DFF-F |
| [Trunk-based development](#trunk-based-development) | DevOps lifecycle | REnO-E |
| [Trunk vs branch workflows](#trunk-vs-branch-workflows) | DevOps lifecycle | REnO-E, KIS |
| [Feature flags](#feature-flags) | DevOps lifecycle | REnO-E, DFF-D |
| [Blue-green deployment](#blue-green-deployment) | DevOps lifecycle | DFF-D, REnO-E |
| [Canary deployment](#canary-deployment) | DevOps lifecycle | DFF-D, REnO-E |
| [Infrastructure as Code](#infrastructure-as-code) | DevOps lifecycle | DRY, DFF-F |
| [Chaos engineering](#chaos-engineering) | DevOps lifecycle | DFF-D |
| [GitOps](#gitops) | DevOps lifecycle | DRY, REnO-E |
| [Release automation](#release-automation) | DevOps lifecycle | REnO-E |
| [Semantic versioning](#semantic-versioning) | DevOps lifecycle | REnO-E |
| [Conventional Commits](#conventional-commits) | DevOps lifecycle | REnO-E, COLAB |
| [Small PRs and auto-merge](#small-prs-and-auto-merge) | DevOps lifecycle | REnO-E, KIS |
| [Twelve-factor app](#twelve-factor-app) | DevOps lifecycle | DRY, KIS |
| [DORA metrics](#dora-metrics) | DevOps lifecycle | REnO-E, DFF-D |
| [ITIL overview](#itil-overview) | ITSM | DFF-F, COLAB |
| [Change management (change enablement)](#change-management-change-enablement) | ITSM | COLAB, DFF-D |
| [Problem vs incident](#problem-vs-incident) | ITSM | DFF-D, REnO-R |
| [Service request management](#service-request-management) | ITSM | COLAB |
| [Knowledge management](#knowledge-management) | ITSM | DRY, COLAB |
| [Continual improvement](#continual-improvement) | ITSM | REnO-R |
| [CMDB](#cmdb) | ITSM | DRY, DFF-F |
| [On-call rotation](#on-call-rotation) | ITSM | DFF-F, COLAB |
| [Postmortems](#postmortems) | ITSM | DFF-D, COLAB, REnO-R |
| [Prompt engineering](#prompt-engineering) | AI-assisted development | AIPD, DRY |
| [Agentic workflows](#agentic-workflows) | AI-assisted development | AIPD, COLAB |
| [Human-in-the-loop review](#human-in-the-loop-review) | AI-assisted development | AIPD, COLAB |
| [AI-generated code review](#ai-generated-code-review) | AI-assisted development | AIPD, COLAB |
| [Evals for AI output](#evals-for-ai-output) | AI-assisted development | AIPD, DFF-D |
## Subject areas and certifications

A knowledge-base index. Exam codes appear only where I'm confident; otherwise they're left out. **None of the names or codes below were web-verified in this pass**, so check them against the vendor pages before publishing (see To-dos).

### 1. Cloud architecture

Designing scalable, resilient, cost-aware systems on public cloud and Kubernetes.

- **Concepts:** [Infrastructure as Code](#infrastructure-as-code), [Twelve-factor app](#twelve-factor-app), [Blue-green deployment](#blue-green-deployment), [Canary deployment](#canary-deployment), [Zero trust](#zero-trust), [Least privilege](#least-privilege), [Capacity planning](#capacity-planning), [Backups and disaster recovery](#backups-and-disaster-recovery), [RTO / RPO](#rto--rpo)
- **Certifications:** AWS Certified Solutions Architect – Associate (SAA-C03); AWS Certified Solutions Architect – Professional (SAP-C02); AWS Certified DevOps Engineer – Professional (DOP-C02); Microsoft Certified: Azure Solutions Architect Expert (AZ-305, with AZ-104 as prerequisite); Microsoft Certified: DevOps Engineer Expert (AZ-400); Google Cloud Professional Cloud Architect; CNCF Certified Kubernetes Administrator (CKA), Certified Kubernetes Application Developer (CKAD), Certified Kubernetes Security Specialist (CKS); HashiCorp Certified: Terraform Associate (code omitted; versions change).
- **Sources:** [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/), [Azure Architecture Center](https://learn.microsoft.com/azure/architecture/), [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework), [Kubernetes docs](https://kubernetes.io/docs/), [CNCF certification](https://www.cncf.io/training/certification/), [Terraform docs](https://developer.hashicorp.com/terraform/docs)
- **Pillars:** DFF-D, DRY, KIS, OSAP

### 2. DevOps and CI/CD

Delivering change quickly and safely through automation and feedback.

- **Concepts:** [CI/CD](#cicd), [Trunk-based development](#trunk-based-development), [Trunk vs branch workflows](#trunk-vs-branch-workflows), [Feature flags](#feature-flags), [GitOps](#gitops), [Release automation](#release-automation), [Semantic versioning](#semantic-versioning), [Conventional Commits](#conventional-commits), [Small PRs and auto-merge](#small-prs-and-auto-merge), [DORA metrics](#dora-metrics), [Chaos engineering](#chaos-engineering)
- **Certifications:** DevOps Institute DevOps Foundation (DevOps Institute is now part of PeopleCert); GitHub Foundations, GitHub Actions, GitHub Advanced Security, GitHub Administration, GitHub Copilot; GitLab certifications (e.g. GitLab Certified Associate); AWS DevOps Engineer – Professional and Azure DevOps Engineer Expert (see area 1).
- **Sources:** [DORA research](https://dora.dev/) and the [State of DevOps reports](https://dora.dev/research/), [GitHub certifications](https://resources.github.com/learn/certifications/), [GitLab certifications](https://about.gitlab.com/learn/certifications/public/), [Twelve-Factor App](https://12factor.net/), [Conventional Commits](https://www.conventionalcommits.org/), [SemVer](https://semver.org/)
- **Pillars:** REnO-E, REnO-R, DFF-D, COLAB

### 3. Security

Protecting systems, data and identities across the lifecycle.

- **Concepts:** [Least privilege](#least-privilege), [Zero trust](#zero-trust), [Secrets management](#secrets-management), [Dependency pinning](#dependency-pinning), [Defensive programming](#defensive-programming), [Fail Fast](#fail-fast)
- **Certifications:** CompTIA Security+ (SY0-701); ISC2 CISSP; EC-Council Certified Ethical Hacker (CEH; version omitted); OffSec OSCP (course PEN-200; now branded OSCP+ for newer holders).
- **Sources:** [OWASP Top 10](https://owasp.org/www-project-top-ten/), [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), [NIST CSF 2.0](https://www.nist.gov/cyberframework), [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- **Pillars:** DFF-F, DFF-D, KIS

### 4. IT service management

Running IT as a set of services with defined practices for incidents, changes and requests.

- **Concepts:** [ITIL overview](#itil-overview), [Change management (change enablement)](#change-management-change-enablement), [Problem vs incident](#problem-vs-incident), [Incident management](#incident-management), [Service request management](#service-request-management), [Knowledge management](#knowledge-management), [Continual improvement](#continual-improvement), [CMDB](#cmdb), [On-call rotation](#on-call-rotation), [Postmortems](#postmortems), [Runbooks](#runbooks), [SLAs](#slas)
- **Certifications:** ITIL 4 Foundation (PeopleCert, which owns Axelos); CompTIA Tech+ (replaced ITF+; code omitted); CompTIA A+ (Core 1 and Core 2; series codes omitted because a new series rolled out recently).
- **Sources:** [ITIL 4 (PeopleCert)](https://www.peoplecert.org/browse-certifications/it-governance-and-service-management/ITIL-1), [CompTIA certifications](https://www.comptia.org/certifications)
- **Pillars:** DFF-F, COLAB, REnO-R

### 5. Data and databases

Storing, querying and moving data with SQL, NoSQL and data pipelines.

- **Concepts:** [Repository](#repository), [Idempotency](#idempotency), [Immutability](#immutability), [Backups and disaster recovery](#backups-and-disaster-recovery), [RTO / RPO](#rto--rpo) (more entries needed; see To-dos)
- **Certifications:** Google Data Analytics Professional Certificate (Coursera); AWS Certified Data Engineer – Associate (DEA-C01); Microsoft Certified: Azure Data Fundamentals (DP-900).
- **Sources:** [PostgreSQL docs](https://www.postgresql.org/docs/), [SQLite docs](https://www.sqlite.org/docs.html), [MongoDB docs](https://www.mongodb.com/docs/), [Google Data Analytics certificate](https://grow.google/certificates/data-analytics/)
- **Pillars:** DRY, DFF-F, KIS

### 6. Programming fundamentals

Core CS: data structures, algorithms, design and clean code.

- **Concepts:** all [Design patterns](#design-patterns) and [Programming principles](#programming-principles), e.g. [Single Responsibility Principle](#single-responsibility-principle), [Pure functions](#pure-functions), [YAGNI](#yagni), [Iterator](#iterator)
- **Certifications:** Harvard CS50 certificates (free via edX); Oracle Certified Professional: Java SE 21 Developer (1Z0-830). Microsoft C#: the old MCSD exam 70-483 is retired with no direct replacement exam; the current option is the *Foundational C# with Microsoft* certificate (with freeCodeCamp).
- **Sources:** [Harvard CS50](https://cs50.harvard.edu/), [Oracle Java certification](https://education.oracle.com/java-certification), [Microsoft Learn C#](https://learn.microsoft.com/dotnet/csharp/), [Refactoring.Guru patterns](https://refactoring.guru/design-patterns)
- **Pillars:** KIS, DRY, MVP

### 7. AI and machine learning

Building, evaluating and safely using ML models and AI assistants.

- **Concepts:** [Prompt engineering](#prompt-engineering), [Agentic workflows](#agentic-workflows), [Human-in-the-loop review](#human-in-the-loop-review), [AI-generated code review](#ai-generated-code-review), [Evals for AI output](#evals-for-ai-output), [Strategy](#strategy)
- **Certifications:** AWS Certified Machine Learning – Specialty (MLS-C01; retirement status not verified); AWS Certified Machine Learning Engineer – Associate (MLA-C01); Google Cloud Professional Machine Learning Engineer.
- **Sources:** [Anthropic prompt engineering guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview), [GitHub Copilot docs](https://docs.github.com/copilot), [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [AWS certification](https://aws.amazon.com/certification/), [Google Cloud certification](https://cloud.google.com/learn/certification)
- **Pillars:** AIPD, COLAB, DFF-D

### 8. Systems administration and networking

Operating hosts and networks: Linux, TCP/IP, routing, monitoring.

- **Concepts:** [Monitoring vs observability](#monitoring-vs-observability), [Configuration management](#configuration-management), [Capacity planning](#capacity-planning), [Runbooks](#runbooks), [Secrets management](#secrets-management)
- **Certifications:** CompTIA Network+ (N10-009); Linux Foundation Certified System Administrator (LFCS); Cisco CCNA (200-301).
- **Sources:** [Linux Foundation certification](https://training.linuxfoundation.org/certification/), [Cisco CCNA](https://www.cisco.com/site/us/en/learn/training-certifications/certifications/enterprise/ccna/index.html), [IETF RFCs](https://www.rfc-editor.org/)
- **Pillars:** DFF-F, OSAP, PoLR

### 9. Project and agile management

Planning and delivering work iteratively with teams.

- **Concepts:** [YAGNI](#yagni), [Small PRs and auto-merge](#small-prs-and-auto-merge), [Continual improvement](#continual-improvement), [Change management (change enablement)](#change-management-change-enablement)
- **Certifications:** PMI Project Management Professional (PMP); Scrum Alliance Certified ScrumMaster (CSM); SAFe certifications from Scaled Agile (e.g. SAFe Agilist).
- **Sources:** [PMI PMP](https://www.pmi.org/certifications/project-management-pmp), [Scrum Alliance CSM](https://www.scrumalliance.org/get-certified/scrum-master-track/certified-scrummaster), [Scaled Agile](https://scaledagile.com/), [Scrum Guide](https://scrumguides.org/)
- **Pillars:** MVP, REnO-E, COLAB

### Subject area summary

| Area | Cert count | Pillars |
|---|---|---|
| Cloud architecture | 10 | DFF-D, DRY, KIS, OSAP |
| DevOps and CI/CD | 7 (+2 shared with area 1) | REnO-E, REnO-R, DFF-D, COLAB |
| Security | 4 | DFF-F, DFF-D, KIS |
| IT service management | 3 | DFF-F, COLAB, REnO-R |
| Data and databases | 3 | DRY, DFF-F, KIS |
| Programming fundamentals | 3 | KIS, DRY, MVP |
| AI and machine learning | 3 | AIPD, COLAB, DFF-D |
| Systems administration and networking | 3 | DFF-F, OSAP, PoLR |
| Project and agile management | 3 | MVP, REnO-E, COLAB |

## Harnesses and loops for consistency

Automations that keep library concepts consistently covered in quests and docs. **All five are proposed and not yet built.**

### 1. Weekly concept-coverage check (proposed)

- **What it does:** For each library entry, searches `pages/_quests/` and `docs/` for its name and aliases, then reports concepts with no coverage.
- **How it runs:** a weekly cron in a new `.github/workflows/concept-coverage.yml` that calls `scripts/validation/concept_coverage.py` and files or updates one tracking issue.
- **Output:** a coverage table (concept → quests/docs) plus a gap list.
- **Builds on:** the weekly cron pattern in `.github/workflows/zer0-doctor.yml:33-34` and `.github/workflows/link-checker.yml:13-14`.

### 2. Quest-to-concept mapping loop (proposed)

- **What it does:** Quests declare the concepts they teach in a new front-matter key, `concepts: [cicd, idempotency]` (library anchors), and a lint checks every anchor against the Index.
- **How it runs:** on PRs touching `pages/_quests/**`, as a step in the existing quest validation; `make quest-normalize` adds an empty `concepts:` key.
- **Output:** a PR check failing on unknown anchors, plus generated concept-to-quest data.
- **Builds on:** `.github/workflows/quest-validation.yml:3-20` (PR paths plus weekly cron), `Makefile:242-243` (`quest-normalize`), `.github/workflows/frontmatter-validation.yml:17-22`, and `make quest-data` (`AGENTS.md:103`).

### 3. New-quest intake check (proposed)

- **What it does:** Requires at least one library concept link on new quest ideas and drafts.
- **How it runs:** an extra field in `.github/ISSUE_TEMPLATE/quest-idea.yml`, validated by Quest Idea Intake when the `quest-idea` label is applied.
- **Output:** an intake comment asking for a concept when one is missing.
- **Builds on:** `.github/workflows/quest-idea-intake.yml:40-42` and `.github/ISSUE_TEMPLATE/quest-idea.yml:9`.

### 4. Doc-consistency check (proposed)

- **What it does:** Links plain concept mentions to library entries and flags pillar drift, such as KIS vs KISS or a wrong expansion, using `_data/brand/values.yml` as the source of truth.
- **How it runs:** on PRs touching `pages/**` or `docs/**`, as a step in `.github/workflows/content-quality.yml:27-32` or the fleet conformance run.
- **Output:** a PR annotation per drift, with a suggested fix.
- **Builds on:** `_data/brand/values.yml:32`, `.github/instructions/brand.instructions.md:38`, `.github/workflows/conformance.yml:23` and [kis-kiss-fix.md](kis-kiss-fix.md).

### 5. Quarterly certification-freshness check (proposed)

- **What it does:** Fetches each vendor certification page listed above and flags renamed, retired or re-coded exams.
- **How it runs:** a quarterly cron in a new `cert-freshness.yml` (optionally through the `claude-run` action for summarization) that opens a PR with proposed edits.
- **Output:** a PR updating "Subject areas and certifications", reviewed by a human.
- **Builds on:** the AI runner (`.github/workflows/README.md:19`) and the link checker (`.github/workflows/link-checker.yml`).

| Harness | Trigger | Builds on | Status |
|---|---|---|---|
| Concept coverage | Weekly cron | `zer0-doctor.yml`, `link-checker.yml` | Proposed |
| Quest-to-concept mapping | Quest PRs | `quest-validation.yml`, `Makefile:242` | Proposed |
| New-quest intake | `quest-idea` label | `quest-idea-intake.yml` | Proposed |
| Doc consistency | Content PRs | `values.yml`, `content-quality.yml` | Proposed |
| Cert freshness | Quarterly cron | `claude-run`, `link-checker.yml` | Proposed |

## Second brain

**Requirement (proposed):** the repo's concepts, techniques, exercises, quests and docs are documented, tracked and distilled into a second brain (an Obsidian vault), with Claude as the engine that builds and maintains it.

1. **What gets distilled:** this library (one note per concept), quests (`pages/_quests/`), `PRD.md`, `features/features.yml` and [pillars-in-practice.md](pillars-in-practice.md).
2. **How Claude builds it:** a scheduled or on-demand workflow (proposed name: `second-brain.yml`) that uses the shared `claude-run` action (`.github/workflows/issue-autopilot.yml:113` shows the call pattern) and `scripts/ai/` usage tracking. It reads the repo and creates or updates notes with `[[wikilinks]]`, tags and backlinks, and it's opt-in behind a `SECOND_BRAIN_ENABLED` switch like the other lanes (`AGENTS.md:128`).
3. **How it stays in sync:** it runs on push to `main` (paths filter: `pages/_quests/**`, `docs/**`, `PRD.md`, `features/**`) and weekly. It flags drift: notes whose `source_sha` is stale, orphaned notes whose source was deleted, and broken wikilinks. It's PR-only, and a human reviews and merges (`AGENTS.md:9`).
4. **Output format:** Obsidian-compatible Markdown with YAML front matter.

```markdown
---
title: Idempotency
aliases: [idempotent, safe retry]
source_path: docs/technical-concepts-library.md
source_sha: <git blob sha>
pillars: [DFF-D]
concepts: [idempotency, retries-with-backoff]
tags: [principle, devops]
updated: 2026-10-29
---
# Idempotency
Running an operation many times has the same effect as once.
Related: [[Retries with backoff]] · Taught in: [[Quest - ...]]
```

Vault layout: `Concepts/`, `Quests/`, `Docs/`, `Pillars/`, `Certifications/`, `MOCs/` (maps of content), `_meta/drift-report.md`.

**Where the vault lives (open question):** (a) a folder in this repo (e.g. `second-brain/`, excluded from the Jekyll build), or (b) a separate repo, e.g. `bamr87/it-journey-brain`.

**Acceptance criteria:**
- Every library entry, quest, PRD section and feature has exactly one note with `source_path` and `source_sha`.
- Zero broken wikilinks in a clean run, and the drift report lists stale and orphaned notes.
- Runs only through PRs; nothing is pushed directly; the switch defaults to off.
- The vault opens in Obsidian with a working graph view and backlinks.
## To-dos and follow-ups

Goal: make this a living, one-stop software-engineering reference for the it-journey repo and site. Nothing below is done yet.

### 1. Gaps to fill

- [ ] Data structures and algorithms (arrays, hash maps, trees, graphs, Big-O, sorting/search). Owner: Content & Comms bot.
- [ ] Networking fundamentals (OSI/TCP-IP, DNS, HTTP/TLS, subnetting, load balancing). Owner: Content & Comms bot.
- [ ] Databases and SQL (normalization, indexes, transactions/ACID, CAP, NoSQL models). Owner: Content & Comms bot.
- [ ] Security and the OWASP Top 10 (one entry per category, threat modeling, supply-chain security). Owner: Content & Comms bot.
- [ ] Testing strategies: unit, integration, e2e, contract, property-based, mutation, a11y. Owner: Content & Comms bot.
- [ ] API design: REST, GraphQL, versioning, pagination, idempotency keys. Owner: Content & Comms bot.
- [ ] Performance profiling (profilers, flame graphs, caching, Core Web Vitals). Owner: Content & Comms bot.
- [ ] Accessibility (WCAG 2.2 principles and levels). Owner: Content & Comms bot.
- [ ] Documentation standards: Diátaxis and ADRs. Owner: Content & Comms bot.
- [ ] Other gaps spotted: concurrency/async, containers and Kubernetes basics, logging/tracing (OpenTelemetry), cost/FinOps, licensing (ties to OSAP). Owner: Content & Comms bot.

### 2. Process for adding concepts

- [ ] Create a `library` label (it doesn't exist; `gh label list -R bamr87/it-journey` shows only `docs`, `collection/docs` and `collection:docs`). Owner: Amr to approve.
- [ ] Document the intake rule: file additions as an issue labeled `library`, or open a docs PR editing this file. Use this template:

```markdown
### Concept name

- **Definition:** 1–2 sentences.
- **When to use:** 1 sentence.
- **Example:** it-journey `path:line` if real, otherwise "General: ...".
- **Pillars:** DFF-F | DFF-D | DRY | KIS | REnO-R | REnO-E | MVP | COLAB | AIPD | PoLR | OSAP
```

- [ ] Add a matching issue form in `.github/ISSUE_TEMPLATE/` (pattern: `quest-idea.yml`). Owner: Sites bot.

### 3. Surfacing on the site

- [ ] Publish a Jekyll page at `pages/_about/library.md` with `permalink: /about/library/` (matching `pages/_about/about.md:4` `/about/` and the `/about/features/` pattern). Alternatively, use a root `/library/` permalink. Render from this doc, or move the doc there and point `docs/` at it. Owner: Sites bot.
- [ ] Add a nav child under About in `_data/navigation/main.yml:45-51` (next to Features and Contributing). Owner: Sites bot.
- [ ] Link it from the About page body (`pages/_about/about.md`). Owner: Sites bot; Amr to approve copy.
- [ ] Footer link: there's no footer nav data file in this repo (only `skip_footer` text in `_data/ui-text.yml:9`). The footer comes from the remote `zer0-mistakes` theme (`_config.yml:36`), so find the theme's footer data hook or override `_includes/footer.html`. Owner: Sites bot.

### 4. Maintenance

- [ ] Quarterly review: add concepts, refresh `path:line` examples (line numbers drift), retire stale entries. Owner: Content & Comms bot; Amr to approve.
- [ ] A scheduled reminder issue each quarter (cron workflow or a fleet routine). Owner: Sites bot.
- [ ] Keep the certification list current as vendors update their programs: a quarterly check of each vendor's cert page, tied to the quarterly review. Also verify every code in this pass, since none were web-verified. Owner: Content & Comms bot.

### 5. Cross-linking

- [ ] Link each entry to related it-journey docs and quests, `PRD.md`, [pillars-in-practice.md](pillars-in-practice.md) and the feature catalog. Owner: Content & Comms bot.
- [ ] Propose a new feature-catalog entry `FR-ITJ-016` "Technical concepts library" in `features/features.yml` (014 and 015 are taken by #870, #871 and #875), then run prd-sync. Owner: Amr to approve.

### 6. Harnesses

- [ ] Build harness 1, weekly concept coverage. Owner: Sites bot.
- [ ] Build harness 2: add a `concepts:` front-matter key and lint it. Owner: Sites bot; Amr to approve the schema.
- [ ] Build harness 3: a concept field in the quest-idea form. Owner: Sites bot.
- [ ] Build harness 4, the doc-consistency / pillar-drift check (apply [kis-kiss-fix.md](kis-kiss-fix.md) first). Owner: Sites bot.
- [ ] Build harness 5, quarterly cert freshness. Owner: Sites bot.

### 7. Second brain

- [ ] Decide where the vault lives (in-repo folder vs separate repo). Owner: Amr.
- [ ] Propose requirement `FR-ITJ-017` "Second brain (Obsidian vault) built by Claude" for the PRD and feature catalog (proposal only; not added). Owner: Amr to approve.
- [ ] Build the opt-in `second-brain.yml` lane with a drift report, PR-only. Owner: Sites bot.

### 8. JEV

- [ ] Build JEV, the AI agent logic engine (future). It answers questions across the library, validates quest logic and drives the harnesses above, and it would consume the second-brain vault as its knowledge graph. Roadmap item: [PRD §7 ROAD, JEV row](../PRD.md#7-road-roadmap), and as a harness-level orchestration component alongside `scripts/ai/`, `.github/instructions/`, `claude-run` and the agent workflows: [PRD §3, AI Orchestration Components](../PRD.md#ai-orchestration-components). Owner: Amr.
- [ ] Mirror the JEV roadmap and component rows into `scripts/prd-machine/prd-machine.py` (`generate_section_road` at :804-817 hardcodes the roadmap), or the next PRD Machine run will drop them. Owner: Amr to approve.
