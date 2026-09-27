# First steps

This installment covers the six commits from the 2020 root through the end of 2020-07-31. The Git objects are the evidence. This report separates what those objects show from what a reader might infer. It does not describe the later repository, and it does not treat the 2021 parentless `Create README.md` commit as the beginning.

## Facts

The history has two parentless commits. The earlier one is `ab523954f523ddaf7402682c79630b36958fad79`, committed 2020-07-30 at 10:19:45 -0600, with the subject `Initial commit`. Its only file is `README.md`, and the text is two lines: `# it-journey` and `From zero to hero collection of docs, tools, scripts, and information to support your IT journey`. The author name is Bamrman. The committer is GitHub.

Three minutes and 52 seconds later, `4fda32c0153182b7ec6f30873a21c5c4812c709a` adds `.github/workflows/blank.yml`. The subject says `Create blank.yml`. The workflow is named CI, listens for push and pull_request events on `master`, checks out the repository with `actions/checkout@v2`, and runs `echo` commands. Its committer is also GitHub.

The next commit is the following afternoon. `41fb5848e494d45fa05695240994c652bbbdacdc` (`adding new mac install files`, 2020-07-31 14:14:27 -0600) is the first commit in this range whose committer is not GitHub. It adds `hb-install.sh` and `hb-packages.sh` at the repository root. The install script calls the Homebrew installer from `raw.githubusercontent.com`. The package script names Atom, Google Chrome, and Firefox through `brew cask install`.

`db60402958d72ce39d24da3d8b2c15f92f75f2f5` (`moved files`, 14:19:25) adds `init_apps/hb-install.sh` and `init_apps/hb-packages.sh`. It does not delete the root copies. Git records two additions, not a rename. `e1f8546d6ac60da93fcc8e6c068f869ce09ea20e` (`removed files`, 14:24:10) deletes the root copies. The directory change is therefore two commits, five minutes apart.

`ff6981adbf3ef217818bac23c65110be3306c7ea` (`updating`, 17:32:35) adds `init_apps/apm-apps.sh`, `init_apps/hb-apps.md`, and `zer0_dev.md`, and modifies the two Homebrew scripts. `zer0_dev.md` opens with `# zer0` and names Windows, macOS, Homebrew, Atom, Git, LaTeX, Pandoc, iTerm, Zsh, and a section called Full Stack Attack. It also contains a local Windows path and a gist identifier. Those values stay in the original commit; they are not copied into this record. At this commit the tree is seven files: the workflow, the README, four files under `init_apps/`, and `zer0_dev.md`. The README is unchanged after the root commit.

## Inferences

The first two commits look like GitHub's web interface, not a local `git commit`. That inference rests on the committer name `GitHub`, the subjects `Initial commit` and `Create blank.yml`, and the workflow text matching GitHub's starter Actions template. The objects do not record which button was clicked.

The repository's stated purpose arrives before any tool. The README promises docs, tools, scripts, and information. The first implementation is a workflow that only echoes, then a pair of machine-setup scripts. The gap between the sentence and the scripts is visible. It is not evidence that a curriculum, a site, or a quest system existed on 2020-07-31.

`moved files` describes an intention that the diff does not perform. The copy lands first, and the deletion follows. That is a small, ordinary Git habit: the subject is the plan, and the patch is the act. It is also the first place this history asks a reader to distrust the subject line.

The spelling `zer0` appears in a note on the second day, while the README still says `zero to hero`. The later public stylization `zer0 to her0` is not established by these six commits. Only the first half of that stylization is present, and only in `zer0_dev.md`.

The local identity `amr abdel-motaleb` begins with the install scripts. That shows a change of tool, from the GitHub web editor to a local commit, not a change of ownership. The earlier author name Bamrman and this later name are both in the same two-day history. The commits do not say whether they are the same person.

## What this sample cannot say

It cannot say the workflow ran, that Homebrew was installed, or that any package in the scripts was present on a machine. A script file is not an execution. It cannot say why the files were rearranged, or what the Windows path was for. It cannot describe August 2020, the JavaScript file added later, or the second root created in March 2021.

## Evidence

Each claim above is recoverable from the listed commit. The derived index is `evidence.json` in this directory. Author email addresses are omitted.

- [git-commit:ab523954f523ddaf7402682c79630b36958fad79](https://github.com/bamr87/it-journey/commit/ab523954f523ddaf7402682c79630b36958fad79)
- [git-commit:4fda32c0153182b7ec6f30873a21c5c4812c709a](https://github.com/bamr87/it-journey/commit/4fda32c0153182b7ec6f30873a21c5c4812c709a)
- [git-commit:41fb5848e494d45fa05695240994c652bbbdacdc](https://github.com/bamr87/it-journey/commit/41fb5848e494d45fa05695240994c652bbbdacdc)
- [git-commit:db60402958d72ce39d24da3d8b2c15f92f75f2f5](https://github.com/bamr87/it-journey/commit/db60402958d72ce39d24da3d8b2c15f92f75f2f5)
- [git-commit:e1f8546d6ac60da93fcc8e6c068f869ce09ea20e](https://github.com/bamr87/it-journey/commit/e1f8546d6ac60da93fcc8e6c068f869ce09ea20e)
- [git-commit:ff6981adbf3ef217818bac23c65110be3306c7ea](https://github.com/bamr87/it-journey/commit/ff6981adbf3ef217818bac23c65110be3306c7ea)
