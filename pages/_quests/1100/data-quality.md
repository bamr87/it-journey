---
title: 'Data Quality Engineering: Validation & Monitoring'
author: IT-Journey Team
description: 'Build data quality into your pipelines: master the six quality dimensions, profiling, validation suites, data contracts, anomaly detection, and lineage.'
excerpt: Guard your pipelines with profiling, validation, data contracts, expectation suites, and lineage
preview: images/previews/data-quality-engineering-descriptive-subtitle.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1100'
difficulty: 🔴 Hard
estimated_time: 3-4 hours
primary_technology: python
quest_type: main_quest
quest_series: Data Engineering Mastery
quest_line: The Data Engineer's Ascent
quest_arc: Guardians of the Data
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/1100/etl-pipeline-design/
  - /quests/1100/apache-spark/
  - /quests/1100/stream-processing/
  unlocks_quests: []
skill_focus: data-engineering
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Comfortable writing functions and using packages in Python 3.10+
  - Basic SQL and how relational tables and keys work
  - The ETL stages and idempotency from ETL Pipeline Design
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Python 3.10+ with pip and venv
  - A text editor or IDE (VS Code recommended)
  skill_level_indicators:
  - Can build and run a small Python data script end to end
  - Ready to think adversarially about how data goes wrong
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A validation suite that fails a pipeline on bad data
  skill_demonstrations:
  - Can profile a dataset and write expectation-style checks
  - Can author a data contract and enforce it at ingestion
  knowledge_checks:
  - Understands the six data-quality dimensions
  - Can describe column, table, and freshness lineage
permalink: /quests/1100/data-quality/
categories:
- Quests
- Data-Engineering
- Hard
tags:
- '1100'
- data-quality
- great-expectations
- main_quest
- data-engineering
- hands-on
keywords:
  primary:
  - '1100'
  - data-quality
  - python
  secondary:
  - data-contracts
  - profiling
  - lineage
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1100 (12) Quest: Main Quest - Data Quality'
rewards:
  badges:
  - 🏆 Guardian of the Data - Caught bad data before it poisoned the kingdom
  - 🔬 Master of the Expectation - Profiled, validated, and contracted every dataset
  skills_unlocked:
  - 🛠️ Data Profiling & Validation Suites
  - 🧠 Data Contracts, Anomaly Detection & Lineage
  progression_points: 75
  unlocks_features:
  - Completes the core Level 1100 Data Engineering quest line
layout: quest
---
*Greetings, brave adventurer! You have built aqueducts, commanded clusters, and ridden endless streams of events. But a pipeline that moves data flawlessly is still worthless if the data itself is wrong - a null where a price should be, a duplicate order, a timestamp from the future. Every dashboard, every model, every decision downstream drinks from your reservoir, and poison flows just as easily as clean water. This quest, **Data Quality Engineering**, teaches you to stand guard at the gates and let no bad data pass.*

*Whether you have been burned by a silent data corruption that broke a report at the worst possible moment, or you already write the occasional ad-hoc check and want a real framework, this adventure forges the final discipline of the data engineer: profiling, validation, data contracts, expectation suites, anomaly detection, and lineage - the armor that protects everything you have built.*

## 📖 The Legend Behind This Quest

*In the early ages, data quality was an afterthought - someone noticed a wrong number weeks later, traced it back through a tangle of jobs, and patched it by hand. The kingdoms that thrived learned a hard truth borrowed from software engineering: you do not hope data is correct, you **test** it, automatically, at every gate, and you **fail loudly** the moment it is not.*

*This quest brings the rigor of testing to data. You will profile datasets to learn their shape, write expectations that encode "what good looks like," author contracts that bind producers and consumers, detect anomalies that slip past static rules, and trace lineage so that when something does break, you know exactly what it touched. Master this and the data your pipelines move becomes trustworthy by design.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **The Quality Dimensions** - Explain completeness, validity, accuracy, consistency, uniqueness, and timeliness
- [ ] **Profiling** - Inspect a dataset to learn its real distributions, ranges, and null rates
- [ ] **Validation & Expectations** - Write Great-Expectations-style checks that fail the pipeline on bad data
- [ ] **Data Contracts** - Author and enforce a schema-and-rules contract at the ingestion boundary

### Secondary Objectives (Bonus Achievements)
- [ ] **Anomaly Detection** - Catch quality drift that static rules miss (volume drops, distribution shifts)
- [ ] **Data Lineage** - Trace a field from source to dashboard so failures are debuggable
- [ ] **Quarantine & Dead-Letter** - Route bad rows aside instead of silently dropping them

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Map a real bug to one of the six quality dimensions
- [ ] Profile a dataset and turn its profile into concrete expectations
- [ ] Write a check that blocks a pipeline when a contract is violated
- [ ] Explain how lineage shortens a 3 a.m. data incident

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Comfortable writing Python functions and using `pip` packages
- [ ] Basic SQL and how relational tables and keys work
- [ ] The ETL stages and idempotency (complete [ETL Pipeline Design](/quests/1100/etl-pipeline-design/) first)

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Python 3.10+ with `pip` and `venv`
- [ ] A text editor or IDE (VS Code recommended)

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can build and run a small Python data script end to end
- [ ] You are ready to think adversarially about how data goes wrong
- [ ] Ready for 3-4 hours of focused, hands-on building

