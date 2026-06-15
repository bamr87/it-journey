---
title: 'Distributed Tracing with Jaeger & OpenTelemetry'
author: IT-Journey Team
description: 'Instrument a Python service with OpenTelemetry, emit spans to Jaeger, propagate trace context, and debug latency across your microservices.'
excerpt: Follow a single request across services with spans, traces, OpenTelemetry, and Jaeger
preview: images/previews/distributed-tracing-jaeger-quest-title-opentelemet.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1010'
difficulty: 🔴 Hard
estimated_time: 90-120 minutes
primary_technology: opentelemetry
quest_type: main_quest
quest_series: Observability Mastery
quest_line: The Warrior's Watchtower
quest_arc: Mastering the Traces Pillar
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/1010/monitoring-fundamentals/
  unlocks_quests:
  - /quests/1010/alerting-systems/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Comfort on the command line and reading YAML
  - The three pillars of observability (metrics, logs, traces)
  - Basic Python and how HTTP services call one another
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Python 3.10+ with pip and venv, plus Docker for Jaeger
  - A terminal and a text editor or IDE (VS Code recommended)
  skill_level_indicators:
  - Can build and run a small Python service
  - Ready to reason about latency spread across multiple services
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A multi-span trace visible in the Jaeger UI
  skill_demonstrations:
  - Can instrument a service with OpenTelemetry and emit spans
  - Can read a trace waterfall and locate the slow span
  knowledge_checks:
  - Understands spans, traces, trace context, and propagation
  - Can describe head versus tail sampling trade-offs
permalink: /quests/1010/distributed-tracing/
categories:
- Quests
- DevOps
- Hard
tags:
- '1010'
- jaeger
- opentelemetry
- main_quest
- devops
- hands-on
- gamified-learning
keywords:
  primary:
  - '1010'
  - jaeger
  - opentelemetry
  secondary:
  - spans-traces
  - context-propagation
  - sampling
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1010 (10) Quest: Main Quest - Distributed Tracing'
rewards:
  badges:
  - 🏆 Pathfinder of the Request - Followed a single request across many services
  - 🧭 Reader of the Waterfall - Located latency in a multi-span trace
  skills_unlocked:
  - 🛠️ OpenTelemetry Instrumentation
  - 🧠 Latency Debugging in Distributed Systems
  progression_points: 75
  unlocks_features:
  - Access to the Alerting Systems quest
layout: quest
---
*Greetings, brave adventurer! From the **Watchtower** you have learned to read metrics and logs. But when a request limps across a dozen services and arrives slow, metrics only tell you *that* it is slow and logs only tell you *what* each service did - neither tells you **where** the time vanished. For that you need the rarest pillar of all: the **trace**. This quest, **Distributed Tracing**, teaches you to follow a single request through your entire kingdom and pin the exact span where the delay hides.*

*Whether you have stared helplessly at a slow endpoint with no idea which downstream call is to blame, or you already log timings by hand and crave something better, this adventure forges the skill every Warrior of the traces needs: spans and traces, context propagation, OpenTelemetry instrumentation, and reading a Jaeger waterfall.*

## 📖 The Legend Behind This Quest

*In the age of the monolith, a profiler could show you exactly where a request spent its time, because it all happened in one process. When the great cities of microservices rose, that single timeline shattered into fragments scattered across machines. A request might pass through an API gateway, an auth service, three databases, and a payment provider - and no single log could see the whole journey.*

*Distributed tracing stitches the fragments back together. Each service records its slice as a **span**; the spans share a **trace ID** and link parent-to-child, reassembling into one timeline. **OpenTelemetry** is the vendor-neutral standard for producing those spans, and **Jaeger** is a popular backend for storing and visualizing them. Master this and the most maddening question in distributed systems - "where did the time go?" - finally has an answer.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Spans and Traces** - Explain what a span is, how spans nest, and how they form a trace
- [ ] **Trace Context & Propagation** - Understand the trace ID, span ID, and how context crosses service boundaries
- [ ] **OpenTelemetry Instrumentation** - Instrument a Python service to emit spans automatically and manually
- [ ] **Reading a Trace in Jaeger** - Open a trace waterfall and identify the slowest span

