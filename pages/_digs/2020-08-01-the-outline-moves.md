---
title: The outline moves, the paths do not
description: Six early-August commits rename the setup files into hello folders, while the outline still names paths those commits had just left.
date: '2026-09-26T22:42:19.000Z'
lastmod: '2026-09-26T22:49:00.000Z'
author: bamr87
categories:
- digs
tags:
- git
- history
- archaeology
keywords:
- git history
- file moves
- it-journey
excerpt: The repository spends two weeks rearranging its first tools, and the map does not keep up with the move.
permalink: /digs/2020-08-01-the-outline-moves/
repository: bamr87/it-journey
range_start: 2020-08-01
range_end: 2020-08-17
start_sha: 00dd4b5b4104cfa4f9354e3926672e8e342f41a5
end_sha: 7220aefde9b07375a7b64273b4b79f8a2112633b
commit_count: 6
voice_profile: git-dig
draft: false
---
A repository that has promised a journey now spends sixteen days moving the luggage. The subjects get vaguer as the tree gets more organized. `Update`. `test`. `commit`. `Clean up`. If the history were a diary, these would be the days it forgot to say what happened, and then carefully recorded the furniture.

## Scope

This dig examines six commits in `bamr87/it-journey` from 2020-08-01 through 2020-08-17, in one parent chain after the first dig. It does not include the August 23 fork, pull requests, issues, or any record that a script ran. The evidence index is `docs/git-archaeology/001-the-outline-moves/evidence.json` in this repository.

## Facts

`added onedrive and alfred to hb packages` modifies `init_apps/hb-packages.sh` and adds two `brew cask install` lines, for OneDrive and Alfred. It also adds `.DS_Store`. The committer is amr abdel-motaleb. [git-commit:00dd4b5b4104cfa4f9354e3926672e8e342f41a5](https://github.com/bamr87/it-journey/commit/00dd4b5b4104cfa4f9354e3926672e8e342f41a5)

Nine days later, `Update` deletes `zer0_dev.md` and `init_apps/hb-apps.md`, adds `init_it.md`, and moves several scripts from `init_apps/` to `init_world/`. Git records three of those moves as renames. The new outline still begins `# zer0` and still points at `./init_apps/hb-packages.sh` and `./init_apps/apm-apps.sh`. It also names Level 00 through Level 02, including the heading `Level 02 - PIjects`. [git-commit:ae59de3c5efeaccca16f8d9dc6f06e60a47aa4d8](https://github.com/bamr87/it-journey/commit/ae59de3c5efeaccca16f8d9dc6f06e60a47aa4d8)

`test` adds three files under `init_world/hello-gcp/` and modifies the package script, a startup script, and `shebang.sh`. The subject does not name a test file, and this sample contains no test result. [git-commit:a947e6b98f9f0cbb22f18544d1f305b3b78f51f9](https://github.com/bamr87/it-journey/commit/a947e6b98f9f0cbb22f18544d1f305b3b78f51f9)

`commit`, four days later, nests scripts into `hello-bash`, `hello-gcp`, and `hello-mac`. Several of those moves are recorded as renames. It also adds `iterminate2.sh` and `vm.yaml`, and edits `init_it.md`. After that edit the outline still contains `./init_apps/hb-packages.sh` and `./init_apps/apm-apps.sh`, beside a path under `init_world/hello-mac/`. [git-commit:9cc38248d83975bcdd01ab3fa749b07ec66fb52c](https://github.com/bamr87/it-journey/commit/9cc38248d83975bcdd01ab3fa749b07ec66fb52c)

Four minutes later, `Clean up` modifies only `init_world/hello-mac/iterminate2.sh`. [git-commit:0ef2f16839b8ff1421ba3980363da97d9859e09f](https://github.com/bamr87/it-journey/commit/0ef2f16839b8ff1421ba3980363da97d9859e09f)

`Hello win` is the first commit in this sample whose author and committer are Bamrman. It adds `init_world/hello-gcp/win-sdk.bat`, `init_world/hello-mac/hello-mac.sh`, and `init_world/hello-win/hello-win.md`. The Windows arrival is a Markdown note plus a batch file. This page does not repeat their install commands. [git-commit:7220aefde9b07375a7b64273b4b79f8a2112633b](https://github.com/bamr87/it-journey/commit/7220aefde9b07375a7b64273b4b79f8a2112633b)

## Inferences

The rename into `hello-*` folders looks like an attempt to sort the first tools by platform. That reading rests on the paths, not on a stated plan. The outline's leftover `init_apps` paths suggest the map was copied forward faster than it was corrected. The objects do not say whether anyone followed those paths and found them missing.

`test` and `commit` are subjects with almost no claim. The diffs are doing the talking. That is a habit, not a motive.

## Limits

This sample cannot say the packages were installed, the cleanup improved anything, or Windows was set up. It cannot explain the gap from August 1 to August 10. The next commits fork from `Clean up`'s parent, not from a single line, and they are a different dig. The open question is whether a journey is the outline, or the files the outline can no longer find.

## Retrospective

This is hindsight, written now. It is not a motive recovered from the subjects.

I wish the outline had been edited in the same commit that moved the files. Leaving `./init_apps/hb-packages.sh` in `init_it.md` after the rename is a map that sends the next reader to a door the same commit removed. The cheaper habit is: move the file, then fail the commit if the outline still names the old path. [git-commit:ae59de3c5efeaccca16f8d9dc6f06e60a47aa4d8](https://github.com/bamr87/it-journey/commit/ae59de3c5efeaccca16f8d9dc6f06e60a47aa4d8)

I wish `.DS_Store` had never entered the tree. A ignore rule on the first day would have saved every later reader from treating desktop debris as project content. [git-commit:00dd4b5b4104cfa4f9354e3926672e8e342f41a5](https://github.com/bamr87/it-journey/commit/00dd4b5b4104cfa4f9354e3926672e8e342f41a5)

I wish `test` and `commit` had been illegal subjects. A subject that names the path and the verb would have saved the time this page spent asking the diff what the author already knew. [git-commit:a947e6b98f9f0cbb22f18544d1f305b3b78f51f9](https://github.com/bamr87/it-journey/commit/a947e6b98f9f0cbb22f18544d1f305b3b78f51f9)
