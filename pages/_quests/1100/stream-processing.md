---
title: 'Stream Processing: Real-Time Data with Apache Kafka & Flink'
author: IT-Journey Team
description: Build real-time streaming pipelines with Kafka. Learn batch versus stream, event time versus processing time, windowing, watermarks, and exactly-once semantics for event-driven systems.
excerpt: Build real-time pipelines with Kafka, windowing, event-time processing, and exactly-once delivery
preview: images/previews/stream-processing-descriptive-subtitle.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1100'
difficulty: 🔴 Hard
estimated_time: 4-5 hours
primary_technology: kafka
quest_type: main_quest
quest_series: Data Engineering Mastery
quest_line: The Data Engineer's Ascent
quest_arc: Data That Never Stops
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/1100/etl-pipeline-design/
  - /quests/1100/apache-spark/
  unlocks_quests:
  - /quests/1100/data-quality/
skill_focus: data-engineering
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Comfortable writing functions and using packages in Python 3.10+
  - The ETL stages and idempotency from ETL Pipeline Design
  - How services communicate and what a message queue is
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Docker and Docker Compose for a local Kafka broker
  - Python 3.10+ with pip and venv
  skill_level_indicators:
  - Can build and run a small Python data script end to end
  - Ready to reason about unbounded, out-of-order data
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A Kafka producer and consumer exchanging events locally
  skill_demonstrations:
  - Can produce to and consume from a Kafka topic with partitions
  - Can explain a windowed aggregation over event time
  knowledge_checks:
  - Understands batch versus stream and event versus processing time
  - Can describe how exactly-once is achieved in practice
permalink: /quests/1100/stream-processing/
categories:
- Quests
- Data-Engineering
- Hard
tags:
- '1100'
- kafka
- streaming
- main_quest
- data-engineering
- hands-on
- gamified-learning
keywords:
  primary:
  - '1100'
  - kafka
  - streaming
  secondary:
  - windowing
  - exactly-once
  - event-time
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1100 (12) Quest: Main Quest - Stream Processing'
rewards:
  badges:
  - 🏆 Rider of the Stream - Processed data that never stops arriving
  - ⏱️ Keeper of Event Time - Tamed windows, watermarks, and late data
  skills_unlocked:
  - 🛠️ Kafka Producer/Consumer Engineering
  - 🧠 Windowing and Exactly-Once Stream Design
  progression_points: 75
  unlocks_features:
  - Access to the Data Quality Engineering quest
layout: quest
---
*Greetings, brave adventurer! In every prior quest your data sat still - a file, a table, a finished batch - waiting patiently to be processed. But the real kingdom never sleeps: orders, clicks, sensor readings, and log events pour in without end, and your analysts want answers *now*, not tomorrow. This quest, **Stream Processing**, teaches you to build aqueducts for water that never stops flowing - pipelines that compute over an endless river of events in real time.*

*Whether you have only ever run nightly batch jobs, or you already pipe events through a queue and wrestle with late-arriving data, this adventure forges the discipline every real-time data engineer needs: the batch-versus-stream mindset, Kafka's log abstraction, windowing over event time, watermarks for late data, and the holy grail of exactly-once processing.*

## 📖 The Legend Behind This Quest

*In the early ages, all data engineering was batch: collect a day of data, process it overnight, report in the morning. But fraud cannot wait until morning; a dashboard of yesterday's sales is a museum piece. The kingdoms that thrived learned to process events **as they arrive**, treating data not as a finished pile but as an infinite, ordered log.*

*Apache Kafka became the backbone of that revolution - a durable, partitioned, replayable log that decouples the producers of events from their consumers. Stream processors like Flink and Kafka Streams compute over that log continuously. But streaming introduces a brutal new challenge absent from batch: events arrive **out of order and late**, so you must reason carefully about *which* clock you trust. This quest teaches you to master that clock.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Batch vs Stream** - Explain the differences and choose the right model for a workload
- [ ] **Kafka Fundamentals** - Understand topics, partitions, offsets, producers, and consumer groups
- [ ] **Event Time vs Processing Time** - Distinguish when an event happened from when it was processed
- [ ] **Windowing** - Aggregate an unbounded stream into tumbling, sliding, and session windows

