---
title: 'Data Warehousing: Build a Dimensional Star Schema in SQL'
author: IT-Journey Team
description: 'Build the Analytical Citadel: model OLTP vs OLAP, design star and snowflake schemas, implement slowly changing dimensions, and explore columnar storage.'
excerpt: Design data warehouses with dimensional modeling, star schemas, slowly changing dimensions, and columnar storage
preview: images/previews/data-warehousing-descriptive-subtitle.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1100'
difficulty: 🔴 Hard
estimated_time: 5-6 hours
primary_technology: sql
quest_type: main_quest
quest_series: Data Engineering Mastery
quest_line: The Data Engineer's Ascent
quest_arc: Building the Analytical Citadel
quest_dependencies:
  required_quests:
  - /quests/1100/etl-pipeline-design/
  recommended_quests:
  - /quests/0110/data-modeling/
  unlocks_quests:
  - /quests/1100/apache-spark/
  - /quests/1100/data-quality/
skill_focus: data-engineering
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Solid SQL - SELECT, JOIN, GROUP BY, aggregate functions
  - Understanding of primary and foreign keys
  - Completion of the ETL Pipeline Design quest (recommended)
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - SQLite (bundled with Python) or DuckDB for the columnar demo
  - A text editor or IDE (VS Code recommended)
  skill_level_indicators:
  - Comfortable writing multi-table JOIN queries
  - Ready to think in terms of analytics, not transactions
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A working star schema with one fact and at least two dimension tables
  skill_demonstrations:
  - Can explain the difference between OLTP and OLAP workloads
  - Can design a star schema from a set of business questions
  knowledge_checks:
  - Understands star versus snowflake schemas and their trade-offs
  - Can implement a Type 2 slowly changing dimension
permalink: /quests/1100/data-warehousing/
categories:
- Quests
- Data-Engineering
- Hard
tags:
- '1100'
- sql
- data-warehouse
- main_quest
- data-engineering
- hands-on
- gamified-learning
keywords:
  primary:
  - '1100'
  - sql
  - data-warehouse
  secondary:
  - main_quest
  - data-engineering
  - hands-on
  - gamified-learning
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1100 (12) Quest: Main Quest - Data Warehousing'
rewards:
  badges:
  - 🏆 Citadel Architect - Designed a dimensional star schema
  - 🌟 Dimension Keeper - Mastered slowly changing dimensions
  skills_unlocked:
  - 🛠️ Dimensional Modeling
  - 🧠 OLAP Schema Design
  progression_points: 80
  unlocks_features:
  - Access to the Apache Spark and Data Quality quests
layout: quest
---
*Greetings, brave adventurer! Your aqueduct from the ETL quest now delivers clean water - but where does it pool? You stand before the **Analytical Citadel**, the great reservoir where data is shaped not for fast single-row transactions but for sweeping questions across millions of rows: "What were sales by region by quarter for the last five years?" Build the citadel with the wrong layout and every report crawls; build it as a **dimensional model** and queries fly.*

*Whether you have only ever queried application databases or you are formalizing the analytics layer your company half-built, this quest forges the discipline of the warehouse: OLTP versus OLAP, star and snowflake schemas, fact and dimension tables, slowly changing dimensions, and the columnar engines that make it all fast.*

## 📖 The Legend Behind This Quest

*Application databases were built for speed at the level of a single order, a single user, a single click. When the kingdom's strategists demanded answers across all orders, all users, all time, those same databases buckled. A new architecture arose - the **data warehouse** - optimized not to write one row quickly but to read billions efficiently. Its master plan was **dimensional modeling**, devised by Ralph Kimball, and it remains the blueprint analysts trust today.*

*This quest teaches the "why" behind every fact table and every dimension. Master it and the rest of the tier - distributed Spark jobs, streaming aggregations, quality contracts - all have a place to land.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **OLTP vs OLAP** - Explain transactional versus analytical workloads and why they need different designs
- [ ] **Star schema modeling** - Design a central fact table surrounded by dimension tables
- [ ] **Snowflake schemas** - Normalize dimensions and weigh the trade-offs
- [ ] **Slowly Changing Dimensions** - Track history correctly as dimension attributes change over time