### Secondary Objectives (Bonus Achievements)
- [ ] **Span Attributes & Events** - Enrich spans with attributes and timestamped events for debugging
- [ ] **Sampling** - Choose between head and tail sampling and reason about overhead
- [ ] **The Collector** - Route telemetry through the OpenTelemetry Collector instead of exporting directly

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Draw a trace as a tree of parent and child spans
- [ ] Explain how the W3C `traceparent` header propagates context between services
- [ ] Add a custom span with attributes around a slow code path
- [ ] Open a real trace and say which span is responsible for the latency

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] The three pillars of observability (complete [Monitoring Fundamentals](/quests/1010/monitoring-fundamentals/) first)
- [ ] Basic Python: functions, imports, running a script
- [ ] How HTTP services make requests to one another

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Python 3.10+ with `pip` and `venv`
- [ ] Docker (to run the Jaeger all-in-one backend)

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can build and run a small Python service end to end
- [ ] You are ready to reason about latency spread across many services
- [ ] Ready for 90-120 minutes of focused, hands-on building

## 🌍 Choose Your Adventure Platform

*The tracing backend (Jaeger) runs in a container everywhere; only Python setup differs. Then everyone meets at the same `pip install opentelemetry-...`.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
brew install python
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip flask requests \
  opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install   # auto-installs matching instrumentation

# Jaeger all-in-one exposes OTLP on 4317/4318 and the UI on 16686
docker run --rm -d --name jaeger -p 16686:16686 -p 4317:4317 -p 4318:4318 \
  jaegertracing/all-in-one:1.57
open http://localhost:16686
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install Python.Python.3.12
py -3 -m venv .venv; .\.venv\Scripts\activate
pip install --upgrade pip flask requests opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install

docker run --rm -d --name jaeger -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:1.57
start http://localhost:16686
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y python3 python3-venv docker.io
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip flask requests opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install

sudo docker run --rm -d --name jaeger -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:1.57
xdg-open http://localhost:16686
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# In a Codespace or any container host, run Jaeger the same way and
# forward port 16686 (UI) to your browser.
docker run --rm -d -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:1.57
```

</details>

## 🧙‍♂️ Chapter 1: Spans, Traces, and the Anatomy of a Request

*A trace is a story; spans are its sentences. Learn this vocabulary and the whole field clicks into place.*

### ⚔️ Skills You'll Forge in This Chapter
- The definition of a span and a trace
- How spans nest into a parent-child tree
- The fields every span carries

### 🏗️ The Vocabulary

- **Span** - one unit of work with a start time, end time (so a duration), a name, and attributes. Example: "HTTP GET /api/orders" or "SELECT FROM orders".
- **Trace** - the full tree of spans for one request, sharing a single **trace ID**.
- **Parent / child** - a span that triggers another (a service calling a database) is the *parent*; the work it triggers is a *child*.
- **Root span** - the first span in a trace, usually the inbound request at the edge.

A trace is best pictured as a **waterfall**, where indentation shows parent-child nesting and width shows duration:

```text
trace_id: 4bf92f3577b34da6  (total 520ms)
└─ checkout-api  GET /checkout              [████████████████████] 520ms   (root)
   ├─ auth-service  validate_token          [█]                    12ms
   ├─ inventory  check_stock                [██]                   40ms
   └─ payment-gw  charge_card               [██████████████]      455ms    <-- the latency lives here
```

Reading this, you instantly know the payment gateway, not your own code, owns the delay. That is the entire promise of tracing.

### 🔍 Knowledge Check: Spans and Traces
- [ ] What does a span measure, and what does a trace contain?
- [ ] In the waterfall above, which span is the root and which is slow?
- [ ] How do you know `auth-service` and `payment-gw` belong to the same request?

### ⚡ Quick Wins and Checkpoints
- [ ] **Read a waterfall**: You located the slow span in the example trace
- [ ] **Defined the terms**: You can explain span, trace, and trace ID

## 🧙‍♂️ Chapter 2: Trace Context and Propagation

*The magic that turns scattered spans into one trace is **context propagation**: every service passes the trace ID along when it calls the next. Lose the context and the trace breaks into orphan fragments.*

### ⚔️ Skills You'll Forge in This Chapter
- What lives in a trace context
- How the W3C `traceparent` header carries it over HTTP
- Why propagation is the make-or-break of distributed tracing

### 🏗️ The `traceparent` Header

When one service calls another over HTTP, OpenTelemetry injects a standard header so the callee knows it is part of an existing trace:

```text
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             │  │                                │                │
          version  trace-id (16 bytes)       parent span-id   trace-flags
                                              (8 bytes)        (sampled?)