## 🌍 Choose Your Adventure Platform

*Everything here is plain Python with pandas and a validation library, so the lab runs anywhere. Only Python setup differs; then everyone meets at the same `pip install`.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
brew install python
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip pandas great-expectations pandera
python -c "import pandas, great_expectations; print('ready')"
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install Python.Python.3.12
py -3 -m venv .venv; .\.venv\Scripts\activate
pip install --upgrade pip pandas great-expectations pandera
python -c "import pandas, great_expectations; print('ready')"
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y python3 python3-venv
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip pandas great-expectations pandera
python -c "import pandas, great_expectations; print('ready')"
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# Any Codespace or container with Python works.
pip install pandas great-expectations pandera
```

</details>

## 🧙‍♂️ Chapter 1: The Six Dimensions of Data Quality

*"Bad data" is vague. To fight it, name it. Every data defect falls into one of six dimensions, and naming the dimension tells you which check to write.*

### ⚔️ Skills You'll Forge in This Chapter
- The six quality dimensions
- Mapping a real defect to a dimension
- Why naming the dimension points you to the fix

### 🏗️ The Six Dimensions

| Dimension | Question it answers | Example failure |
| --- | --- | --- |
| **Completeness** | Is required data present? | 12% of orders have a null `customer_id` |
| **Validity** | Does data match its format/type/range? | `email` = "not-an-email"; `age` = -3 |
| **Accuracy** | Does data reflect reality? | A product priced at $1 that should be $100 |
| **Consistency** | Does data agree across systems? | Order total ≠ sum of line items |
| **Uniqueness** | Are there unwanted duplicates? | The same order id appears twice |
| **Timeliness** | Is data fresh enough? | The "daily" feed last updated three days ago |

Naming the dimension is half the battle: a null-rate problem is *completeness* (write a not-null expectation), a future timestamp is *validity* (write a range check), a duplicate key is *uniqueness* (write a uniqueness check). The taxonomy turns a vague "the data looks wrong" into a specific, testable assertion.

### 🔍 Knowledge Check: Dimensions
- [ ] Which dimension does a duplicate primary key violate?
- [ ] "The total doesn't match the line items" is which dimension?
- [ ] Why does naming the dimension help you write the right check?

### ⚡ Quick Wins and Checkpoints
- [ ] **Named the six**: You can list all six dimensions
- [ ] **Classified a bug**: You mapped a real defect to its dimension

## 🧙‍♂️ Chapter 2: Profiling - Know Your Data Before You Guard It

*You cannot guard what you do not understand. **Profiling** measures a dataset's actual shape - types, ranges, null rates, cardinality, distributions - so your checks reflect reality instead of guesswork.*

### ⚔️ Skills You'll Forge in This Chapter
- Profiling a dataset's real distributions
- Turning a profile into candidate expectations
- Spotting the surprises hiding in real data

### 🏗️ Profile a Dataset in Python

```python
# profile.py — learn the real shape of a dataset before writing any rule
import pandas as pd

df = pd.read_csv("orders.csv")

print("Shape:", df.shape)
print("\nDtypes:\n", df.dtypes)
print("\nNull rate per column:\n", (df.isna().mean() * 100).round(1))
print("\nNumeric summary:\n", df.describe())
print("\nUnique customers:", df["customer_id"].nunique())
print("Duplicate order_ids:", df["order_id"].duplicated().sum())
print("Amount range:", df["amount"].min(), "to", df["amount"].max())
```

Profiling routinely surprises you: a "never null" column that is 3% null, an `amount` with a negative minimum (a refund? a bug?), a "unique" id with duplicates. Each surprise becomes a candidate expectation. The lesson: **derive your rules from the data's reality, then tighten them**, rather than inventing rules in a vacuum.

### 🔍 Knowledge Check: Profiling
- [ ] What does a column's null rate tell you about completeness?
- [ ] Why derive expectations from a profile instead of guessing?
- [ ] What might a negative value in an `amount` column reveal?

## 🧙‍♂️ Chapter 3: Validation with Expectation Suites

*Profiling tells you what *is*; validation enforces what *should be*. An **expectation** is a single testable assertion about a column or table; a **suite** is a collection of them that gates your pipeline.*

### ⚔️ Skills You'll Forge in This Chapter
- Writing expectations (Great-Expectations style)
- Assembling a suite that fails on bad data
- A lightweight alternative when you cannot add a heavy dependency

### 🏗️ A Great-Expectations-Style Suite

Great Expectations is the de-facto framework: you assert expectations, and it validates a batch and produces a report.

```python
# validate_ge.py — assert expectations against a batch and fail on violation
import great_expectations as gx
import pandas as pd

