---
title: 'ELK Stack: Elasticsearch, Logstash & Kibana Logs'
author: IT-Journey Team
description: 'Deploy the ELK stack for centralized logging: Elasticsearch indexing, Logstash and Beats pipelines, and Kibana dashboards for distributed systems.'
excerpt: Build centralized logging with Elasticsearch, Logstash pipelines, Beats shippers, and Kibana visualization
preview: images/previews/elk-stack-elasticsearch-logstash-quest-title-kiban.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1010'
difficulty: 🔴 Hard
estimated_time: 120-150 minutes
primary_technology: elasticsearch
quest_type: main_quest
quest_series: Observability Mastery
quest_line: The Warrior's Watchtower
quest_arc: Mastering the Logs Pillar
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/1010/monitoring-fundamentals/
  unlocks_quests:
  - /quests/1010/distributed-tracing/
  - /quests/1010/alerting-systems/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Comfort on the command line and reading YAML
  - The three pillars of observability (metrics, logs, traces)
  - How web services emit logs and what a log line contains
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Docker and Docker Compose (8 GB RAM recommended for the stack)
  - A terminal and a text editor or IDE (VS Code recommended)
  skill_level_indicators:
  - Can operate a small service and read its logs
  - Ready to reason about parsing, indexing, and searching at scale
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A running ELK stack ingesting and visualizing structured logs
  skill_demonstrations:
  - Can write a Logstash grok pipeline that parses an unstructured log line
  - Can build a Kibana visualization over an index pattern
  knowledge_checks:
  - Understands indices, shards, mappings, and the inverted index
  - Can describe when to use Beats versus Logstash for shipping
permalink: /quests/1010/elk-stack/
categories:
- Quests
- DevOps
- Hard
tags:
- '1010'
- elasticsearch
- logstash
- kibana
- main_quest
- devops
- hands-on
- gamified-learning
keywords:
  primary:
  - '1010'
  - elasticsearch
  - logstash
  - kibana
  secondary:
  - structured-logging
  - log-pipelines
  - beats
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1010 (10) Quest: Main Quest - ELK Stack'
rewards:
  badges:
  - 🏆 Loremaster of the Logs - Centralized logs from chaos into a searchable archive
  - 📜 Keeper of the Index - Tamed Elasticsearch mappings and Logstash pipelines
  skills_unlocked:
  - 🛠️ Centralized Log Aggregation
  - 🧠 Structured Logging & Pipeline Design
  progression_points: 75
  unlocks_features:
  - Access to the Distributed Tracing and Alerting Systems quests
layout: quest
---
*Greetings, brave adventurer! High in the **Watchtower** of the Warrior tier you have learned to read the three pillars of observability. Now you descend into the great **Hall of Records** - the realm of logs - where every service in your kingdom scribbles its story in a thousand scattered scrolls. Alone, those scrolls are noise. Gathered, parsed, and indexed, they become an oracle that answers any question about what happened, when, and why. This quest, **The ELK Stack**, teaches you to build that oracle.*

*Whether you have only ever run `tail -f` on a single log file, or you already grep across servers and yearn for something better, this adventure forges the discipline every Warrior of the logs needs: structured logging, parsing pipelines, indices and mappings, and dashboards that turn raw events into insight.*

## 📖 The Legend Behind This Quest

*In the early ages, a service ran on one machine and its log lived in one file. When the great cities of microservices rose, a single user request might leave footprints in a dozen log files across a dozen hosts. Debugging by SSHing into each box and grepping became impossible. The operators who survived learned a single truth: logs must be **shipped, parsed, and centralized** the moment they are born, or they are useless when the fire starts.*

*The ELK Stack - **E**lasticsearch, **L**ogstash, and **K**ibana, joined by the lightweight **Beats** shippers - is the most widely deployed answer to that problem. Master it and you can ask any question of any log from any service, all from a single search bar.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **The ELK Architecture** - Explain what Elasticsearch, Logstash, Kibana, and Beats each do and how data flows between them
- [ ] **Elasticsearch Indexing** - Create indices, understand mappings and the inverted index, and query with the search API
- [ ] **Logstash Pipelines** - Write an input → filter → output pipeline that parses unstructured logs with `grok`
- [ ] **Kibana Visualization** - Build an index pattern, a Discover search, and a dashboard

