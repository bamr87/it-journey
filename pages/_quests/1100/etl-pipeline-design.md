---
title: 'ETL Pipeline Design: Build Scalable Data Pipelines with Python'
author: IT-Journey Team
description: Design and implement production ETL pipelines in Python. Learn ETL vs ELT, extraction and loading strategies, idempotency, incremental loads, and orchestration with Airflow DAGs.
excerpt: Build production-grade ETL pipelines with Python, covering extraction, transformation, idempotent loading, and Airflow orchestration
preview: images/previews/etl-pipeline-design-descriptive-subtitle.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1100'
difficulty: 🔴 Hard
estimated_time: 4-5 hours
primary_technology: python
quest_type: main_quest
quest_series: Data Engineering Mastery
quest_line: The Data Engineer's Ascent
quest_arc: Forging the Pipeline Foundations
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/1100/conquer-king-edgar/
  unlocks_quests:
  - /quests/1100/data-warehousing/
  - /quests/1100/apache-spark/
  - /quests/1100/data-quality/
skill_focus: data-engineering
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Comfortable writing functions and using packages in Python 3.10+
  - Basic SQL (SELECT, INSERT, JOIN) and how relational tables work
  - Understanding of JSON, CSV, and HTTP/REST basics
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Python 3.10+ with pip and venv
  - SQLite (bundled with Python) and a text editor or IDE
  skill_level_indicators:
  - Can build and run a small Python script end to end
  - Ready to reason about failure, retries, and reruns of a process
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A runnable Python ETL script that loads idempotently into SQLite
  skill_demonstrations:
  - Can explain when to choose ETL versus ELT and why
  - Can implement an idempotent upsert that is safe to rerun
  knowledge_checks:
  - Understands incremental versus full loads and watermarks
  - Can describe what an Airflow DAG, task, and dependency are
permalink: /quests/1100/etl-pipeline-design/
categories:
- Quests
- Data-Engineering
- Hard
tags:
- '1100'
- python
- etl
- main_quest
- data-engineering
- hands-on
- gamified-learning
keywords:
  primary:
  - '1100'
  - python
  - etl
  secondary:
  - main_quest
  - data-engineering
  - hands-on
  - gamified-learning
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1100 (12) Quest: Main Quest - ETL Pipelines'
rewards:
  badges:
  - 🏆 Pipeline Architect - Designed an idempotent, orchestrated ETL flow
  - ⚙️ Idempotency Adept - Built loads that are safe to rerun
  skills_unlocked:
  - 🛠️ Python ETL Engineering
  - 🧠 Workflow Orchestration with Airflow
  progression_points: 75
  unlocks_features:
  - Access to the Data Warehousing and Apache Spark quests
layout: quest
---
*Greetings, brave adventurer! You stand at the gates of the **Master tier** and the realm of **Data Engineering** opens before you. Your first trial is the **ETL Pipeline** - the great aqueduct that carries raw data from scattered springs, purifies it in transformation chambers, and delivers it into the reservoirs your analysts and models depend on. Build it well and the kingdom drinks clean water; build it carelessly and every dashboard downstream is poisoned.*

*Whether you have hand-fed CSVs into spreadsheets or you are formalizing pipelines you already run by intuition, this quest forges the core discipline of every data engineer: moving data **reliably, repeatably, and idempotently** from source to destination - then handing the work to an orchestrator that runs it on schedule, forever.*

## 📖 The Legend Behind This Quest

*In the early days, data lived in one database and one report. Then came the flood: APIs, event logs, SaaS exports, sensor feeds. Engineers discovered that the value was never in the raw data itself but in the **pipeline** that reshaped it into something trustworthy. The ones who thrived learned a hard truth - a pipeline that cannot be safely rerun is not a pipeline, it is a time bomb.*

*This quest teaches the "why" behind every Extract, Transform, and Load. Master it and the rest of the Data Engineering tier - warehousing, Spark, streaming, quality - becomes a set of variations on a theme you already understand.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **ETL vs ELT** - Explain both patterns and choose correctly for a given workload
- [ ] **The Extract / Transform / Load stages** - Build each stage as a clean, testable function
- [ ] **Idempotency & incremental loads** - Write a load that is safe to rerun and only moves new data
- [ ] **Orchestration with Airflow** - Express the pipeline as a DAG of dependent tasks on a schedule