context = gx.get_context()
df = pd.read_csv("orders.csv")
batch = context.sources.add_pandas("orders_src").read_dataframe(df)

# Each line below encodes one dimension as a concrete, testable rule:
batch.expect_column_values_to_not_be_null("order_id")          # completeness
batch.expect_column_values_to_be_unique("order_id")            # uniqueness
batch.expect_column_values_to_be_between("amount", 0, 100000)  # validity
batch.expect_column_values_to_match_regex("email", r"[^@]+@[^@]+\.[^@]+")  # validity

result = batch.validate()
if not result.success:
    raise SystemExit("Data quality FAILED — blocking the pipeline")  # fail loudly
print("Data quality PASSED")
```

### 🏗️ A Dependency-Free Validator

When you cannot add a framework, the same idea is just assertions in a function. This is the pattern to drop directly into a pipeline stage:

```python
# validate_simple.py — the same expectations as plain, dependency-free checks
import pandas as pd

def validate(df: pd.DataFrame) -> list[str]:
    """Return a list of violations; an empty list means the batch is clean."""
    errors = []
    if df["order_id"].isna().any():
        errors.append("completeness: null order_id")
    if df["order_id"].duplicated().any():
        errors.append("uniqueness: duplicate order_id")
    if not df["amount"].between(0, 100_000).all():
        errors.append("validity: amount out of range")
    if not df["email"].str.contains(r"[^@]+@[^@]+\.[^@]+", regex=True).all():
        errors.append("validity: malformed email")
    return errors

violations = validate(pd.read_csv("orders.csv"))
if violations:
    raise SystemExit("Data quality FAILED:\n  - " + "\n  - ".join(violations))
print("Data quality PASSED")
```

The principle is identical to unit testing code: assert what "good" looks like, run it on every batch, and stop the line when an assertion fails.

### 🔍 Knowledge Check: Validation
- [ ] What is the difference between an expectation and a suite?
- [ ] Why should a failed validation *block* the pipeline rather than warn?
- [ ] How does an expectation suite resemble a unit-test suite?

## 🧙‍♂️ Chapter 4: Data Contracts, Anomaly Detection, and Lineage

*Validation guards one dataset. **Contracts** guard the agreement between teams, **anomaly detection** catches what static rules miss, and **lineage** lets you trace a failure to its source.*

### ⚔️ Skills You'll Forge in This Chapter
- Authoring and enforcing a data contract
- Detecting anomalies beyond fixed thresholds
- Reading lineage to debug incidents

### 🏗️ A Data Contract

A **data contract** is an explicit, version-controlled agreement: the producer promises a schema and a set of guarantees; the consumer can rely on them. Enforce it at the ingestion boundary so a breaking change is caught at the door, not three dashboards later. Here it is as a `pandera` schema:

```python
# contract.py — a data contract enforced at ingestion with pandera
import pandera as pa
from pandera import Column, Check

orders_contract = pa.DataFrameSchema({
    "order_id":    Column(int,   Check.greater_than(0), unique=True, nullable=False),
    "customer_id": Column(int,   nullable=False),
    "amount":      Column(float, Check.in_range(0, 100_000)),
    "email":       Column(str,   Check.str_matches(r"[^@]+@[^@]+\.[^@]+")),
    "created_at":  Column(pa.DateTime),
}, strict=True)   # strict=True rejects unexpected/extra columns — a schema change is a contract break

# At the ingestion boundary, validate or refuse the batch entirely:
import pandas as pd
orders_contract.validate(pd.read_csv("orders.csv"), lazy=True)  # collects ALL failures at once
```

### 🏗️ Anomaly Detection: Beyond Static Rules

Static rules cannot foresee everything. If yesterday's feed had 1,000,000 rows and today's has 4,000, every row may be individually *valid* yet the batch is clearly broken. **Anomaly detection** compares a batch against its own history:

```python
# anomaly.py — flag a batch whose volume deviates far from the recent norm
import statistics

recent_row_counts = [1_004_212, 998_330, 1_010_540, 1_001_220]   # last 4 days
today = 4_000

mean = statistics.mean(recent_row_counts)
stdev = statistics.pstdev(recent_row_counts)
z = (today - mean) / stdev if stdev else 0
if abs(z) > 3:   # more than 3 standard deviations from the recent mean
    raise SystemExit(f"Anomaly: row count {today} is {z:.1f}σ from normal — investigate")