### Secondary Objectives (Bonus Achievements)
- [ ] **Columnar storage** - Understand why analytics engines store data by column
- [ ] **Grain definition** - Pin down exactly what one fact row represents
- [ ] **Surrogate keys** - Decouple the warehouse from source system identifiers

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Describe why an OLTP schema is a poor fit for analytics
- [ ] Design a star schema directly from a list of business questions
- [ ] Implement a Type 2 SCD that preserves the full history of a record
- [ ] Explain why columnar storage accelerates aggregate queries

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Solid SQL: `SELECT`, `JOIN`, `GROUP BY`, aggregate functions
- [ ] Comfort with primary keys and foreign keys
- [ ] Completion of [ETL Pipeline Design](/quests/1100/etl-pipeline-design/) (recommended)

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] SQLite (ships with Python) for the schema work
- [ ] Optional: DuckDB for the columnar storage demo
- [ ] A text editor or IDE (VS Code recommended)

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can write multi-table JOIN and GROUP BY queries
- [ ] You are ready to think in analytics, not single-row transactions
- [ ] Ready for 5-6 hours of focused, hands-on modeling

## 🌍 Choose Your Adventure Platform

*All the SQL runs in SQLite, which ships with Python everywhere. The optional columnar demo uses DuckDB. Choose your setup path.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
brew install python duckdb
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip duckdb
sqlite3 --version
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install Python.Python.3.12 DuckDB.cli
py -3 -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip duckdb
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y python3 python3-venv sqlite3   # Debian/Ubuntu
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip duckdb
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# DuckDB needs no server and runs in any container or notebook:
pip install duckdb
python -c "import duckdb; print(duckdb.sql('SELECT 42 AS answer'))"
```

</details>

## 🧙‍♂️ Chapter 1: OLTP vs OLAP - Two Worlds of Data

*The same data can be stored two completely different ways depending on the questions you ask of it.*

### ⚔️ Skills You'll Forge in This Chapter
- The distinction between transactional and analytical workloads
- Why one schema cannot serve both well
- The vocabulary of facts, dimensions, and grain

### 🏗️ The Two Workloads

| Aspect | **OLTP** (Online Transaction Processing) | **OLAP** (Online Analytical Processing) |
| --- | --- | --- |
| Typical query | Insert/update one order; read one customer | Aggregate millions of rows across time |
| Optimized for | Many small, concurrent writes | Few large, read-heavy scans |
| Schema | Highly normalized (3NF), no redundancy | Denormalized star schema, redundancy embraced |
| Example system | PostgreSQL backing an app | Snowflake, BigQuery, Redshift, DuckDB |
| Row vs column | Row-oriented storage | Column-oriented storage |

An OLTP schema spreads a sale across `orders`, `order_items`, `customers`, `products`, and `addresses` to avoid duplication. Answering "total revenue by city by month" then demands five-way joins over millions of rows. The warehouse **denormalizes** that into a shape built for exactly such questions.

### 🔍 Knowledge Check: OLTP vs OLAP
- [ ] Why is heavy normalization great for OLTP but painful for OLAP?
- [ ] What does "denormalized for analytics" buy you, and what does it cost?
- [ ] Name two OLAP engines and two OLTP databases

## 🧙‍♂️ Chapter 2: Star Schemas - Facts and Dimensions

*The star schema is the heart of dimensional modeling: one central **fact** table of measurements, surrounded by **dimension** tables of descriptive context. Drawn out, it looks like a star.*

### ⚔️ Skills You'll Forge in This Chapter
- Identifying facts (measures) versus dimensions (context)
- Defining the **grain** - what one fact row means
- Building a star schema in SQL with surrogate keys

### 🏗️ Anatomy of a Star

- **Fact table** - the numbers you measure: quantities, amounts, counts. One row per event at a defined grain (e.g., "one row per product per order").
- **Dimension tables** - the *who, what, where, when*: customers, products, dates, stores. These give your numbers meaning.
- **Surrogate keys** - integer keys minted by the warehouse (`date_key`, `product_key`) instead of reusing source ids, so the warehouse stays stable when sources change.

```sql
-- Dimension tables: descriptive context, one row per entity.
CREATE TABLE dim_date (
    date_key   INTEGER PRIMARY KEY,   -- e.g. 20250613
    full_date  TEXT,                  -- '2025-06-13'
    year       INTEGER,
    quarter    INTEGER,
    month      INTEGER,
    day_name   TEXT
);

CREATE TABLE dim_product (
    product_key  INTEGER PRIMARY KEY, -- surrogate key
    product_id   TEXT,                -- natural key from the source system
    name         TEXT,
    category     TEXT
);

CREATE TABLE dim_customer (
    customer_key INTEGER PRIMARY KEY,
    customer_id  TEXT,
    name         TEXT,
    city         TEXT
);