### Secondary Objectives (Bonus Achievements)
- [ ] **Structured Logging** - Emit JSON logs at the source so parsing becomes trivial
- [ ] **Beats Shippers** - Use Filebeat to ship logs without a heavy Logstash on every host
- [ ] **Index Lifecycle Management** - Roll over and delete old indices so storage does not explode

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Draw the data flow from a log line to a Kibana chart without notes
- [ ] Write a grok pattern that turns `127.0.0.1 - GET /api 200 53ms` into structured fields
- [ ] Explain why high-cardinality fields and unbounded indices are dangerous
- [ ] Decide when Filebeat alone is enough and when you need Logstash in the middle

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Comfort on the command line and reading/writing YAML
- [ ] The three pillars of observability (complete [Monitoring Fundamentals](/quests/1010/monitoring-fundamentals/) first)
- [ ] A mental model of what a log line is and where services write them

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Docker and Docker Compose installed (allocate at least 4 GB, ideally 8 GB, to Docker)
- [ ] A terminal and a text editor or IDE (VS Code recommended)

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can run multi-container apps with Docker Compose
- [ ] You are ready to think about parsing, indexing, and searching at scale
- [ ] Ready for 120-150 minutes of focused, hands-on building

## 🌍 Choose Your Adventure Platform

*The stack runs in containers, so the lab is identical everywhere. The only platform difference is how you install Docker. Then everyone meets at the same `docker compose up`.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Install Docker Desktop (or colima) and confirm Compose is available
brew install --cask docker
docker --version
docker compose version

# Elasticsearch needs a higher mmap limit; Docker Desktop's VM handles it,
# but if you hit a vm.max_map_count error, raise it inside the VM.
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
# Install Docker Desktop with the WSL2 backend
winget install Docker.DockerDesktop
docker --version
docker compose version
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin   # Debian/Ubuntu
sudo systemctl enable --now docker

# Elasticsearch requires a raised virtual-memory map count on Linux hosts:
sudo sysctl -w vm.max_map_count=262144
echo 'vm.max_map_count=262144' | sudo tee /etc/sysctl.d/99-elasticsearch.conf
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# In a Codespace or any container host, the same compose file works.
# Forward ports 5601 (Kibana) and 9200 (Elasticsearch) to your browser.
docker compose up -d
```

> ⚠️ This single-node stack disables security for learning convenience. Never expose it to the public internet, and never use these settings in production.

</details>

## 🧙‍♂️ Chapter 1: The Architecture of the Hall of Records

*Before you ship a single log, learn what each component does. The ELK Stack is four cooperating services, each with one job.*

### ⚔️ Skills You'll Forge in This Chapter
- The role of Elasticsearch, Logstash, Kibana, and Beats
- How a log line travels from source to dashboard
- Where parsing should happen and why

### 🏗️ The Four Components

| Component | Job | Analogy |
| --- | --- | --- |
| **Beats** (e.g. Filebeat) | Lightweight shipper that tails files and forwards lines | The runner who carries scrolls from each tower |
| **Logstash** | Heavy pipeline: ingest, parse, enrich, and route | The scribe who reads, structures, and stamps each scroll |
| **Elasticsearch** | Distributed search engine that indexes and stores | The vast indexed library you can query instantly |
| **Kibana** | Web UI for search, visualization, and dashboards | The reading room where you ask the oracle questions |

The canonical data flow:

```text
[ app log file ] --> Filebeat --> Logstash (grok/filter) --> Elasticsearch (index) --> Kibana (search/chart)
```

For simple JSON logs you can skip Logstash entirely: `Filebeat --> Elasticsearch`. You add Logstash when you need to **parse unstructured text**, enrich records (GeoIP, lookups), or fan out to multiple destinations.

### 🔍 Knowledge Check: Architecture
- [ ] Which component stores and searches the data?
- [ ] When can you drop Logstash from the pipeline?
- [ ] What does Filebeat do that Logstash also can but more expensively?

### ⚡ Quick Wins and Checkpoints
- [ ] **Named the four roles**: You can say what each component does in one line
- [ ] **Drew the flow**: You sketched source → ship → parse → index → visualize

## 🧙‍♂️ Chapter 2: Stand Up the Stack with Docker Compose

*Now make it real. This single Compose file brings up Elasticsearch, Logstash, and Kibana, wired together.*

### ⚔️ Skills You'll Forge in This Chapter
- Running the full stack locally
- Verifying cluster health from the Elasticsearch API

### 🏗️ The Compose File

```yaml
# docker-compose.yml — single-node ELK for learning (security disabled)
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.13.4
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - ES_JAVA_OPTS=-Xms1g -Xmx1g        # cap heap so it fits a laptop
    ports:
      - "9200:9200"
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:9200/_cluster/health | grep -q '\"status\"'"]
      interval: 10s
      retries: 12

  logstash:
    image: docker.elastic.co/logstash/logstash:8.13.4
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    ports:
      - "5044:5044"      # Beats input
    depends_on:
      elasticsearch:
        condition: service_healthy

  kibana:
    image: docker.elastic.co/kibana/kibana:8.13.4
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - "5601:5601"
    depends_on:
      elasticsearch:
        condition: service_healthy
