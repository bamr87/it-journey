---
title: "The repository's first six commits"
description: "What the 2020-07-30 root and the next day's install notes actually contain, with the commit subjects kept separate from the diffs."
date: 2026-09-26T21:21:40.000Z
lastmod: 2026-09-26T22:49:00.000Z
author: bamr87
categories:
  - digs
tags:
  - git
  - history
  - archaeology
keywords:
  - git history
  - initial commit
  - it-journey
excerpt: "A first dig through the repository's own beginning: one sentence, a workflow that only echoes, and a move that took two commits."
permalink: /digs/2020-07-30-first-steps/
repository: bamr87/it-journey
range_start: 2020-07-30
range_end: 2020-07-31
start_sha: ab523954f523ddaf7402682c79630b36958fad79
end_sha: ff6981adbf3ef217818bac23c65110be3306c7ea
commit_count: 6
voice_profile: git-dig
draft: false
---

A journey from zero to hero announces itself, and the first tool it adds is a workflow that says hello. That is a grand sentence with a very small echo. The interesting question is not whether the echo was ambitious. It is what a beginning is allowed to be before it has done anything.

## Scope

This dig examines six commits in `bamr87/it-journey`, from the 2020-07-30 root through the last commit on 2020-07-31. It does not collect pull requests, issues, workflow runs, or anything after that day. The evidence index is `docs/git-archaeology/000-first-steps/evidence.json` in this repository. It is not a site page.

## Facts

The root commit has no parent. Its only file is `README.md`, and the text is `# it-journey` plus `From zero to hero collection of docs, tools, scripts, and information to support your IT journey`. The committer is GitHub. [git-commit:ab523954f523ddaf7402682c79630b36958fad79](https://github.com/bamr87/it-journey/commit/ab523954f523ddaf7402682c79630b36958fad79)

Four minutes later the subject says `Create blank.yml`. The path is `.github/workflows/blank.yml`. The workflow is named CI, watches `master`, and runs echo commands. The committer is GitHub. A workflow file is not a recorded run. [git-commit:4fda32c0153182b7ec6f30873a21c5c4812c709a](https://github.com/bamr87/it-journey/commit/4fda32c0153182b7ec6f30873a21c5c4812c709a)

The next afternoon is the first commit in the sample whose committer is not GitHub. It adds two root scripts: one calls the Homebrew installer, and the other names Atom, Chrome, and Firefox. [git-commit:41fb5848e494d45fa05695240994c652bbbdacdc](https://github.com/bamr87/it-journey/commit/41fb5848e494d45fa05695240994c652bbbdacdc)

`moved files` adds copies under `init_apps/` and leaves the root scripts in place. Five minutes later, `removed files` deletes the originals. Git records additions and deletions, not a rename. [git-commit:db60402958d72ce39d24da3d8b2c15f92f75f2f5](https://github.com/bamr87/it-journey/commit/db60402958d72ce39d24da3d8b2c15f92f75f2f5) [git-commit:e1f8546d6ac60da93fcc8e6c068f869ce09ea20e](https://github.com/bamr87/it-journey/commit/e1f8546d6ac60da93fcc8e6c068f869ce09ea20e)

By 17:32 the tree is seven files. A note opens with `# zer0` while the README still says `zero to hero`. The note names editors, shells, and a section called Full Stack Attack. It also contains a local Windows path and a gist identifier, which this page does not repeat. [git-commit:ff6981adbf3ef217818bac23c65110be3306c7ea](https://github.com/bamr87/it-journey/commit/ff6981adbf3ef217818bac23c65110be3306c7ea)

## Inferences

The first two commits look like GitHub's web interface. That reading rests on the committer name, the subjects, and the starter workflow text. The objects do not record which button was clicked. `moved files` describes an intention the first of those two diffs does not perform. The later public phrase `zer0 to her0` is not established here. Only `zer0` is present, and only in a note.

## Limits

This sample cannot say the workflow ran, that Homebrew was installed, or why the files were rearranged. A second parentless commit, `Create README.md`, is dated 2021-03-13. It is not this beginning. The open question is how long a repository can promise a journey before the history has to show one.

## Retrospective

This is hindsight, written now. The commits do not record that anyone wished it at the time.

I wish the first workflow had failed if the tree was empty of a real check, instead of echoing hello under the name CI. The cheaper move was one command that proved the repository could be read, and a name that did not pretend to be a build. [git-commit:4fda32c0153182b7ec6f30873a21c5c4812c709a](https://github.com/bamr87/it-journey/commit/4fda32c0153182b7ec6f30873a21c5c4812c709a)

I wish the move had been one `git mv`, not a copy and a deletion five minutes apart. Two commits taught the subject line to lie. One rename would have kept the history attached to the file. [git-commit:db60402958d72ce39d24da3d8b2c15f92f75f2f5](https://github.com/bamr87/it-journey/commit/db60402958d72ce39d24da3d8b2c15f92f75f2f5)

I wish the first note had not carried a local path or a gist identifier. A placeholder path would have taught the same setup and left nothing personal in the permanent record. [git-commit:ff6981adbf3ef217818bac23c65110be3306c7ea](https://github.com/bamr87/it-journey/commit/ff6981adbf3ef217818bac23c65110be3306c7ea)
