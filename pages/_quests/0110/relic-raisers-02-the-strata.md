---
title: 'The Strata: Read the Copybook, Then Let the Data Testify'
description: 'Decode a COBOL copybook into a data dictionary, profile the fixed-width file field by field until the two tells surface, and date every layer of the relic''s history — with a familiar drafting and the data confirming.'
excerpt: Turn PIC clauses into a data dictionary, profile the relic's file until its tells surface, and date its strata — the familiar drafts, the data confirms.
date: '2026-09-14T00:00:00.000Z'
lastmod: '2026-09-14T00:00:00.000Z'
level: '0110'
difficulty: '🟡 Medium'
estimated_time: 2-3 hours
primary_technology: python
quest_type: main_quest
quest_series: The Relic Raisers
quest_line: The Relic Raisers
quest_arc: 'The Strata'
skill_focus: data-engineering
learning_style: hands-on
author: IT-Journey Team
permalink: /quests/0110/relic-raisers-02-the-strata/
fmContentType: quest
layout: quest
draft: false
comments: true
mermaid: true
categories:
- Quests
- Legacy Systems
- Data Engineering
tags:
- '0110'
- python
- main_quest
- legacy-systems
- data-dictionary
- fixed-width
- hands-on
- gamified-learning
keywords:
  primary:
  - '0110'
  - data-dictionary
  - legacy-systems
  secondary:
  - copybook
  - fixed-width-files
  - data-profiling
  - ai-assisted-development
  - gamified-learning
prerequisites:
  knowledge_requirements:
  - Chapter I complete — the relic compiles and runs in your relic-raisers folder
  - Python 3 basics (slicing a string, reading a file)
  system_requirements:
  - The relic-raisers folder from Chapter I with INVREC.CPY, ARAGE01.cob, INVOICES.DAT, and AGING.RPT
  - Python 3.10+ and an AI familiar
quest_dependencies:
  required_quests: []
  recommended_quests:
  - /quests/0011/relic-raisers-01-the-dig-site/
  unlocks_quests:
  - /quests/1111/relic-raisers-03-the-elders/
rewards:
  badges:
  - 📜 Copybook Reader — decoded every field and dated every stratum
  skills_unlocked:
  - 🧮 Reading PIC clauses into byte offsets and implied decimals
  - 🔬 Profiling data to confirm or deny a dictionary
  progression_points: 75
  unlocks_features:
  - Continue The Relic Raisers campaign
validation_criteria:
  completion_requirements:
  - DATA_DICTIONARY.md has one row per field with offset, length, type, meaning, and evidence
  - The profiler runs against INVOICES.DAT and both tells are recorded
  - STRATA.md dates the three layers of the relic from its own comments
  skill_demonstrations:
  - Can compute a field's byte offset from the copybook by hand
  - Can explain why REDEFINES adds no bytes
  knowledge_checks:
  - Explains why '000125000' means 1,250.00 and cites the report line that proves it
environment:
  os:
  - linux
  - macos
  - windows
  - cloud
  shell:
  - bash
  - zsh
  - powershell
---
*The relic has a data dictionary already. It is called the copybook, and it was written for the machine: six bytes here, nine digits there, a decimal point that exists only in the program's mind. Your job in this chapter is to write the one for humans — and to refuse every meaning in it that the data has not confirmed. The Archives keep records; the Librarian decides what they mean.*

*The real-world skill: decoding a fixed-width record layout into a data dictionary, and using the data itself — not a familiar's confidence — to validate it.*

## 📖 The Legend Behind This Quest

*A relic's data outlives its documentation by decades. The copybook survives because the program will not compile without it; the meaning of each field survives only in heads, and heads retire. Two things always show through when you profile a relic's data: dates written with two-digit years that straddle a century, and codes in a status column that no scroll explains. The guild calls them the tells, and the discipline of this chapter is to make a familiar draft the dictionary fast, then let the data testify before a single meaning is believed.*

## 🎯 Quest Objectives

### Primary Objectives