```

Bring it up and confirm the cluster is alive:

```bash
docker compose up -d

# Wait for green/yellow status (yellow is normal for a single node)
curl -s 'http://localhost:9200/_cluster/health?pretty'

# Kibana takes a minute; then open it
open http://localhost:5601   # macOS; use start/xdg-open elsewhere
```

### 🔍 Knowledge Check: Standing It Up
- [ ] Why is a single-node cluster `yellow` and not `green`?
- [ ] What does `ES_JAVA_OPTS=-Xms1g -Xmx1g` protect against on a laptop?
- [ ] Why does Logstash `depend_on` Elasticsearch being healthy?

## 🧙‍♂️ Chapter 3: Indexing in Elasticsearch

*Elasticsearch is a search engine, not just a database. Understanding indices, mappings, and the inverted index is what separates a log searcher from a log struggler.*

### ⚔️ Skills You'll Forge in This Chapter
- Indices, documents, shards, and mappings
- How the inverted index makes full-text search fast
- Indexing and querying documents via the REST API

### 🏗️ Core Concepts

- **Document** - a single JSON record (one log event).
- **Index** - a named collection of documents (e.g. `logs-2026.06.14`), like a table.
- **Shard** - a horizontal slice of an index; shards are how Elasticsearch scales and replicates.
- **Mapping** - the schema: which fields exist and their types (`keyword` for exact match, `text` for full-text, `date`, `long`, etc.).
- **Inverted index** - instead of scanning rows, Elasticsearch maps each *term* to the documents containing it, so searching billions of logs for "timeout" is near-instant.

Create an index with an explicit mapping, then index and search a document:

```bash
# 1. Create an index with a mapping (keyword vs text matters for search/aggregation)
curl -s -X PUT 'http://localhost:9200/app-logs' -H 'Content-Type: application/json' -d '{
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "level":      { "type": "keyword" },
      "service":    { "type": "keyword" },
      "message":    { "type": "text" },
      "duration_ms":{ "type": "long" }
    }
  }
}'

# 2. Index a structured log document
curl -s -X POST 'http://localhost:9200/app-logs/_doc' -H 'Content-Type: application/json' -d '{
  "@timestamp": "2026-06-14T10:31:02Z",
  "level": "error",
  "service": "checkout",
  "message": "payment gateway timeout",
  "duration_ms": 5012
}'