### Secondary Objectives (Bonus Achievements)
- [ ] **Watermarks & Late Data** - Handle out-of-order events with watermarks and allowed lateness
- [ ] **Exactly-Once Semantics** - Explain how idempotent producers and transactions prevent duplicates
- [ ] **Backpressure & Replay** - Reason about consumer lag and replaying from an offset

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Decide whether a problem needs batch or streaming and defend the choice
- [ ] Produce to and consume from a partitioned Kafka topic
- [ ] Explain why a windowed count differs under event time versus processing time
- [ ] Describe the three guarantees - at-most-once, at-least-once, exactly-once

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Comfortable writing Python functions and using `pip` packages
- [ ] The ETL stages and idempotency (complete [ETL Pipeline Design](/quests/1100/etl-pipeline-design/) first)
- [ ] A mental model of message queues and how services pass messages

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Docker and Docker Compose for a local Kafka broker
- [ ] Python 3.10+ with `pip` and `venv`

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can build and run a small Python data script end to end
- [ ] You are ready to reason about unbounded, out-of-order data
- [ ] Ready for 4-5 hours of focused, hands-on building

## 🌍 Choose Your Adventure Platform

*Kafka runs in a container everywhere; only Docker setup differs. Then everyone meets at the same `kafka-python` producer.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
brew install --cask docker
brew install python
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip kafka-python
# Bring up the single-broker Kafka (compose file in Chapter 2), then:
docker compose up -d
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install Docker.DockerDesktop Python.Python.3.12
py -3 -m venv .venv; .\.venv\Scripts\activate
pip install --upgrade pip kafka-python
docker compose up -d
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin python3 python3-venv
sudo systemctl enable --now docker
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip kafka-python
docker compose up -d
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# In a Codespace or container host, run the same compose file.
# Forward port 9092 (broker) so your Python client can connect.
docker compose up -d
```

</details>

## 🧙‍♂️ Chapter 1: Batch vs Stream - Two Mental Models

*Before a single event flows, decide whether you are processing a finished pile or an endless river. The two models demand different thinking.*

### ⚔️ Skills You'll Forge in This Chapter
- The defining differences between batch and stream
- When real-time processing is worth its complexity
- The vocabulary of bounded vs unbounded data

### 🏗️ The Two Models

| Aspect | **Batch** | **Stream** |
| --- | --- | --- |
| Data shape | Bounded - a finite, complete dataset | Unbounded - an endless, never-complete sequence |
| Latency | Minutes to hours | Milliseconds to seconds |
| Completeness | You see all the data before computing | You never see "all" the data; you compute as it arrives |
| Typical use | Daily reports, ML training, reconciliation | Fraud detection, live dashboards, alerting, personalization |
| Reprocessing | Re-run the whole job | Replay from an offset in the log |

**Rule of thumb:** if a delay of hours is acceptable, batch is simpler and cheaper - prefer it. Reach for streaming only when freshness has real value (a fraud alert tomorrow is worthless). Many modern systems run *both*: a streaming layer for now, a batch layer for correctness and backfills.

### 🔍 Knowledge Check: Batch vs Stream
- [ ] What makes streaming data "unbounded"?
- [ ] Name one workload where streaming's complexity is unjustified
- [ ] Why can a stream processor never wait to "see all the data"?

### ⚡ Quick Wins and Checkpoints
- [ ] **Chose a model**: You can justify batch or stream for a workload you know
- [ ] **Defined the terms**: You can explain bounded versus unbounded data

## 🧙‍♂️ Chapter 2: Kafka - The Log at the Heart of Streaming

*Kafka is not a queue you drain; it is a durable, replayable **log**. Understanding that abstraction unlocks everything else.*

### ⚔️ Skills You'll Forge in This Chapter
- Topics, partitions, offsets, and consumer groups
- Why the log is replayable and durable
- Producing and consuming events in Python

### 🏗️ The Kafka Mental Model

- **Topic** - a named stream of events (e.g. `orders`).
- **Partition** - a topic is split into ordered, append-only partitions; order is guaranteed *within* a partition, not across them. Partitions are how Kafka scales and parallelizes.
- **Offset** - each event's position in its partition. Consumers track their offset, so they can **replay** from any point - the log is not deleted on read.
- **Consumer group** - a set of consumers that split a topic's partitions among themselves for parallel consumption.

```text
topic: orders (3 partitions)            consumer group "billing"
  p0: [e0][e1][e2][e3 ...]  <───────────  consumer A (reads p0)
  p1: [e0][e1][e2 ...]      <───────────  consumer B (reads p1)
  p2: [e0][e1 ...]          <───────────  consumer C (reads p2)
  ▲ offsets advance →          replay by resetting an offset
```

Bring up a broker, then produce and consume:

```yaml
# docker-compose.yml — a single-broker Kafka in KRaft mode (no ZooKeeper)
services:
  kafka:
    image: bitnami/kafka:3.7
    ports:
      - "9092:9092"
    environment:
      - KAFKA_CFG_NODE_ID=0
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka:9093
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
```

```python
# producer.py — append events to the 'orders' topic
import json, time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode(),
    key_serializer=lambda k: k.encode(),
)
for i in range(5):
    event = {"order_id": i, "amount": 10 * i, "event_time": time.time()}
    # The key decides the partition, so all events for one customer keep order.
    producer.send("orders", key=f"cust-{i % 2}", value=event)