- [ ] **Decode the copybook by hand** — compute every field's offset and length from its `PIC` clause, and explain the implied decimal
- [ ] **Profile the data by script** — parse the copybook programmatically and report distinct values, ranges, and the two tells for every field
- [ ] **Draft the dictionary with a familiar** — then reject every meaning that does not cite the copybook, the code, or the profile
- [ ] **Date the strata** — build a table of the relic's layers from its header comments and its Chronicle

### Mastery Indicators

- [ ] You can say, without running anything, which byte `INV-STATUS` starts at and why
- [ ] You can show that `000125000` and the report's `1250.00` are the same number and where the point went
- [ ] Your dictionary marks the difference between a meaning you read and a meaning you inferred

## 🗺️ Quest Prerequisites

- **Chapter I complete** — you need the relic's files and its report in your `relic-raisers` folder.
- **A little Python** — string slicing (`rec[34:40]`) and reading a file line by line are the only tricks used.
- **Your familiar** — the same `claude -p` spells as before; any assistant will do.

## 🧙‍♂️ Chapter 1: Reading PIC — the Copybook by Hand

### ⚔️ Skills You'll Forge

- `X` versus `9`, and what `V` means
- `REDEFINES` as two names for the same bytes
- Byte offsets as the map of a record

Lay the copybook's fields end to end. `X(n)` is `n` characters; `9(n)` is `n` digits stored as characters too; `V` marks where a decimal point *would* be and costs nothing on disk; `REDEFINES` gives the same bytes a second set of names and advances nothing. Walk it once with a pencil:

| Field | PIC | Offset | Length | Notes |
|---|---|---|---|---|
| `INV-CUST-ID` | `X(6)` | 0 | 6 | text |
| `INV-CUST-NAME` | `X(20)` | 6 | 20 | text, space-padded |
| `INV-NUMBER` | `X(8)` | 26 | 8 | text |
| `INV-DUE-DATE` | `9(6)` | 34 | 6 | `YYMMDD` — two-digit year |
| `INV-DUE-YY` / `INV-DUE-MMDD` | `99` / `9(4)` | 34 / 36 | 2 / 4 | `REDEFINES` the six bytes above; adds no bytes |
| `INV-AMOUNT` | `9(7)V99` | 40 | 9 | nine digits, point implied two from the right |
| `INV-STATUS` | `X` | 49 | 1 | one code, undocumented |
| `FILLER` | `X(30)` | 50 | 30 | reserved; the comment says the layout is shared |

Prove the implied decimal with the report from Chapter I: `INV10001` carries `000125000` in the data and the relic printed `1250.00`. Nine digits, the point inserted before the last two, leading zeros dropped by the edit picture `Z(7)9.99`. Nothing in the file says "1,250" — only the program knows, and now so do you.

### 🔍 Knowledge Check

- [ ] What byte does `INV-STATUS` occupy, and how did you get there?
- [ ] If a future program wrote a real decimal point into `INV-AMOUNT`, what would the relic read?
- [ ] Why does the `REDEFINES` row add nothing to the running offset?

## 🧙‍♂️ Chapter 2: Let the Data Testify — the Profiler

### ⚔️ Skills You'll Forge

- Parsing `PIC` clauses programmatically
- Profiling fixed-width data field by field
- Recognizing the two tells

A pencil scales to one copybook. A script scales to the Empire's. Save this as `profile_relic.py`; it parses the copybook's `PIC` clauses into offsets, then walks the data file and reports what each field actually contains — including the two tells that every relic hides.