```

The receiving service reads this header, starts its spans as **children** of `00f067aa0ba902b7`, and forwards a new `traceparent` to whatever it calls next. This is how a single trace ID flows end to end. If any hop drops the header (a misconfigured proxy, a queue without propagation), the downstream spans become a separate, orphaned trace - the most common tracing bug.

```python
# OpenTelemetry's requests instrumentation injects traceparent automatically.
# This is why auto-instrumentation matters: propagation is handled for you.
import requests
from opentelemetry.instrumentation.requests import RequestsInstrumentor

RequestsInstrumentor().instrument()      # now every requests.get() carries context
resp = requests.get("http://inventory:8000/stock")   # traceparent injected on the wire
```

### 🔍 Knowledge Check: Propagation
- [ ] What three IDs/flags does `traceparent` carry?
- [ ] What happens to a trace if one hop fails to forward the header?
- [ ] Why does auto-instrumentation make propagation reliable?

## 🧙‍♂️ Chapter 3: Instrumenting a Service with OpenTelemetry

*Now produce real spans. OpenTelemetry gives you two paths: **auto-instrumentation** (zero-code, wraps known libraries) and **manual spans** (you mark the code you care about).*

### ⚔️ Skills You'll Forge in This Chapter
- Auto-instrumenting a Flask app with one command
- Creating manual spans around custom logic
- Adding attributes and events to enrich a span

### 🏗️ A Traced Two-Service App

Here is a small Flask service that calls a downstream service. Manual spans wrap the interesting work:

```python
# app.py — a service instrumented with OpenTelemetry
from flask import Flask
import requests
from opentelemetry import trace

app = Flask(__name__)
tracer = trace.get_tracer(__name__)   # the handle used to create manual spans

@app.route("/checkout")
def checkout():
    # A manual span around domain logic that auto-instrumentation can't see.
    with tracer.start_as_current_span("validate_cart") as span:
        span.set_attribute("cart.items", 3)        # searchable attribute in Jaeger
        span.add_event("cart validated")           # a timestamped event on the span

    # This downstream call is auto-instrumented: its span and the
    # traceparent header are created for us.
    resp = requests.get("http://localhost:8000/stock", timeout=5)
    return {"ok": resp.ok}

if __name__ == "__main__":
    app.run(port=5000)
```

Run it with the zero-code auto-instrumentation wrapper, pointing at Jaeger's OTLP endpoint:

```bash
# OTEL_* env vars configure the exporter; opentelemetry-instrument wraps the app.
OTEL_SERVICE_NAME=checkout-api \
OTEL_TRACES_EXPORTER=otlp \
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 \
opentelemetry-instrument python app.py

# Generate a request, then look for the trace in Jaeger:
curl -s http://localhost:5000/checkout
# Open http://localhost:16686, pick service "checkout-api", click Find Traces.
```

`opentelemetry-instrument` automatically traces Flask routes and outbound `requests` calls; your manual `validate_cart` span nests inside the request span. In Jaeger you will see the whole tree.

### 🔍 Knowledge Check: Instrumentation
- [ ] What does auto-instrumentation give you for free, and what still needs a manual span?
- [ ] What is the difference between a span attribute and a span event?
- [ ] Where does the `validate_cart` span appear relative to the request span?

## 🧙‍♂️ Chapter 4: Reading Traces and Sampling Wisely

*Producing spans is half the quest; reading them and controlling their cost is the other half.*

### ⚔️ Skills You'll Forge in This Chapter
- Navigating the Jaeger waterfall
- Head versus tail sampling
- Keeping tracing overhead affordable

### 🏗️ Reading the Jaeger Waterfall

In the Jaeger UI: pick the service, click **Find Traces**, open one, and read top to bottom. Each bar is a span; nesting shows parent-child; the widest bar at the deepest level that is *not* explained by its children is usually your culprit. Click a span to see its attributes, events, and the service that emitted it.

### 🏗️ Sampling: You Cannot Keep Every Trace

At scale, tracing every request is too expensive. **Sampling** decides which traces to keep:

| Strategy | When the decision is made | Pro | Con |
| --- | --- | --- | --- |
| **Head sampling** | At the root, before the request runs (e.g. keep 10%) | Cheap, simple, low overhead | May discard the rare slow/error trace you needed |
| **Tail sampling** | After the trace completes, in the Collector | Keep all errors and slow traces, drop boring ones | Must buffer whole traces; more infrastructure |

A common production setup uses **tail sampling in the OpenTelemetry Collector**: keep 100% of error and high-latency traces, sample the healthy majority down to a few percent.

```yaml
# otel-collector-config.yaml — tail sampling: always keep errors and slow traces
processors:
  tail_sampling:
    policies:
      - name: keep-errors
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: keep-slow
        type: latency
        latency: { threshold_ms: 500 }
      - name: sample-the-rest
        type: probabilistic
        probabilistic: { sampling_percentage: 5 }