# 3. Search it: find all error logs from the checkout service
curl -s 'http://localhost:9200/app-logs/_search?pretty' -H 'Content-Type: application/json' -d '{
  "query": { "bool": { "must": [
    { "match": { "level": "error" } },
    { "match": { "service": "checkout" } }
  ]}}
}'
```

> Field types matter: use `keyword` for fields you filter and aggregate on (level, service) and `text` for fields you full-text search (message). Getting this wrong is the #1 beginner mistake.

### 🔍 Knowledge Check: Indexing
- [ ] What is the difference between a `keyword` and a `text` field?
- [ ] Why is the inverted index faster than scanning every document?
- [ ] What does a mapping define, and why set it explicitly?

## 🧙‍♂️ Chapter 4: Parsing Logs with Logstash and `grok`

*Most real logs are unstructured text. Logstash's job is to turn `127.0.0.1 - - GET /api/orders 200 53` into searchable fields. The `grok` filter is the spell that does it.*

### ⚔️ Skills You'll Forge in This Chapter
- The input → filter → output pipeline shape
- Parsing unstructured lines with `grok`
- Why structured logging at the source beats parsing later

### 🏗️ A Logstash Pipeline

```ruby
# logstash.conf — input (Beats) -> filter (parse) -> output (Elasticsearch)
input {
  beats { port => 5044 }
}

filter {
  # grok parses a common access-log line into named fields.
  grok {
    match => { "message" => "%{IP:client_ip} %{USER:ident} %{USER:auth} %{WORD:method} %{URIPATHPARAM:request} %{NUMBER:status:int} %{NUMBER:duration_ms:int}" }
  }
  # Promote the parsed timestamp to the event's @timestamp.
  date {
    match => [ "timestamp", "ISO8601" ]
  }
  # Drop the raw message once parsed to save space (optional).
  mutate { remove_field => [ "ident", "auth" ] }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "access-logs-%{+YYYY.MM.dd}"   # daily indices, easy to roll over
  }
}
```

The three stages map directly onto the architecture: **input** receives from Beats, **filter** structures the data, **output** writes to Elasticsearch. The `%{NUMBER:status:int}` syntax both extracts *and* casts, so `status` becomes a real number you can aggregate.

### 🏗️ The Better Path: Structured Logging at the Source

Parsing text is fragile - one log-format change breaks your grok. The superior approach is to emit **JSON logs** at the application, so no parsing is needed:

```python
# Emit JSON logs the moment they are born — no grok required downstream.
import json, logging, sys

class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "@timestamp": self.formatTime(record),
            "level": record.levelname.lower(),
            "service": "checkout",
            "message": record.getMessage(),
        })

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
log = logging.getLogger("app")
log.addHandler(handler)
log.setLevel(logging.INFO)