```python
#!/usr/bin/env python3
"""profile_relic.py — read a copybook, then let the DATA testify.

Parses the PIC clauses in a COBOL copybook into (name, offset, length, kind),
then profiles every field across a fixed-width data file: distinct values,
min/max, and the two relic tells — two-digit years on both sides of a pivot,
and status codes nobody documented. Usage: profile_relic.py COPYBOOK DATAFILE
"""
import re
import sys
from collections import Counter

PIC_RE = re.compile(r"^\s*(\d\d)\s+([\w-]+)\s+(?:(REDEFINES)\s+[\w-]+\s+)?PIC\s+([X9SV()\d]+)\.", re.I)
REDEF_RE = re.compile(r"^\s*(\d\d)\s+([\w-]+)\s+REDEFINES\s+([\w-]+)\.", re.I)

def pic_length(pic):
    """X(6) -> 6, 9(7)V99 -> 9 (V is an implied point: no bytes)."""
    total = 0
    for sym, rep in re.findall(r"([X9])(?:\((\d+)\))?", pic.upper()):
        total += int(rep) if rep else 1
    return total

def parse_copybook(path):
    fields, offset, in_redefines, redef_level = [], 0, False, None
    for line in open(path):
        if len(line) > 6 and line[6] == "*":
            continue  # a comment line: column 7 holds the asterisk
        body = line[7:72] if len(line) > 7 else ""
        m = REDEF_RE.match(body)
        if m:
            in_redefines, redef_level = True, int(m.group(1))
            continue
        m = PIC_RE.match(body)
        if not m:
            continue
        level, name, _, pic = int(m.group(1)), m.group(2), m.group(3), m.group(4)
        length = pic_length(pic)
        if in_redefines and level > redef_level:
            continue  # sub-fields of a REDEFINES share bytes already counted
        in_redefines = False
        kind = "numeric" if pic.upper().lstrip("S").startswith("9") else "text"
        fields.append((name, offset, length, kind))
        offset += length
    return fields, offset

def main(copybook, datafile):
    fields, reclen = parse_copybook(copybook)
    records = [l.rstrip("\n").ljust(reclen) for l in open(datafile)]
    print(f"{copybook}: {len(fields)} fields, record length {reclen}; {datafile}: {len(records)} records\n")
    print(f"{'FIELD':<16}{'OFF':>4}{'LEN':>4}  {'KIND':<8}{'DISTINCT':>9}  MIN .. MAX")
    for name, off, ln, kind in fields:
        values = [r[off:off + ln] for r in records]
        distinct = Counter(values)
        lo, hi = min(values), max(values)
        print(f"{name:<16}{off:>4}{ln:>4}  {kind:<8}{len(distinct):>9}  {lo!r} .. {hi!r}")
        if name.endswith("-DATE") and ln == 6:
            years = sorted({v[:2] for v in values})
            print(f"{'':16}  two-digit years present: {years} — which century is each? (look for a pivot in the code)")
        if name.endswith("-STATUS"):
            print(f"{'':16}  status distribution: {dict(distinct)} — every code needs a documented meaning")

if __name__ == "__main__":
    main(*sys.argv[1:3])
```

Cast it on the relic's files:

```bash
python3 profile_relic.py INVREC.CPY INVOICES.DAT
```

```text
INVREC.CPY: 7 fields, record length 80; INVOICES.DAT: 8 records

FIELD            OFF LEN  KIND     DISTINCT  MIN .. MAX
INV-CUST-ID        0   6  text            4  'C00101' .. 'C00412'
INV-CUST-NAME      6  20  text            4  'ACME FASTENERS      ' .. 'PLATTE VALLEY DIST  '
INV-NUMBER        26   8  text            8  'INV10001' .. 'INV10008'
INV-DUE-DATE      34   6  numeric         8  '260401' .. '991231'
                  two-digit years present: ['26', '99'] — which century is each? (look for a pivot in the code)
INV-AMOUNT        40   9  numeric         7  '000125000' .. '000980000'
INV-STATUS        49   1  text            2  '7' .. 'O'
                  status distribution: {'O': 7, '7': 1} — every code needs a documented meaning
FILLER            50  30  text            1  '                              ' .. '                              '
```

The script's offsets match your pencil's, which is the first thing to check whenever a tool reads a copybook for you. Then the tells. The date column holds years `26` and `99`, and only the program's pivot can say whether `99` is 1999 or 2099 — you saw in Chapter I that it chose 1999, and Chapter V will show what happens when a port forgets. The status column holds `O` and `7`, and no scroll in the folder says what either means; the header comment says what `7` does, not what it *is*. On a real relic you will see a dozen codes and a comment for two of them. Write every code down; the ones without a meaning are questions for the Elders.

### 🔍 Knowledge Check

- [ ] The profiler reports `INV-DUE-DATE` as numeric with eight distinct values. Which of those values would a port sort wrongly if it treated `YY` as a plain number?
- [ ] Why does the script skip the `INV-DUE-YY` and `INV-DUE-MMDD` lines when computing offsets?
- [ ] What would a `FILLER` field with more than one distinct value tell you about the "reserved" bytes?

