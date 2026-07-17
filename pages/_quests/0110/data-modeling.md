---
title: 'Data Modeling: Schema Design and Database Relationships'
author: IT-Journey Team
description: 'Turn fuzzy requirements into solid database schemas using entity-relationship modeling, normalization to 3NF, and one-to-many and many-to-many relationships.'
excerpt: Master ER modeling, normalization, relationships, and schema design to build databases that scale.
preview: images/previews/data-modeling-schema-design-quest-title-and-relat.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '0110'
difficulty: 🟡 Medium
estimated_time: 75-90 minutes
primary_technology: sql
quest_type: main_quest
quest_series: Database Mastery
quest_line: The Adventurer's Data Keep
quest_arc: Foundations of the Relational Realm
quest_dependencies:
  required_quests:
  - /quests/0110/database-fundamentals/
  recommended_quests: []
  unlocks_quests:
  - /quests/0110/sql-mastery/
  - /quests/0110/query-optimization/
skill_focus: data-engineering
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Completion of Database Fundamentals (recommended)
  - Comfort with CREATE TABLE and primary/foreign keys
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - PostgreSQL 14+ (or Docker to run it)
  skill_level_indicators:
  - Understands tables, rows, and keys
  - Ready to translate requirements into structure
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - An ER model implemented as a normalized schema
  skill_demonstrations:
  - Can draw an ER diagram for a given domain
  - Can implement a many-to-many relationship with a junction table
  knowledge_checks:
  - Understands cardinality and participation
  - Can normalize a table through 3NF
permalink: /quests/0110/data-modeling/
categories:
- Quests
- Data-Engineering
- Medium
tags:
- '0110'
- sql
- main_quest
- data-engineering
- hands-on
- gamified-learning
keywords:
  primary:
  - '0110'
  - sql
  - main_quest
  secondary:
  - data-engineering
  - er-modeling
  - normalization
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 0110 (6) Quest: Main Quest - ER Modeling & Schema Design'
rewards:
  badges:
  - 🏆 Cartographer of Data - Drew an ER map of an entire domain
  - 🛡️ Architect of the Schema - Designed normalized, relationship-rich tables
  skills_unlocked:
  - 🛠️ Entity-Relationship Modeling
  - 🧠 Normalization Through 3NF
  progression_points: 75
  unlocks_features:
  - Deeper schema-design challenges in the Database Mastery line
layout: quest
---
*Greetings, brave adventurer! Before you can query a kingdom's data, someone must first **draw its map**. That mapmaker is you. This quest, **Data Modeling**, teaches the discipline of turning vague human requirements - "we need to track students, courses, and who enrolled in what" - into a precise, normalized schema that the database can enforce forever.*

*A good data model is invisible when it works and catastrophic when it doesn't. Get the relationships right and your application glides; get them wrong and you will fight your own schema for years. This is the cartographer's craft.*

## 📖 The Legend Behind This Quest

*The entity-relationship model was conjured in 1976 by the scholar Peter Chen, who realized that almost any domain can be described with just three primitives: **entities** (the things), **attributes** (their properties), and **relationships** (how they connect). With those three runes you can map a library, a hospital, an empire's tax records - anything. ER diagrams became the blueprint that every relational schema is built from.*

*This quest hands you Chen's runes and teaches you to wield them, then to translate the resulting diagram into real `CREATE TABLE` statements.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Entity-Relationship Modeling** - Identify entities, attributes, and relationships from requirements
- [ ] **Cardinality** - Model one-to-one, one-to-many, and many-to-many relationships correctly
- [ ] **Normalization (1NF-3NF)** - Eliminate redundancy and update anomalies
- [ ] **Schema Translation** - Convert an ER diagram into a working relational schema

### Secondary Objectives (Bonus Achievements)
- [ ] **Junction Tables** - Resolve many-to-many relationships into linking tables
- [ ] **Surrogate vs Natural Keys** - Choose the right primary key strategy
- [ ] **Denormalization Trade-offs** - Know when breaking a rule is justified

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Sketch an ER diagram for a domain you have never modeled before
- [ ] Decide whether a relationship needs a foreign key or a junction table
- [ ] Justify why a schema is in 3NF
- [ ] Explain one situation where deliberate denormalization is the right call

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Understanding of tables, rows, columns, and keys
- [ ] Familiarity with primary and foreign keys
- [ ] Completion of [Database Fundamentals](/quests/0110/database-fundamentals/) (recommended)

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] PostgreSQL 14+ installed, or Docker to run it
- [ ] A text editor or IDE, and optionally a diagramming tool

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can read and write basic SQL `CREATE TABLE`
- [ ] You are ready to think structurally about a problem domain
- [ ] Ready for 75-90 minutes of focused, hands-on learning

## 🌍 Choose Your Adventure Platform

