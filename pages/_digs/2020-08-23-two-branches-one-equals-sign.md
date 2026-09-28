---
title: Two branches, one equals sign
description: Five late-August commits fork the history, add a JavaScript assignment, correct it on one side, and merge both stories.
date: '2026-09-26T22:42:19.000Z'
lastmod: '2026-09-26T22:49:00.000Z'
author: bamr87
categories:
- digs
tags:
- git
- history
- javascript
excerpt: The history splits, a condition assigns instead of compares, and the merge has to keep both versions of the mistake.
permalink: /digs/2020-08-23-two-branches-one-equals-sign/
repository: bamr87/it-journey
range_start: 2020-08-23
range_end: 2020-08-25
start_sha: b6d3cf5958e6c639f13b60f47f62af715f3e788d
end_sha: 4304ba962ea09e180c0249eed686587cd547d2a3
commit_count: 5
voice_profile: git-dig
draft: false
---
For a moment the repository has two memories of the same afternoon. One of them says hello to Windows. The other adds a JavaScript file whose condition does not ask whether a value is `"blah"`. It makes the value `"blah"`. Philosophy has spent centuries on the difference between naming a thing and changing it. This history spends two days, and then merges the argument.

## Scope

This dig examines five commits in `bamr87/it-journey` from 2020-08-23 through 2020-08-25. They are not one straight line. `js and stuff` and the already published `Hello win` share a parent. Two merges follow. This page does not collect pull-request reviews, issue comments, or a test run. The evidence index is `docs/git-archaeology/002-two-branches/evidence.json` in this repository.

## Facts

`js and stuff` adds `js_testing.js` and modifies two Mac setup files. In the new file, the loop condition is `itemList1[i] = "blah"`, one equals sign. The parent is `0ef2f16839b8ff1421ba3980363da97d9859e09f`, the same parent as `Hello win`. The committer is amr abdel-motaleb. [git-commit:b6d3cf5958e6c639f13b60f47f62af715f3e788d](https://github.com/bamr87/it-journey/commit/b6d3cf5958e6c639f13b60f47f62af715f3e788d)

Fifty-one seconds later, `Merge branch 'master' of https://github.com/Bamrman/it-journey` joins `Hello win` and `js and stuff`. The author and committer are Bamrman. The merge commit itself has an empty name-status. [git-commit:e5f9d75ed0130be054310daba72a03390fa00b78](https://github.com/bamr87/it-journey/commit/e5f9d75ed0130be054310daba72a03390fa00b78)

`update` does not sit on that merge. Its parent is `js and stuff`. It changes the condition to `itemList1[i] == "blah"` and maps the quantity strings with `.map(`. It also rewrites the `init_it.md` headings from `Level 00` through `Level 02` into binary labels, `Level 0000` through `Level 1111`. The last of those headings is `Level 1111 - Borne Again Solutions Hero`. The heading `Level 0010 - PIjects` keeps the earlier spelling. [git-commit:1cae4d51b37a7a875855dd6acdd6ca5503562e5e](https://github.com/bamr87/it-journey/commit/1cae4d51b37a7a875855dd6acdd6ca5503562e5e)

`comit` sits on the other side, parented by the first merge. It still has `itemList1[i] = "blah"`, and it changes the addition to `valueOf`. It adds an empty `gpc-app.md` and edits `hello-win.md`. The author and committer are Bamrman. [git-commit:244e56725cef6fa4dec242367e882244a700e45d](https://github.com/bamr87/it-journey/commit/244e56725cef6fa4dec242367e882244a700e45d)

`Merge branch 'master' of github.com:Bamrman/it-journey` joins `update` and `comit`. Its only recorded path is `js_testing.js`, with status `MM`. The file stored at that commit contains `itemList1[i] = "blah"` and does not contain the two-equals comparison. It also contains no conflict markers. The committer is amr abdel-motaleb. [git-commit:4304ba962ea09e180c0249eed686587cd547d2a3](https://github.com/bamr87/it-journey/commit/4304ba962ea09e180c0249eed686587cd547d2a3)

## Inferences

The two equals-sign versions are not a before-and-after on one line. They are contemporaries. One branch compares. The other still assigns. The merge tip keeps the assigning form. That is what the stored file shows. It does not show whether a person chose that line or a merge tool did.

The binary level headings appear in the same commit as the comparison fix. That pairing suggests the outline was being renamed toward the later `0000` to `1111` ladder. The commit does not say the ladder was taught, published, or followed. `PIjects` surviving the rename suggests the edit was a relabel, not a proofread. The correction and the ladder both lose the argument at the tip: the comparison is not the version this sample ends on.

## Limits

This sample cannot say the JavaScript was executed, or why the assigning form is the one at the merge tip. It cannot say the empty `gpc-app.md` was a typo for GCP, only that the filename is `gpc-app.md` and the file is empty. The open question is what a history owes a reader when the careful correction and the surviving bug are both true, and only one of them remains.

## Retrospective

This is hindsight, written now. The merge does not say anyone noticed the loss.

I wish the condition had been a comparison on the first commit, and I wish a check had refused an assignment inside `if`. The bug is one character. The time cost is the rest of this dig. [git-commit:b6d3cf5958e6c639f13b60f47f62af715f3e788d](https://github.com/bamr87/it-journey/commit/b6d3cf5958e6c639f13b60f47f62af715f3e788d)

I wish the comparing branch had been the one merged, or the two lines had been rebased onto one parent before either side called itself done. Instead the tip stores the assigning form after a commit had already written `==`. The lesson is not "merges are bad." It is that a correction on a side branch is not a correction until the tip contains it. [git-commit:1cae4d51b37a7a875855dd6acdd6ca5503562e5e](https://github.com/bamr87/it-journey/commit/1cae4d51b37a7a875855dd6acdd6ca5503562e5e) [git-commit:4304ba962ea09e180c0249eed686587cd547d2a3](https://github.com/bamr87/it-journey/commit/4304ba962ea09e180c0249eed686587cd547d2a3)

I wish the empty `gpc-app.md` had not been added under a misspelled name. An empty file teaches nothing and leaves the next reader to guess. Not adding it would have saved that guess. [git-commit:244e56725cef6fa4dec242367e882244a700e45d](https://github.com/bamr87/it-journey/commit/244e56725cef6fa4dec242367e882244a700e45d)