-- Fact table: measures + foreign keys to every dimension.
-- Grain: one row per product per order line.
CREATE TABLE fact_sales (
    sale_id       INTEGER PRIMARY KEY,
    date_key      INTEGER REFERENCES dim_date(date_key),
    product_key   INTEGER REFERENCES dim_product(product_key),
    customer_key  INTEGER REFERENCES dim_customer(customer_key),
    quantity      INTEGER,            -- additive measure
    amount        REAL                -- additive measure
);
```

Now the dreaded "revenue by city by quarter" is a clean, fast query:

```sql
SELECT c.city, d.year, d.quarter, SUM(f.amount) AS revenue
FROM fact_sales f
JOIN dim_customer c ON c.customer_key = f.customer_key
JOIN dim_date     d ON d.date_key     = f.date_key
GROUP BY c.city, d.year, d.quarter
ORDER BY revenue DESC;
```

### 🔍 Knowledge Check: Star Schemas
- [ ] What is the "grain" of `fact_sales`, and why must you define it first?
- [ ] Why use a surrogate `product_key` instead of the source `product_id`?
- [ ] Which columns are measures and which are context?

## 🧙‍♂️ Chapter 3: Snowflake Schemas and Slowly Changing Dimensions

*Two refinements separate a working warehouse from a robust one: deciding how far to normalize dimensions, and deciding how to record history when a dimension changes.*

### ⚔️ Skills You'll Forge in This Chapter
- Star versus snowflake normalization trade-offs
- The three classic Slowly Changing Dimension (SCD) types
- Implementing a Type 2 SCD that preserves full history

### 🏗️ Snowflake: Normalizing the Dimensions

A **snowflake schema** normalizes dimensions into sub-tables (e.g., `dim_product` → `dim_category` → `dim_department`). It saves storage and removes redundancy but adds joins and complexity.

```sql
-- Snowflaked: category extracted into its own table.
CREATE TABLE dim_category (
    category_key INTEGER PRIMARY KEY,
    category     TEXT,
    department   TEXT
);
-- dim_product now references dim_category instead of repeating the text.
ALTER TABLE dim_product ADD COLUMN category_key INTEGER REFERENCES dim_category(category_key);
```

**Rule of thumb:** prefer **star** (denormalized) for query speed and simplicity - storage is cheap and analysts love fewer joins. Reach for **snowflake** only when a dimension is huge, frequently reused, or governed centrally.

### 🏗️ Slowly Changing Dimensions

When a customer moves city, what should history show? The SCD types answer this:

- **Type 1** - overwrite the old value. Simple, but history is lost.
- **Type 2** - add a new row with effective dates, keeping the old one. Full history preserved.
- **Type 3** - add a "previous value" column. Limited history (one prior value).

```sql
-- Type 2 SCD: track history with effective dates and a current flag.
CREATE TABLE dim_customer_scd2 (
    customer_key   INTEGER PRIMARY KEY,  -- surrogate; a new key per version
    customer_id    TEXT,                 -- natural key, stable across versions
    name           TEXT,
    city           TEXT,
    valid_from     TEXT,
    valid_to       TEXT,                 -- NULL while current
    is_current     INTEGER               -- 1 for the active version
);

-- When customer C1 moves from Austin to Denver:
-- 1) Close the old version.
UPDATE dim_customer_scd2
SET valid_to = '2025-06-13', is_current = 0
WHERE customer_id = 'C1' AND is_current = 1;

-- 2) Insert the new current version.
INSERT INTO dim_customer_scd2 (customer_id, name, city, valid_from, valid_to, is_current)
VALUES ('C1', 'Ada Lovelace', 'Denver', '2025-06-13', NULL, 1);
```

Now a fact row joined on the **surrogate** `customer_key` forever reflects the city the customer lived in *at the time of the sale* - history stays correct.

### 🔍 Knowledge Check: Snowflake & SCDs
- [ ] When is a snowflake schema worth the extra joins?
- [ ] Which SCD type loses history, and which preserves it fully?
- [ ] Why does a Type 2 SCD require a *new surrogate key* per version?

## 🧙‍♂️ Chapter 4: Columnar Storage - Why Analytics Engines Are Fast

*The final secret of the warehouse is physical, not logical: analytical engines store data **by column, not by row**.*

### ⚔️ Skills You'll Forge in This Chapter
- Row-oriented versus column-oriented storage
- Why columnar layout accelerates aggregates and compresses well
- Seeing it in action with DuckDB

### 🏗️ Rows vs Columns

A row store keeps `(sale_id, date, product, amount)` together on disk - perfect for reading one whole order. But `SUM(amount)` over a billion rows must then touch every column of every row. A **column store** keeps all `amount` values contiguously, so the engine reads *only* that column - far less I/O, and columns of similar values compress dramatically.

```python
# columnar_demo.py — DuckDB is an embedded columnar OLAP engine
import duckdb