*You will draw diagrams and then build the schema in PostgreSQL. Pick how you run the database; the diagramming can happen on paper, a whiteboard, or a free online tool.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
brew install postgresql@16
brew services start postgresql@16
createdb modeling_realm
psql modeling_realm
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
winget install PostgreSQL.PostgreSQL.16
createdb modeling_realm
psql modeling_realm
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y postgresql
sudo systemctl enable --now postgresql
sudo -u postgres createdb modeling_realm
sudo -u postgres psql modeling_realm
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
docker run --name modeling -e POSTGRES_PASSWORD=quest -p 5432:5432 -d postgres:16
docker exec -it modeling psql -U postgres
```

For diagrams, use a browser tool such as dbdiagram.io or draw.io - no install required.

</details>

## 🧙‍♂️ Chapter 1: Entities, Attributes, and Relationships

*The first act of modeling is reading requirements and naming the **nouns**. Most nouns become entities; their properties become attributes; the verbs connecting them become relationships.*

### ⚔️ Skills You'll Forge in This Chapter
- Extracting entities and attributes from prose
- Distinguishing an entity from an attribute
- Naming relationships and their direction

### 🏗️ Reading the Requirements

Requirement: *"A university tracks students and courses. Each student can enrol in many courses, and each course can hold many students. Every course is taught in one department."*

```text
Entities:   Student, Course, Department
Attributes: Student(student_id, name, email)
            Course(course_id, title, credits)
            Department(dept_id, name)
Relationships:
            Student  --< enrols in >--  Course      (many-to-many)
            Course   --> belongs to -->  Department  (many-to-one)
```

A handy test: if a "thing" has its own attributes and identity, it is an entity (Course has a title and credits). If it only describes another thing, it is an attribute (a student's email describes the student).

### 🔍 Knowledge Check: Entities
- [ ] Why is `Department` an entity rather than an attribute of `Course`?
- [ ] What attributes would you give a `Student` entity?
- [ ] What verb names the Student-Course relationship?

### ⚡ Quick Wins and Checkpoints
- [ ] **Entities named**: You listed at least three entities for the domain
- [ ] **Relationships named**: You identified the direction of each relationship

## 🧙‍♂️ Chapter 2: Cardinality - One, Many, and Many-to-Many

*Cardinality describes **how many** of one entity relate to another. Get it wrong and your schema either loses data or drowns in duplication.*

### ⚔️ Skills You'll Forge in This Chapter
- One-to-one, one-to-many, and many-to-many relationships
- Where the foreign key goes for each type
- Resolving many-to-many with a junction table

### 🏗️ The Three Cardinalities

```text
One-to-One   (1:1):  A Person has one Passport.
                     -> foreign key on either side, often the optional side.

One-to-Many  (1:N):  A Department has many Courses.
                     -> foreign key on the "many" side (Course.dept_id).

Many-to-Many (M:N):  A Student enrols in many Courses;
                     a Course holds many Students.
                     -> needs a JUNCTION TABLE (enrolments).
```

The many-to-many case is where beginners stumble. You cannot put a list of students in a course row. Instead you create a third table whose rows each represent one pairing:

```sql
CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    name    TEXT NOT NULL UNIQUE
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    title     TEXT NOT NULL,
    credits   INTEGER NOT NULL CHECK (credits > 0),
    dept_id   INTEGER NOT NULL REFERENCES departments(dept_id)  -- 1:N
);

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    email      TEXT UNIQUE
);

-- Junction table resolves the M:N relationship between students and courses.
CREATE TABLE enrolments (
    student_id INTEGER NOT NULL REFERENCES students(student_id),
    course_id  INTEGER NOT NULL REFERENCES courses(course_id),
    enrolled_on DATE NOT NULL DEFAULT CURRENT_DATE,
    grade      TEXT,
    PRIMARY KEY (student_id, course_id)   -- composite key: one row per pairing
);
```

The composite primary key `(student_id, course_id)` guarantees a student cannot enrol in the same course twice, and the junction table can carry its own attributes (`grade`, `enrolled_on`).

### 🔍 Knowledge Check: Cardinality
- [ ] On which side of a 1:N relationship does the foreign key live?
- [ ] Why can't a many-to-many relationship be stored with a single foreign key?
- [ ] What does the composite primary key on `enrolments` prevent?

## 🧙‍♂️ Chapter 3: Normalization in Practice

*Normalization formalizes the rule "store each fact once." You met it briefly in Database Fundamentals; here you apply it as a modeling step.*

### ⚔️ Skills You'll Forge in This Chapter
- Driving a model from 1NF to 3NF
- Spotting partial and transitive dependencies
- Knowing when denormalization is a deliberate choice

### 🏗️ Normalizing a Real Schema

A naive single table for enrolments might look like this:

```text
enrolment(student_id, student_email, course_id, course_title,
          dept_id, dept_name, grade)