```

### 🔍 Knowledge Check: Reading and Sampling
- [ ] In a waterfall, how do you spot the span responsible for latency?
- [ ] Why might head sampling lose the exact trace you needed?
- [ ] What does tail sampling let you guarantee that head sampling cannot?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Emit Your First Trace
**Objective**: Instrument the Flask app, send one request, and find its trace in Jaeger.

**Requirements**:
- [ ] App runs under `opentelemetry-instrument` exporting to Jaeger
- [ ] One request produces a trace visible in the Jaeger UI
- [ ] The trace shows at least the request span and one child span

**Validation**: You can open the trace and see the parent-child waterfall.

### 🟡 Intermediate Challenge: Find the Slow Span
**Objective**: Add an artificial `time.sleep()` inside a manual span, then locate it in Jaeger.

**Requirements**:
- [ ] A manual span wraps the slow code with descriptive attributes
- [ ] The trace shows the slow span as the widest bar
- [ ] You can name the offending span from the waterfall alone

**Validation**: The injected delay is unmistakable in the trace timeline.

### 🔴 Advanced Challenge: Propagate Across Two Services
**Objective**: Run two instrumented services where one calls the other, and confirm both appear in a single trace.

**Requirements**:
- [ ] Service A calls Service B over HTTP with propagation enabled
- [ ] One Jaeger trace contains spans from both services
- [ ] Breaking propagation (stripping `traceparent`) splits them into two traces

**Validation**: The single trace shows both service names; removing propagation produces two orphaned traces.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Pathfinder of the Request** - You followed one request across many services
- 🧭 **Reader of the Waterfall** - You located latency inside a multi-span trace

**🛠️ Skills Unlocked**:
- **OpenTelemetry Instrumentation** - Produce spans automatically and manually
- **Latency Debugging in Distributed Systems** - Find where the time actually goes

**🔓 Unlocked Quests**:
- Alerting Systems - Turn the slow traces you find into actionable alerts

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Alerting Systems](/quests/1010/alerting-systems/) - Route and respond to the problems tracing reveals

**Explore Side Adventures**:
- ⚔️ [ELK Stack](/quests/1010/elk-stack/) - Correlate traces with the logs each span produced

### Character Class Recommendations

**💻 Software Developer**: Continue to [Alerting Systems](/quests/1010/alerting-systems/)  
**🏗️ System Engineer**: Explore [ELK Stack](/quests/1010/elk-stack/)  
**🛡️ Security Specialist**: Revisit [Monitoring Fundamentals](/quests/1010/monitoring-fundamentals/) for SLO grounding

## 📚 Resources

### Official Documentation
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/) - The vendor-neutral observability standard
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/) - Auto and manual instrumentation
- [Jaeger Documentation](https://www.jaegertracing.io/docs/) - Storing and visualizing traces
- [W3C Trace Context](https://www.w3.org/TR/trace-context/) - The `traceparent` propagation standard

### Community Resources
- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) - Routing, processing, and tail sampling
- [Awesome OpenTelemetry](https://github.com/magsther/awesome-opentelemetry) - Curated tools and reading
- [CNCF Distributed Tracing](https://www.cncf.io/) - Community and projects

### Learning Materials
- [Mastering Distributed Tracing (sample chapters)](https://www.shkuro.com/books/2019-mastering-distributed-tracing/) - Yuri Shkuro, Jaeger's creator
- [Sampling in OpenTelemetry](https://opentelemetry.io/docs/concepts/sampling/) - Head versus tail in depth

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Instrumented a service and emitted a trace
- [ ] ✅ Located a slow span in the Jaeger waterfall
- [ ] ✅ Propagated context across two services
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1010 - Monitoring & Observability]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Requires:** [[Monitoring Fundamentals: Metrics, Logs, and Traces for Observability]]
**Unlocks:** [[Alerting Systems: Alertmanager, Routing, and On-Call]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