producer.flush()
print("produced 5 events")
```

```python
# consumer.py — read events from the beginning, tracking offsets per group
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    group_id="billing",
    auto_offset_reset="earliest",       # start from offset 0 the first time
    value_deserializer=lambda b: json.loads(b),
)
for msg in consumer:
    print(f"partition={msg.partition} offset={msg.offset} value={msg.value}")
```

### 🔍 Knowledge Check: Kafka
- [ ] Within what scope does Kafka guarantee ordering?
- [ ] Why can a Kafka consumer replay old events but a traditional queue cannot?
- [ ] What determines which partition an event lands in?

## 🧙‍♂️ Chapter 3: Event Time, Processing Time, and Windowing

*This is the hardest and most important idea in streaming. Events carry the time they *happened*, but you process them at a different, later time - and they may arrive out of order. Choosing the right clock changes your results.*

### ⚔️ Skills You'll Forge in This Chapter
- Event time vs processing time vs ingestion time
- Tumbling, sliding, and session windows
- Watermarks and handling late data

### 🏗️ Three Clocks

- **Event time** - when the event actually occurred (a timestamp inside the event). What you almost always *want* to aggregate by.
- **Processing time** - when your system happened to process it. Easy, but wrong whenever events are delayed.
- **Ingestion time** - when the event entered Kafka. A compromise between the two.

A mobile order placed at 11:59 but uploaded at 12:03 (after the phone regained signal) *belongs* in the 11:00-12:00 hour by event time, even though it was processed in the next hour. Use processing time and you mis-bucket it.

### 🏗️ Windowing an Unbounded Stream

Because a stream never ends, you aggregate over **windows** - finite slices of the timeline:

```text
Tumbling (fixed, non-overlapping):  [00:00-00:05)[00:05-00:10)[00:10-00:15)
Sliding  (fixed, overlapping):      [00:00-00:05)[00:01-00:06)[00:02-00:07)
Session  (gap-defined):             [activity...][gap > 5m][new session...]
```

- **Tumbling** - "count orders every 5 minutes." Each event lands in exactly one window.
- **Sliding** - "average over the last 5 minutes, updated every minute." Windows overlap.
- **Session** - "group a user's activity until they go quiet for 5 minutes." Windows are data-driven.

### 🏗️ Watermarks: Deciding When a Window Is "Done"

Since late events can always trickle in, how does the processor know a window is complete enough to emit? A **watermark** is the stream's assertion that "no events older than time T will (probably) still arrive." When the watermark passes a window's end, the window fires. Events arriving after, within an **allowed lateness**, can still update it; beyond that, they are dropped or sent to a side output.

```text
window [12:00-12:05)  closes when watermark >= 12:05
  late event with event_time 12:04 arriving at 12:06:
    if watermark < 12:05 + allowed_lateness  -> still counted
    else                                      -> dropped (or routed to a "late" stream)
```

### 🔍 Knowledge Check: Time and Windows
- [ ] Why prefer event time over processing time for most aggregations?
- [ ] When is a session window the right choice over a tumbling one?
- [ ] What question does a watermark answer for the processor?

## 🧙‍♂️ Chapter 4: Delivery Guarantees and Exactly-Once

*The final mystery: in a distributed stream with retries and failures, how do you avoid counting an event twice - or losing it? The answer is a careful combination of idempotence and transactions.*

### ⚔️ Skills You'll Forge in This Chapter
- The three delivery guarantees
- How exactly-once is actually achieved
- Why idempotent consumers matter

### 🏗️ The Three Guarantees

| Guarantee | Meaning | Risk |
| --- | --- | --- |
| **At-most-once** | Each event delivered zero or one times | May **lose** events on failure |
| **At-least-once** | Each event delivered one or more times | May **duplicate** events on retry |
| **Exactly-once** | Each event takes effect exactly once | Hardest; needs coordination |

Naive retries give at-least-once: if a producer resends after a timeout, the broker may store the event twice. **Exactly-once semantics (EOS)** in Kafka combines two mechanisms:

1. **Idempotent producer** (`enable.idempotence=true`) - the broker deduplicates retries using a producer ID and sequence number, so a resend does not create a duplicate.
2. **Transactions** - a consume-process-produce cycle is wrapped in a transaction so the output write and the consumer-offset commit succeed or fail **together** (`read_committed` isolation downstream).

```python
# Exactly-once flavored producer: idempotence + transactions
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    enable_idempotence=True,                 # broker dedups retried sends
    transactional_id="orders-aggregator-1",  # enables atomic transactions
    value_serializer=lambda v: v.encode(),
)
producer.init_transactions()
producer.begin_transaction()
try:
    producer.send("orders-agg", value="window=12:00 count=42")
    # ... also commit the consumed offsets inside this same transaction ...
    producer.commit_transaction()            # output + offsets land atomically