### Secondary Objectives (Bonus Achievements)
- [ ] **Error handling & retries** - Make the pipeline survive transient failures
- [ ] **Watermarking** - Track the high-water mark so reruns do not duplicate data
- [ ] **Backfills** - Reprocess a historical window without breaking the present

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain idempotency to another person with a concrete example
- [ ] Convert a full-load script into an incremental one using a watermark
- [ ] Sketch an Airflow DAG with the correct task dependencies for a real pipeline
- [ ] Rerun your pipeline twice and prove the destination is unchanged the second time

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Comfortable writing Python functions and using `pip` packages
- [ ] Basic SQL: `SELECT`, `INSERT`, `JOIN`, primary keys
- [ ] Understanding of JSON, CSV, and how an HTTP API returns data

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Python 3.10+ with `pip` and `venv`
- [ ] SQLite (ships with Python) and VS Code or your editor of choice

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can build and run a small Python program end to end
- [ ] You are ready to think about failure, retries, and safe reruns
- [ ] Ready for 4-5 hours of focused, hands-on building

## 🌍 Choose Your Adventure Platform

*The pipeline is plain Python and SQLite, so it runs anywhere. Pick the path that fits your setup, then everyone meets at the same `pip install`.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
brew install python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip requests pandas
python --version
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install Python.Python.3.12
py -3 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip requests pandas
python --version
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y python3 python3-venv   # Debian/Ubuntu
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip requests pandas
python --version
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Any Codespace or container with Python works. For the Airflow chapter:
docker run --rm -p 8080:8080 apache/airflow:2.9.3 standalone
# Then open http://localhost:8080 (the standalone command prints a login).
```

</details>

## 🧙‍♂️ Chapter 1: ETL vs ELT - Choosing the Shape of Your Pipeline

*Before you move a single byte, you must decide **where transformation happens**. This single choice shapes your whole architecture.*

### ⚔️ Skills You'll Forge in This Chapter
- The difference between ETL and ELT
- When each pattern is the right tool
- The vocabulary of source, staging, and destination

### 🏗️ The Two Patterns

| Aspect | **ETL** (Extract → Transform → Load) | **ELT** (Extract → Load → Transform) |
| --- | --- | --- |
| Where transforms run | In a processing layer **before** loading | **Inside** the warehouse, after loading raw data |
| Best for | Legacy targets, heavy cleansing, small/medium volume, compliance filtering before storage | Cloud warehouses (Snowflake, BigQuery, Redshift) with cheap compute and storage |
| Raw data kept? | Often discarded after transform | Raw lands first, so you can re-transform later |
| Tooling | Python, Spark, Informatica, custom code | dbt, SQL, warehouse compute |

**Rule of thumb:** if your destination is a powerful cloud warehouse, prefer **ELT** - load raw, transform with SQL/dbt, and keep the raw layer so you can fix transforms without re-extracting. If you must cleanse, mask, or reshape before data ever touches storage (PII, tiny target, on-prem), use **ETL**. This quest builds an ETL pipeline because it teaches every stage explicitly; the warehousing quest that follows leans into ELT.

### 🔍 Knowledge Check: ETL vs ELT
- [ ] Why does ELT let you re-run transformations without re-extracting?
- [ ] Name one scenario where ETL is mandatory for compliance reasons
- [ ] Which pattern keeps a permanent raw layer by default?

### ⚡ Quick Wins and Checkpoints
- [ ] **Pattern chosen**: You can justify ETL or ELT for a workload you know
- [ ] **Vocabulary set**: You can define source, staging, and destination

## 🧙‍♂️ Chapter 2: Extract and Transform - The First Two Stages

*Every pipeline begins by pulling data from a source and reshaping it. We'll build each stage as a small, pure function so it can be tested and reused.*

### ⚔️ Skills You'll Forge in This Chapter
- Extracting from an API or file into Python structures
- Writing transforms that are deterministic and side-effect-free
- Separating concerns so each stage can fail and retry independently

### 🏗️ Extract: Pull Raw Data

```python
# etl.py — stage 1: extract
import requests