log.error("payment gateway timeout")   # -> a clean JSON line Elasticsearch loves
```

### 🔍 Knowledge Check: Parsing
- [ ] What do the three Logstash stages (input/filter/output) each do?
- [ ] Why is structured JSON logging more robust than grok parsing?
- [ ] What does `%{NUMBER:status:int}` accomplish beyond extraction?

## 🧙‍♂️ Chapter 5: Visualizing in Kibana

*Elasticsearch holds the answers; Kibana asks the questions. In a few clicks you turn indexed logs into searches, charts, and dashboards.*

### ⚔️ Skills You'll Forge in This Chapter
- Creating a data view (index pattern)
- Searching in Discover with KQL
- Building a visualization and a dashboard

### 🏗️ From Index to Dashboard

1. **Create a data view**: in Kibana, go to *Stack Management → Data Views* and add `access-logs-*` with `@timestamp` as the time field.
2. **Explore in Discover**: open *Discover*, pick the data view, and filter with **KQL** (Kibana Query Language):

```text
# KQL examples you type in the Discover search bar
status >= 500 and method : "POST"
service : "checkout" and duration_ms > 1000
not status : 200
```

3. **Build a visualization**: in *Lens*, drop `@timestamp` on the X axis and `Count` on the Y axis, then break it down by the `status` keyword field to see error spikes over time.
4. **Assemble a dashboard**: combine a request-rate line chart, a top-errors table, and a p95-latency metric into one board your team watches.

### 🔍 Knowledge Check: Visualization
- [ ] What does a Kibana data view connect to?
- [ ] Write a KQL query for "5xx responses on the checkout service"
- [ ] Why must you choose a time field when creating the data view?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Index and Search by Hand
**Objective**: Using only the Elasticsearch REST API, create an index, add three log documents, and run a search that returns exactly one of them.

**Requirements**:
- [ ] An index with an explicit mapping (at least one `keyword` and one `text` field)
- [ ] Three documents indexed via `_doc`
- [ ] A `bool`/`match` query that returns exactly one document

**Validation**: The search response's `hits.total.value` equals 1.

### 🟡 Intermediate Challenge: Parse a Real Log Line
**Objective**: Write a Logstash `grok` filter that turns a raw access-log line into structured, typed fields.

**Requirements**:
- [ ] `grok` extracts at least method, path, status, and duration
- [ ] `status` and `duration_ms` are cast to integers
- [ ] The output lands in a daily-rolled index in Elasticsearch

**Validation**: In Kibana Discover, you can filter `status >= 500` and see only matching events.

### 🔴 Advanced Challenge: Build the Observability Dashboard
**Objective**: Build a Kibana dashboard for one service with request rate, error rate, and latency.

**Requirements**:
- [ ] A time-series of request count broken down by `status`
- [ ] A table of the top error messages
- [ ] A metric showing p95 `duration_ms`

**Validation**: Generate some traffic, then watch the dashboard reflect the error spike within a minute.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Loremaster of the Logs** - You centralized scattered logs into a searchable archive
- 📜 **Keeper of the Index** - You tamed Elasticsearch mappings and Logstash pipelines

**🛠️ Skills Unlocked**:
- **Centralized Log Aggregation** - Ship, parse, and index logs from anywhere
- **Structured Logging & Pipeline Design** - Make logs searchable by design, not by luck

**🔓 Unlocked Quests**:
- Distributed Tracing - Follow a single request across services
- Alerting Systems - Turn indexed signals into actionable pages

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Distributed Tracing](/quests/1010/distributed-tracing/) - Master the traces pillar with OpenTelemetry and Jaeger

**Explore Side Adventures**:
- ⚔️ [Alerting Systems](/quests/1010/alerting-systems/) - Route and respond to what your logs reveal

### Character Class Recommendations

**💻 Software Developer**: Continue to [Distributed Tracing](/quests/1010/distributed-tracing/)  
**🏗️ System Engineer**: Explore [Alerting Systems](/quests/1010/alerting-systems/)  
**🛡️ Security Specialist**: Revisit [Monitoring Fundamentals](/quests/1010/monitoring-fundamentals/) for SLO grounding

## 📚 Resources

### Official Documentation
- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html) - Indices, mappings, and the query DSL
- [Logstash Reference](https://www.elastic.co/guide/en/logstash/current/index.html) - Pipelines, inputs, filters, outputs
- [Kibana Guide](https://www.elastic.co/guide/en/kibana/current/index.html) - Data views, Discover, Lens, dashboards
- [Filebeat Reference](https://www.elastic.co/guide/en/beats/filebeat/current/index.html) - Lightweight log shipping

### Community Resources
- [Grok Debugger](https://grokdebugger.com/) - Test grok patterns interactively
- [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current/index.html) - A shared field naming standard
- [Awesome Elasticsearch](https://github.com/dzharii/awesome-elasticsearch) - Curated tools and reading

### Learning Materials
- [Elastic Stack Quickstart](https://www.elastic.co/guide/en/elastic-stack/current/index.html) - Get the whole stack running
- [Index Lifecycle Management](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html) - Roll over and retire indices

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Stood up a running ELK stack with Docker Compose
- [ ] ✅ Indexed and searched documents in Elasticsearch
- [ ] ✅ Parsed a log line with a Logstash grok filter
- [ ] ✅ Built a Kibana dashboard
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1010 - Monitoring & Observability]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Requires:** [[Monitoring Fundamentals: Metrics, Logs, and Traces for Observability]] **Unlocks:** [[Distributed Tracing: OpenTelemetry and Jaeger]] · [[Alerting Systems: Alertmanager, Routing, and On-Call]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