except Exception:
    producer.abort_transaction()             # nothing is half-applied
```

A practical complement: make your **consumer idempotent** too - key writes on a stable event id and upsert (just like the idempotent load from the ETL quest), so even an at-least-once delivery causes no harm downstream.

### 🔍 Knowledge Check: Delivery Guarantees
- [ ] What does at-least-once risk that exactly-once prevents?
- [ ] What two mechanisms combine to give Kafka exactly-once?
- [ ] Why does an idempotent consumer make duplicates harmless?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Produce and Consume
**Objective**: Run the local Kafka broker, produce several events to a partitioned topic, and consume them in a group.

**Requirements**:
- [ ] A topic with at least two partitions
- [ ] A producer that keys events so related ones share a partition
- [ ] A consumer group that reads from the earliest offset

**Validation**: The consumer prints each event with its partition and offset; replaying resets the offset and re-reads.

### 🟡 Intermediate Challenge: Windowed Count over Event Time
**Objective**: Aggregate the stream into tumbling windows keyed by the event's own timestamp.

**Requirements**:
- [ ] Events carry an `event_time` field used for bucketing
- [ ] A tumbling window count per fixed interval
- [ ] An out-of-order event lands in the correct window by event time

**Validation**: A deliberately late event is counted in its true window, not the current one.

### 🔴 Advanced Challenge: Exactly-Once Aggregation
**Objective**: Build a consume-process-produce loop that survives a forced failure without duplicating output.

**Requirements**:
- [ ] Idempotent producer with a transactional id
- [ ] Offsets committed inside the same transaction as the output
- [ ] An idempotent downstream upsert keyed on a stable id

**Validation**: Kill the process mid-batch, restart it, and confirm the output totals are correct with no duplicates.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Rider of the Stream** - You processed data that never stops arriving
- ⏱️ **Keeper of Event Time** - You tamed windows, watermarks, and late data

**🛠️ Skills Unlocked**:
- **Kafka Producer/Consumer Engineering** - Build durable, replayable event pipelines
- **Windowing and Exactly-Once Stream Design** - Aggregate unbounded data correctly

**🔓 Unlocked Quests**:
- Data Quality Engineering - Validate streaming and batch data alike

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Data Quality Engineering](/quests/1100/data-quality/) - Guard the correctness of every event

**Explore Side Adventures**:
- ⚔️ [Apache Spark](/quests/1100/apache-spark/) - Batch-process the same data at scale

### Character Class Recommendations

**💻 Software Developer**: Continue to [Data Quality Engineering](/quests/1100/data-quality/)  
**🏗️ System Engineer**: Revisit [Apache Spark](/quests/1100/apache-spark/) for Structured Streaming  
**📊 Data Scientist**: Advance to [Data Quality Engineering](/quests/1100/data-quality/)

## 📚 Resources

### Official Documentation
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/) - Topics, partitions, producers, consumers
- [Kafka Exactly-Once Semantics](https://kafka.apache.org/documentation/#semantics) - Idempotence and transactions
- [Apache Flink Documentation](https://nightlies.apache.org/flink/flink-docs-stable/) - Event time, windows, watermarks
- [kafka-python](https://kafka-python.readthedocs.io/) - The Python client used in this quest

### Community Resources
- [The Log: What every engineer should know (Jay Kreps)](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying) - The foundational essay
- [Streaming 101 & 102 (Tyler Akidau)](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/) - Event time and windowing explained
- [Awesome Kafka](https://github.com/infoslack/awesome-kafka) - Curated tools and reading

### Learning Materials
- [Kafka: The Definitive Guide (Confluent, free)](https://www.confluent.io/resources/kafka-the-definitive-guide/) - The standard book
- [Designing Data-Intensive Applications](https://dataintensive.net/) - Chapter 11 on stream processing

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Produced to and consumed from a partitioned Kafka topic
- [ ] ✅ Built a windowed aggregation over event time
- [ ] ✅ Handled a late event correctly with a watermark
- [ ] ✅ Implemented an exactly-once aggregation
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1100 - Data Engineering]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Requires:** [[ETL Pipeline Design: Build Scalable Data Pipelines with Python]]
**Unlocks:** [[Data Quality Engineering: Testing, Validation & Monitoring Frameworks]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