```

The same idea applies to null rates, value distributions, and freshness - watch the *shape* over time, not just each row.

### 🏗️ Data Lineage

**Lineage** records where each dataset and field comes from and what depends on it: `source.orders → staging.orders → marts.daily_revenue → the CEO dashboard`. When `daily_revenue` looks wrong, lineage tells you instantly which upstream tables and which downstream consumers are affected - turning a multi-hour archaeology dig into a single graph lookup. Tools like dbt (column-level lineage), OpenLineage, and DataHub capture it automatically.

### 🔍 Knowledge Check: Contracts, Anomalies, Lineage
- [ ] What does `strict=True` in a contract protect against?
- [ ] Why can a batch of individually valid rows still be an anomaly?
- [ ] How does lineage shorten a data incident investigation?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Profile and Expect
**Objective**: Profile a real CSV, then write three expectations derived from its actual profile.

**Requirements**:
- [ ] A profile reporting null rates, ranges, and duplicates
- [ ] At least three expectations, each tied to a named dimension
- [ ] One expectation that deliberately catches a real defect you found

**Validation**: Running the suite on a corrupted copy fails; on a clean copy it passes.

### 🟡 Intermediate Challenge: Enforce a Contract
**Objective**: Author a `pandera` (or equivalent) contract and wire it into an ingestion step that refuses bad batches.

**Requirements**:
- [ ] A schema covering types, ranges, nullability, and uniqueness
- [ ] `strict` mode rejecting unexpected columns
- [ ] Lazy validation that reports *all* violations, not just the first

**Validation**: Adding an extra column or a bad value causes ingestion to fail with a clear report.

### 🔴 Advanced Challenge: Quarantine, Detect, and Trace
**Objective**: Build a stage that quarantines bad rows, flags a volume/distribution anomaly, and documents the dataset's lineage.

**Requirements**:
- [ ] Bad rows routed to a quarantine/dead-letter table, not silently dropped
- [ ] An anomaly check on row count or null rate against recent history
- [ ] A written lineage map from source to final consumer

**Validation**: A corrupted batch leaves clean rows flowing, quarantines the bad ones, raises the anomaly, and you can trace the field end to end.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Guardian of the Data** - You caught bad data before it poisoned the kingdom
- 🔬 **Master of the Expectation** - You profiled, validated, and contracted every dataset

**🛠️ Skills Unlocked**:
- **Data Profiling & Validation Suites** - Encode "what good looks like" and enforce it
- **Data Contracts, Anomaly Detection & Lineage** - Guard agreements, drift, and provenance

**🔓 Unlocked Quests**:
- You have completed the core Data Engineering quest line - advance to the next Master-tier theme

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Machine Learning Fundamentals](/quests/1101/) - Feed trustworthy data into models (Level 1101)

**Explore Side Adventures**:
- ⚔️ [Apache Spark](/quests/1100/apache-spark/) - Run these checks at distributed scale
- ⚔️ [Stream Processing](/quests/1100/stream-processing/) - Validate events in flight

### Character Class Recommendations

**💻 Software Developer**: Bring data-testing discipline back to [ETL Pipeline Design](/quests/1100/etl-pipeline-design/)  
**🏗️ System Engineer**: Scale checks with [Apache Spark](/quests/1100/apache-spark/)  
**📊 Data Scientist**: Guard model inputs, then advance toward the Machine Learning tier

## 📚 Resources

### Official Documentation
- [Great Expectations Documentation](https://docs.greatexpectations.io/) - Expectations, suites, and data docs
- [pandera Documentation](https://pandera.readthedocs.io/) - DataFrame schemas and contracts in Python
- [dbt Tests](https://docs.getdbt.com/docs/build/data-tests) - Testing data in the warehouse
- [OpenLineage](https://openlineage.io/) - An open standard for data lineage

### Community Resources
- [Data Contracts (Andrew Jones)](https://www.datacontract.com/) - Patterns and templates
- [The Six Dimensions of Data Quality (DAMA)](https://www.dama.org/) - The canonical taxonomy
- [Awesome Data Quality](https://github.com/MeltanoLabs/awesome-data-quality) - Curated tools and reading

### Learning Materials
- [Monte Carlo: Data Observability](https://www.montecarlodata.com/blog-what-is-data-observability/) - Anomaly detection in practice
- [Designing Data-Intensive Applications](https://dataintensive.net/) - Reliability and correctness foundations

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Profiled a dataset and derived expectations from it
- [ ] ✅ Built a validation suite that blocks bad data
- [ ] ✅ Authored and enforced a data contract
- [ ] ✅ Added an anomaly check and documented lineage
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1100 - Data Engineering]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Requires:** [[ETL Pipeline Design: Build Scalable Data Pipelines with Python]] **Related:** [[Apache Spark Mastery: Big Data Processing with PySpark & Scala]] · [[Stream Processing: Real-Time Data with Apache Kafka & Flink]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