## 🧙‍♂️ Chapter 3: The Dictionary — a Familiar Drafts, the Evidence Decides

### ⚔️ Skills You'll Forge

- Prompting for a dictionary that separates read meanings from inferred ones
- Auditing every row against evidence

Save the profile to a file and hand the familiar everything it is allowed to know: the copybook, the program, and the data's testimony. The spell tells it what a row must contain and what to do when it does not know.

```bash
python3 profile_relic.py INVREC.CPY INVOICES.DAT > profile.txt
cat INVREC.CPY ARAGE01.cob profile.txt | claude -p "Draft a data dictionary as a Markdown table with one row per field of INV-RECORD: FIELD, OFFSET, LENGTH, TYPE, MEANING, EVIDENCE. Under EVIDENCE cite the copybook line, the program paragraph, or the profile line that supports the MEANING. If you are inferring a meaning rather than reading it, prefix it with HYPOTHESIS. Do not invent meanings for values no source explains." > DATA_DICTIONARY.md
```

Print mode answers on standard output, so the redirect is what puts the draft on disk. Open the file and audit it. Every row must survive three questions: does the offset match the profiler, does the evidence exist where the row says, and is the meaning read or guessed? The dictionary that survives the audit looks like this — notice the two rows that are honest about what nobody knows:

| Field | Offset | Length | Type | Meaning | Evidence |
|---|---|---|---|---|---|
| `INV-CUST-ID` | 0 | 6 | text | Customer key, `C` + five digits | profile: 4 distinct, `C00101`..`C00412` |
| `INV-CUST-NAME` | 6 | 20 | text | Customer name, space-padded | copybook `PIC X(20)`; report column NAME |
| `INV-NUMBER` | 26 | 8 | text | Invoice key, unique per record | profile: 8 distinct in 8 records |
| `INV-DUE-DATE` | 34 | 6 | numeric | Due date `YYMMDD`; `YY` < 50 is 20YY, else 19YY | `PROCESS-RECORD` pivot; `INV10006` prints `1999/12/31` |
| `INV-AMOUNT` | 40 | 9 | numeric | Open amount, two implied decimals | `PIC 9(7)V99`; `000125000` prints `1250.00` |
| `INV-STATUS` | 49 | 1 | text | `7` = excluded from aging, reported as DISPUTED; `O` = HYPOTHESIS "open" — no source defines it | `MOD 06/06` comment; `EVALUATE` first `WHEN`; profile `{'O': 7, '7': 1}` |
| `FILLER` | 50 | 30 | text | Reserved; HYPOTHESIS used by `ARINV05`/`ARSTM02` | copybook header comment; profile: all spaces |

The row for `O` is the important one. Seven of eight records carry it, the program never mentions it, and a familiar will cheerfully call it "open". That is a Plausible Ghost in miniature: probably right, entirely unproven, and the word HYPOTHESIS is what keeps it from being built into a port as fact.

### 🔍 Knowledge Check

- [ ] Which row's meaning is read from code, and which is inferred from data? Name one of each.
- [ ] What would you need to see to remove the HYPOTHESIS mark from the `O` status?
- [ ] Why hand the familiar the profile at all, rather than only the copybook?

## 🧙‍♂️ Chapter 4: Date the Strata

### ⚔️ Skills You'll Forge

- Reading a relic's history from its comments
- Consulting the Chronicle for the layers the comments forgot

Dig anywhere in a relic and you hit a decade. `ARAGE01` announces its own strata in the header; write them down as a table in `STRATA.md`, oldest at the bottom the way a dig is drawn:

| Layer | Date | Change | Who | Where in the code |
|---|---|---|---|---|
| 3 | 06/2006 | Status `7` excluded from aging, reported separately | "J.R./ACCTG" | `EVALUATE`, first `WHEN`; `WS-TOT-DISPUTED` |
| 2 | 11/1999 | Y2K window added, pivot 50 | unnamed | `READ-PARM`, `PROCESS-RECORD` |
| 1 | 03/1997 | Written; converted from RPG II | "D.M." | the whole program |