```

Apply the forms:

- **1NF**: each column atomic - already true here (no comma-separated lists).
- **2NF**: remove columns that depend on only *part* of the composite key. `student_email` depends only on `student_id`, `course_title` only on `course_id`. Move them to `students` and `courses`.
- **3NF**: remove transitive dependencies. `dept_name` depends on `dept_id`, which depends on the course - not on the enrolment. It belongs in `departments`.

The result is exactly the four tables from Chapter 2. Normalization is not academic ceremony - it is what stops a department rename from requiring thousands of row updates and risking inconsistency.

**When to denormalize:** a read-heavy analytics dashboard might deliberately store `dept_name` alongside aggregated counts to avoid repeated JOINs. That is a conscious trade of write-time complexity for read speed - acceptable only when you understand the rule you are breaking.

### 🔍 Knowledge Check: Normalization
- [ ] Which form removes partial dependencies on a composite key?
- [ ] Why does `dept_name` violate 3NF in the flat table?
- [ ] Name one legitimate reason to denormalize.

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Model a Blog
**Objective**: Draw an ER diagram for a blog with Authors, Posts, and Comments.

**Requirements**:
- [ ] Identify all entities and their attributes
- [ ] Mark the cardinality of every relationship
- [ ] Decide where each foreign key goes

**Validation**: Each relationship's foreign key lands on the correct ("many") side.

### 🟡 Intermediate Challenge: Build the University Schema
**Objective**: Implement the students/courses/departments/enrolments schema in PostgreSQL.

**Requirements**:
- [ ] All four tables created with correct keys and constraints
- [ ] The junction table uses a composite primary key
- [ ] Insert data proving a student is enrolled in multiple courses

**Validation**: `SELECT` joining all four tables returns enrolment rows with grades.

### 🔴 Advanced Challenge: Model and Normalize a Store
**Objective**: Model an e-commerce store (customers, products, orders, order_items) and prove it is in 3NF.

**Requirements**:
- [ ] Resolve the order-to-product many-to-many with an `order_items` junction
- [ ] Store the price per line item (it can change over time)
- [ ] Document why each table satisfies 3NF

**Validation**: No fact is stored twice; an order can contain many products and a product can appear in many orders.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Cartographer of Data** - You mapped an entire domain with an ER diagram
- 🛡️ **Architect of the Schema** - You translated that map into normalized tables

**🛠️ Skills Unlocked**:
- **Entity-Relationship Modeling** - Convert requirements into rigorous structure
- **Normalization Through 3NF** - Build schemas free of update anomalies

**🔓 Unlocked Quests**:
- SQL Mastery - Query the relationships you just designed
- Query Optimization - Index the keys that make JOINs fast

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [SQL Mastery](/quests/0110/sql-mastery/) - JOIN across the tables you modeled

**Explore Side Adventures**:
- ⚔️ [Query Optimization](/quests/0110/query-optimization/) - Tune queries over your schema
- ⚔️ [Database Migrations](/quests/0110/database-migrations/) - Evolve the schema safely

### Character Class Recommendations

**💻 Software Developer**: Continue to [SQL Mastery](/quests/0110/sql-mastery/)  
**🏗️ System Engineer**: Explore [Database Migrations](/quests/0110/database-migrations/)  
**📊 Data Scientist**: Advance to [Query Optimization](/quests/0110/query-optimization/)

## 📚 Resources

### Official Documentation
- [PostgreSQL Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) - Keys, checks, and uniqueness
- [PostgreSQL Foreign Keys](https://www.postgresql.org/docs/current/tutorial-fk.html) - Referential integrity in practice
- [PostgreSQL Data Definition](https://www.postgresql.org/docs/current/ddl.html) - Organizing larger models

### Community Resources
- [dbdiagram.io](https://dbdiagram.io/) - Free browser-based ER diagramming
- [Chen's 1976 ER Model Paper](https://dl.acm.org/doi/10.1145/320434.320440) - The original entity-relationship scroll
- [Stack Overflow: database-design tag](https://stackoverflow.com/questions/tagged/database-design) - Modeling questions answered

### Learning Materials
- [Wikipedia: Entity-Relationship Model](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model) - Notation and concepts
- [Wikipedia: Database Normalization](https://en.wikipedia.org/wiki/Database_normalization) - The normal forms in depth

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Drew an ER diagram and implemented it as a schema
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 0110 - Database Mastery]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Prerequisites:** [[Database Fundamentals: The Relational Model and ACID]] **Unlocks:** [[SQL Mastery: Query Language Proficiency for Data Professionals]] · [[Query Optimization: Performance Tuning for Fast Database Queries]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
</content>
