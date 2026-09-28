---
title: The repository's first six commits
description: What the 2020-07-30 root and the next day's install notes actually contain, with the commit subjects kept separate from the diffs.
date: '2026-09-26T21:01:42.000Z'
lastmod: '2026-09-26T21:01:42.000Z'
author: bamr87
categories:
- notes
tags:
- git
- history
- archaeology
keywords:
- git history
- initial commit
- it-journey
excerpt: 'A first dig through the repository''s own beginning: one sentence, a workflow that only echoes, and a move that took two commits.'
permalink: /notes/git-archaeology/first-steps/
draft: true
---
The repository does not begin as a platform. It begins as two lines in `README.md`, committed on 2020-07-30 at 10:19:45 -0600, with no parent. The file says `# it-journey` and then `From zero to hero collection of docs, tools, scripts, and information to support your IT journey`. The committer is GitHub, not a local Git identity. That is the whole root. [git-commit:ab523954f523ddaf7402682c79630b36958fad79](https://github.com/bamr87/it-journey/commit/ab523954f523ddaf7402682c79630b36958fad79)

Four minutes later the history adds a file the subject line calls `blank.yml`. The path is `.github/workflows/blank.yml`. The workflow is named CI, watches `master`, checks out the tree, and echoes hello. It does not build, test, or deploy anything. A workflow file is not a workflow run; this sample has no evidence that the job ever executed. [git-commit:4fda32c0153182b7ec6f30873a21c5c4812c709a](https://github.com/bamr87/it-journey/commit/4fda32c0153182b7ec6f30873a21c5c4812c709a)

The next afternoon is the first local commit in the sample. Two scripts land at the repository root: one calls the Homebrew installer, and the other names Atom, Chrome, and Firefox. The subject is accurate about the files. It is not evidence that those programs were installed. [git-commit:41fb5848e494d45fa05695240994c652bbbdacdc](https://github.com/bamr87/it-journey/commit/41fb5848e494d45fa05695240994c652bbbdacdc)

Then the subject line and the diff part company. `moved files` only adds copies under `init_apps/`. The root scripts are still there. Five minutes later, `removed files` deletes the originals. The move is real across the pair of commits, and it is not a Git rename. The message described the intention. The patches did the work in two steps. [git-commit:db60402958d72ce39d24da3d8b2c15f92f75f2f5](https://github.com/bamr87/it-journey/commit/db60402958d72ce39d24da3d8b2c15f92f75f2f5) [git-commit:e1f8546d6ac60da93fcc8e6c068f869ce09ea20e](https://github.com/bamr87/it-journey/commit/e1f8546d6ac60da93fcc8e6c068f869ce09ea20e)

By 17:32 the tree is seven files. A note titled `zer0` appears while the README still says `zero to hero`. The note names editors, shells, and a section called Full Stack Attack. It also contains a local Windows path and a gist identifier, which this note does not repeat. The stylized ending `her0` is not in this sample. Neither is a site, a quest, or a test run. [git-commit:ff6981adbf3ef217818bac23c65110be3306c7ea](https://github.com/bamr87/it-journey/commit/ff6981adbf3ef217818bac23c65110be3306c7ea)

There is a second parentless commit, `Create README.md`, dated 2021-03-13. It is not this beginning. The published copy of this reading is the first dig. This note stays a draft.