On a real relic the comments lie by omission and the Chronicle fills the gaps. These three spells read the Chronicle of any file that has one; run them on your own repository and on the next relic you meet:

```bash
git log --oneline --follow -- ARAGE01.cob        # every entry that touched the file
git log -S'STATUS 7' --oneline -- ARAGE01.cob     # entries that added or removed a phrase (the pickaxe)
git blame -L '/EVALUATE TRUE/,+14' ARAGE01.cob    # whose hand inscribed the bucket logic, and when
```

Your lab relic's Chronicle has a single entry — "as found" — because you began it in Chapter I. That is itself a fact worth recording: a system whose history starts on the day you arrived has strata you can only recover from comments and people. Before you commit, add the two tells to the Unknowns list in `EXPEDITION.md` — what `O` means, and whether any due date before 1950 ever existed — so the interview guide for Chapter III is complete. Then commit the dictionary, the strata table, and the notes.

```bash
git add profile_relic.py profile.txt DATA_DICTIONARY.md STRATA.md EXPEDITION.md
git commit -q -m "strata: data dictionary with evidence, profiler, dated layers"
```

## 🎮 Mastery Challenge

**Objective:** a dictionary the port in Chapter V can be written from, and a strata map the Elders in Chapter III can correct.

- [ ] `profile_relic.py` runs clean and its offsets match your hand-computed table
- [ ] `DATA_DICTIONARY.md` has seven rows; every MEANING has an EVIDENCE cell, and every inferred meaning says HYPOTHESIS
- [ ] `STRATA.md` dates all three layers and names the code each one lives in
- [ ] Both tells — the century straddle and the undocumented `O` — are written down as questions in `EXPEDITION.md`

## 🎁 Rewards & Progression

- 📜 **Copybook Reader** — you decoded every field and dated every stratum
- 🧮 **Skill unlocked:** reading `PIC` clauses into byte offsets and implied decimals
- 🔬 **Skill unlocked:** profiling data to confirm or deny a dictionary
- **+75 XP**

## 🔁 Reproduce It

The profiler and its output above were run on 2026-09-14 against the exact `INVREC.CPY` and `INVOICES.DAT` from Chapter I, on Python 3.11 (any 3.10+ works; stock Ubuntu 24.04 ships 3.12). The dictionary table is the audited result of that run plus the relic's own comments; the only two meanings marked HYPOTHESIS are the two that no source in the folder defines.

## 🗺️ Quest Network

```mermaid
graph LR
  A["Ch. I — The Dig Site"] --> B["Ch. II — The Strata"]
  B --> C["Ch. III — The Elders"]
  click A "/quests/0011/relic-raisers-01-the-dig-site/"
  click C "/quests/1111/relic-raisers-03-the-elders/"
  classDef current fill:#1f6feb,stroke:#0b3d91,color:#fff;
  class B current;
```

*Chapters sit at different levels by design: the campaign runs through the levels, and each chapter also appears on its own level hub.*

## 🔮 Next Adventures

The data has said everything it can. Two meanings are still marked HYPOTHESIS, and a comment names a person. Next you find the Elders and recover the reasons before they retire.

- ➡️ **Next chapter:** [Chapter III — The Elders](/quests/1111/relic-raisers-03-the-elders/)
- 🏺 **Campaign hub:** [Epic Quest: The Relic Raisers](/quests/codex/relic-raisers/)
- 📚 **Deeper in the Archives:** [Data Modeling](/quests/0110/data-modeling/)

## 📚 Resource Codex

- [GnuCOBOL Programmer's Guide](https://gnucobol.sourceforge.io/doc/gnucobol.html) — `PICTURE` symbols, `REDEFINES`, and `COMP-3` explained by the compiler's own manual
- [Python `re` module](https://docs.python.org/3/library/re.html) — the runecraft the profiler uses to read `PIC` clauses
- [Python `collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter) — the one-liner behind the status distribution

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Campaign hub:** [[Epic Quest: The Relic Raisers]] **Level hub:** [[Level 0110 (6) - Database Mastery]] **Previous:** [[The Dig Site: Unearth the Relic and Name What You Do Not Know]] **Next:** [[The Elders: Recover the Reasons Before They Retire]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