duckdb.sql("CREATE TABLE sales AS SELECT range AS id, random() AS amount FROM range(5_000_000)")
# Only the 'amount' column is scanned — columnar engines shine on aggregates.
print(duckdb.sql("SELECT COUNT(*), SUM(amount), AVG(amount) FROM sales"))
```

This is why Snowflake, BigQuery, Redshift, Parquet files, and DuckDB are all columnar: aggregate analytics over wide tables is exactly the workload columns are built for.

### 🔍 Knowledge Check: Columnar Storage
- [ ] Why does `SUM(amount)` run faster on a column store than a row store?
- [ ] Why do columns compress better than rows?
- [ ] Name three columnar systems you might meet in production

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Build the Star
**Objective**: Create the `fact_sales` star schema with `dim_date`, `dim_product`, and `dim_customer`, then load a few rows.

**Requirements**:
- [ ] One fact table and at least two dimension tables
- [ ] Surrogate keys on all dimensions
- [ ] A working "revenue by dimension" aggregate query

**Validation**: Your GROUP BY query returns sensible totals.

### 🟡 Intermediate Challenge: Track History
**Objective**: Implement a Type 2 SCD for customers and record a city change.

**Requirements**:
- [ ] `valid_from`, `valid_to`, and `is_current` columns
- [ ] Old version closed, new version inserted on change
- [ ] A query that shows both historical and current versions

**Validation**: A sale before the move still maps to the old city.

### 🔴 Advanced Challenge: Star to Snowflake and Columnar
**Objective**: Snowflake the product dimension and benchmark an aggregate in DuckDB.

**Requirements**:
- [ ] Extract category into `dim_category` with a foreign key
- [ ] Load a multi-million-row fact table into DuckDB
- [ ] Compare the aggregate query against a row-store equivalent and note the difference

**Validation**: You can explain the speed difference in terms of columnar I/O.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Citadel Architect** - You designed a dimensional star schema
- 🌟 **Dimension Keeper** - You preserve history with slowly changing dimensions

**🛠️ Skills Unlocked**:
- **Dimensional Modeling** - Facts, dimensions, grain, and surrogate keys
- **OLAP Schema Design** - Star, snowflake, and columnar trade-offs

**🔓 Unlocked Quests**:
- Apache Spark - Build these tables at petabyte scale
- Data Quality Engineering - Enforce contracts on your warehouse tables

**📊 Progression Points**: +80 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Apache Spark](/quests/1100/apache-spark/) - Scale dimensional builds with distributed compute

**Explore Side Adventures**:
- ⚔️ [Data Quality Engineering](/quests/1100/data-quality/) - Validate every dimension and fact
- ⚔️ [Stream Processing](/quests/1100/stream-processing/) - Feed the warehouse in real time

### Character Class Recommendations

**💻 Software Developer**: Continue to [Apache Spark](/quests/1100/apache-spark/)  
**🏗️ System Engineer**: Explore [Stream Processing](/quests/1100/stream-processing/)  
**📊 Data Scientist**: Advance to [Data Quality Engineering](/quests/1100/data-quality/)

## 📚 Resources

### Official Documentation
- [DuckDB Documentation](https://duckdb.org/docs/) - Embedded columnar OLAP engine
- [SQLite SQL Reference](https://www.sqlite.org/lang.html) - Used for the schema work here
- [Kimball Dimensional Modeling Techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/) - The canonical reference

### Community Resources
- [dbt Star Schema guidance](https://docs.getdbt.com/) - Modeling marts in modern warehouses
- [Awesome Data Engineering](https://github.com/igorbarinov/awesome-data-engineering) - Tools and reading
- [Snowflake vs star schema discussions](https://www.reddit.com/r/dataengineering/) - Practitioner debates

### Learning Materials
- [The Data Warehouse Toolkit (Kimball) overview](https://www.kimballgroup.com/) - Dimensional modeling bible
- [Apache Parquet format](https://parquet.apache.org/) - The columnar file format behind modern lakes

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Built a working star schema with facts and dimensions
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1100 - Data Engineering]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Prerequisites:** [[ETL Pipeline Design: Build Scalable Data Pipelines with Python]] **Unlocks:** [[Apache Spark Mastery: Big Data Processing with PySpark & Scala]] · [[Data Quality Engineering: Testing, Validation & Monitoring Frameworks]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