def extract(url: str) -> list[dict]:
    """Pull raw records from a JSON API. Raises on HTTP errors so the
    orchestrator can retry the task rather than load garbage."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    # Normalize to a list of records regardless of API envelope shape.
    return payload if isinstance(payload, list) else payload.get("data", [])

if __name__ == "__main__":
    rows = extract("https://jsonplaceholder.typicode.com/users")
    print(f"Extracted {len(rows)} records")
```

### 🏗️ Transform: Reshape and Clean

A good transform is **deterministic**: the same input always yields the same output, with no hidden state. That property is what makes the whole pipeline rerunnable.

```python
# etl.py — stage 2: transform
from datetime import datetime, timezone

def transform(rows: list[dict]) -> list[dict]:
    """Select fields, normalize types, and stamp an ingestion time.
    Pure function: no I/O, no globals — easy to unit test."""
    cleaned = []
    for r in rows:
        cleaned.append({
            "user_id": int(r["id"]),
            "name": r["name"].strip(),
            "email": r["email"].strip().lower(),
            "city": r.get("address", {}).get("city", "").strip(),
            "ingested_at": datetime.now(timezone.utc).isoformat(),
        })
    return cleaned
```

### 🔍 Knowledge Check: Extract & Transform
- [ ] Why should `extract` raise on an HTTP error instead of returning `[]`?
- [ ] What makes a transform function "pure," and why does that matter for reruns?
- [ ] Where would you add field validation - and what should happen on a bad row?

## 🧙‍♂️ Chapter 3: Idempotent Loading and Incremental Pipelines

*Loading is where pipelines live or die. The golden rule: **running the pipeline twice must not create two copies of the same data.** That property is called idempotency.*

### ⚔️ Skills You'll Forge in This Chapter
- Idempotent upserts with a natural/primary key
- Incremental loads using a watermark
- Designing loads that are safe to retry mid-failure

### 🏗️ Load: Idempotent Upsert into SQLite

The naive approach - `INSERT` every row - duplicates data on every rerun. Instead, use an **upsert** keyed on a stable identifier so a rerun overwrites rather than duplicates.

```python
# etl.py — stage 3: load (idempotent)
import sqlite3

def load(rows: list[dict], db_path: str = "warehouse.db") -> int:
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY,
            name        TEXT,
            email       TEXT,
            city        TEXT,
            ingested_at TEXT
        )
    """)
    # ON CONFLICT makes this idempotent: rerunning UPDATES the existing row
    # instead of inserting a duplicate. The PRIMARY KEY is the conflict target.
    conn.executemany("""
        INSERT INTO users (user_id, name, email, city, ingested_at)
        VALUES (:user_id, :name, :email, :city, :ingested_at)
        ON CONFLICT(user_id) DO UPDATE SET
            name=excluded.name,
            email=excluded.email,
            city=excluded.city,
            ingested_at=excluded.ingested_at
    """, rows)
    conn.commit()
    count = conn.total_changes
    conn.close()
    return count
```

### 🏗️ Wire the Full Pipeline

```python
# etl.py — orchestrate the three stages with retry on extract
import time

def run_pipeline(url: str) -> None:
    for attempt in range(3):
        try:
            raw = extract(url)
            break
        except requests.RequestException as e:
            wait = 2 ** attempt
            print(f"Extract failed ({e}); retrying in {wait}s")
            time.sleep(wait)
    else:
        raise RuntimeError("Extract failed after 3 attempts")

    clean = transform(raw)
    changed = load(clean)
    print(f"Loaded/updated {changed} rows idempotently")

if __name__ == "__main__":
    run_pipeline("https://jsonplaceholder.typicode.com/users")
    run_pipeline("https://jsonplaceholder.typicode.com/users")  # run twice — still no duplicates
```

Run it twice. The second run updates the same rows instead of duplicating them - that is idempotency in action.

### 🏗️ Incremental Loads with a Watermark

Full loads waste effort once data grows. An **incremental load** moves only records newer than the last successful run, tracked by a **watermark** (a high-water mark such as a timestamp or monotonic id).

```sql
-- Find the watermark: the newest record we have already loaded.
SELECT COALESCE(MAX(updated_at), '1970-01-01') AS watermark FROM users;

-- Then extract only newer rows from the source:
--   SELECT * FROM source_users WHERE updated_at > :watermark;
-- After a successful load, the new MAX(updated_at) becomes the next watermark.
```

This makes reruns cheap **and** correct: combined with the idempotent upsert, even an overlapping window cannot create duplicates.

### 🔍 Knowledge Check: Idempotency & Incrementals
- [ ] What does `ON CONFLICT ... DO UPDATE` guarantee on a rerun?
- [ ] How does a watermark prevent re-processing old data?
- [ ] Why is "idempotent upsert + watermark" safer than either alone?

## 🧙‍♂️ Chapter 4: Orchestration with Airflow DAGs

*A pipeline you run by hand is a chore. A pipeline an orchestrator runs on a schedule, retries on failure, and alerts you when it breaks is **infrastructure**. Apache Airflow models your pipeline as a **DAG** - a Directed Acyclic Graph of tasks with dependencies.*

### ⚔️ Skills You'll Forge in This Chapter
- DAGs, tasks, dependencies, and schedules
- Expressing extract → transform → load as ordered tasks
- Built-in retries and idempotent task design

### 🏗️ The Same Pipeline as an Airflow DAG

```python
# dags/users_etl.py — drop into your Airflow dags/ folder
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from etl import extract, transform, load  # your functions from Chapter 2-3

default_args = {
    "retries": 3,                          # Airflow retries failed tasks for you
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="users_etl",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",                     # run once per day
    catchup=False,
    default_args=default_args,
    tags=["data-engineering", "etl"],
) as dag:

    def _extract(**ctx):
        rows = extract("https://jsonplaceholder.typicode.com/users")
        ctx["ti"].xcom_push(key="raw", value=rows)

    def _transform(**ctx):
        raw = ctx["ti"].xcom_pull(key="raw", task_ids="extract")
        ctx["ti"].xcom_push(key="clean", value=transform(raw))

    def _load(**ctx):
        clean = ctx["ti"].xcom_pull(key="clean", task_ids="transform")
        load(clean)

    t_extract = PythonOperator(task_id="extract", python_callable=_extract)
    t_transform = PythonOperator(task_id="transform", python_callable=_transform)
    t_load = PythonOperator(task_id="load", python_callable=_load)

    # The dependency chain — this is the "directed acyclic" part of the DAG:
    t_extract >> t_transform >> t_load
```

The `>>` operator declares dependencies: `load` cannot start until `transform` succeeds, which cannot start until `extract` succeeds. Because each task is idempotent, Airflow can safely retry any single task without corrupting your data.

### 🔍 Knowledge Check: Orchestration
- [ ] What do the nodes and edges of an Airflow DAG represent?
- [ ] Why must a DAG be **acyclic**?
- [ ] How do Airflow retries rely on your tasks being idempotent?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Run It Twice
**Objective**: Run `etl.py` twice and prove the row count is identical both times.

**Requirements**:
- [ ] Pipeline executes extract, transform, and load
- [ ] `SELECT COUNT(*) FROM users` returns the same number after both runs
- [ ] No `UNIQUE constraint failed` errors

**Validation**: Run `python etl.py`, then re-run it; the table is unchanged in size.

### 🟡 Intermediate Challenge: Make It Incremental
**Objective**: Convert the full load into an incremental one driven by a watermark.

**Requirements**:
- [ ] Compute the current watermark from the destination
- [ ] Extract only records newer than the watermark
- [ ] Keep the idempotent upsert so overlap is harmless

**Validation**: A second run with no new source data loads zero rows.

### 🔴 Advanced Challenge: Orchestrate and Backfill
**Objective**: Run the DAG in Airflow and perform a backfill over a historical window.

**Requirements**:
- [ ] DAG appears and runs in the Airflow UI on a schedule
- [ ] Tasks have retries configured and survive a simulated extract failure
- [ ] A backfill reprocesses past dates without duplicating present data

**Validation**: Trigger the DAG, kill the extract once, and confirm the retry completes the run cleanly.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Pipeline Architect** - You designed an idempotent, orchestrated ETL flow
- ⚙️ **Idempotency Adept** - Your loads are safe to rerun, every time

**🛠️ Skills Unlocked**:
- **Python ETL Engineering** - Build extract, transform, and load stages cleanly
- **Workflow Orchestration** - Express pipelines as scheduled Airflow DAGs

**🔓 Unlocked Quests**:
- Data Warehousing - Model the destination your pipeline feeds
- Apache Spark - Scale your transforms to distributed compute
- Data Quality Engineering - Guard the data your pipeline moves

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Data Warehousing](/quests/1100/data-warehousing/) - Design the analytical destination

**Explore Side Adventures**:
- ⚔️ [Apache Spark](/quests/1100/apache-spark/) - Distribute your transformations
- ⚔️ [Data Quality Engineering](/quests/1100/data-quality/) - Validate every load

### Character Class Recommendations

**💻 Software Developer**: Continue to [Data Warehousing](/quests/1100/data-warehousing/)  
**🏗️ System Engineer**: Explore [Apache Spark](/quests/1100/apache-spark/)  
**📊 Data Scientist**: Advance to [Data Quality Engineering](/quests/1100/data-quality/)

## 📚 Resources

### Official Documentation
- [Apache Airflow Documentation](https://airflow.apache.org/docs/) - DAGs, operators, scheduling
- [Python sqlite3 module](https://docs.python.org/3/library/sqlite3.html) - The standard-library database used here
- [SQLite UPSERT syntax](https://www.sqlite.org/lang_upsert.html) - `ON CONFLICT DO UPDATE`

### Community Resources
- [dbt - the analytics engineering standard for ELT](https://docs.getdbt.com/) - Transform-in-warehouse tooling
- [Awesome Data Engineering](https://github.com/igorbarinov/awesome-data-engineering) - Curated tools and reading
- [r/dataengineering](https://www.reddit.com/r/dataengineering/) - Practitioner community

### Learning Materials
- [The Data Engineering Cookbook](https://github.com/andkret/Cookbook) - Patterns and interview prep
- [Airflow Tutorials](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html) - Hands-on DAG building

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Built a runnable, idempotent ETL script
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1100 - Data Engineering]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Unlocks:** [[Data Warehousing: Design Star Schema & Build Modern Analytics Architecture]] · [[Apache Spark Mastery: Big Data Processing with PySpark & Scala]] · [[Data Quality Engineering: Testing, Validation & Monitoring Frameworks]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
