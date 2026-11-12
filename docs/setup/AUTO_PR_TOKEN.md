# The automation token (`AUTO_PR_GITHUB_TOKEN`)

> What the `AUTO_PR_GITHUB_TOKEN` repository secret is for, the fine-grained permissions the Issue Autopilot and the other PR lanes need from it, and how the owner re-issues it without the value reaching a terminal, a file or a log.

The agent lanes open their pull requests with a personal access token rather than the workflow's own `github.token`. GitHub raises no events for a push or a pull request made with `github.token`, so CI would not run on an agent's PR and the content auto-merge gate would have no checks to wait on. That token is the repository secret `AUTO_PR_GITHUB_TOKEN`.

Nothing rotates it. It is not in the hub's token contract (`_data/fleet.yml` `tokens:` in bamr87/bamr87), and a new personal access token can only be created in GitHub's web settings, so re-issuing it is always a job for the repository owner. This page is that job, written down.

## Why an expired token breaks the lanes

Every reader picks its token with `secrets.AUTO_PR_GITHUB_TOKEN || secrets.PAT_TOKEN || github.token`. That expression tests whether a secret is **set**, not whether it **works**. An expired `AUTO_PR_GITHUB_TOKEN` is still chosen, GitHub rejects it, and the job dies in `actions/checkout` with `could not read Username for 'https://github.com'` before any agent runs ([bamr87/bamr87#761](https://github.com/bamr87/bamr87/issues/761)). It never falls through to the next link, so an expired token has to be replaced or deleted.

## Required permissions

Create a **fine-grained** personal access token with exactly this:

| Setting | Value |
| --- | --- |
| Resource owner | `bamr87` |
| Repository access | **Only select repositories** → `bamr87/it-journey` |
| Contents | Read and write |
| Pull requests | Read and write |
| Issues | Read and write |
| Metadata | Read-only (GitHub adds it) |
| Everything else, and all account permissions | No access |
| Expiration | 90 days or less; write the date in the log below |

That is everything the Issue Autopilot's `resolve` job does with the token (`.github/workflows/issue-autopilot.yml`):

| The job does | Permission |
| --- | --- |
| `actions/checkout` with `token:`, then the resolver pushes its `content/issue-*` branch with the credentials checkout left behind | Contents: write |
| `gh pr list --label auto:issue` to de-dupe, `gh pr create` with the `auto:issue` and `collection/<area>` labels | Pull requests: write |
| `gh issue view` for each issue in the batch; a comment and the `needs-human` label on an issue it escalates instead of fixing | Issues: write |

The `gate` and `triage` jobs use `github.token` and do not read this secret. The resolver edits content only (`pages/**`, `assets/**`, `_data/quests/**`), so the token needs no Workflows, Actions, Administration, Secrets or Variables permission.

### The other readers

Ten more workflows read the same secret, so the new token serves them too. The three permissions above cover all of them except two soft edges:

| Workflow | What it does with the token | Beyond the three |
| --- | --- | --- |
| `content-factory.yml`, `agent-audit.yml`, `quest-forge.yml`, `quest-fix.yml`, `quest-walkthrough.yml`, `quest-perfection.yml`, `quest-video.yml` | Check out, push a branch, open a labelled PR; `quest-forge` creates its labels, `quest-perfection` upserts the loop-health issue | Nothing |
| `quest-fix-loop.yml` | Upserts the loop-health issue; lists open fix PRs and the walk lane's artifacts | Nothing (the repository is public) |
| `pr-freshness.yml` | Updates stale PR branches, labels and comments, then re-dispatches `content-auto-merge.yml` | **Actions: read and write**, for the re-dispatch only. Without it the step warns "could not dispatch the merge lane" and carries on. |
| `dependabot-auto-merge.yml` | Merges green Dependabot PRs | **Workflows: read and write**, only to merge a bump that touches `.github/workflows/**`. Without it the PR is labelled `manual-merge-required`. |

The same Workflows permission is what GitHub may ask of `pr-freshness.yml` when the branch it updates is missing workflow changes that `main` has gained; without it that update warns and the PR waits for a human.

Add those two permissions only if you want those lanes to do that unattended. Each one widens what a leaked token can do: Workflows lets it rewrite the CI that holds every other secret.

## Re-issuing it

Run this on the owner's own machine. Step 1 is a browser page only the owner can use.

1. **Mint.** Open <https://github.com/settings/personal-access-tokens/new>, fill in the table above, generate the token and copy it. GitHub shows it once.

2. **Store it straight from the clipboard**, then empty the clipboard. The value is never typed, echoed or written to disk.

   ```bash
   pbpaste | gh secret set AUTO_PR_GITHUB_TOKEN --repo bamr87/it-journey && pbcopy < /dev/null
   ```

   Without a clipboard tool, run `gh secret set AUTO_PR_GITHUB_TOKEN --repo bamr87/it-journey` with no pipe and paste at its hidden prompt.

3. **Check that it landed.** This prints names and dates, never values.

   ```bash
   gh secret list --repo bamr87/it-journey
   ```

4. **Prove it works.** The next scheduled Issue Autopilot run (18:10 UTC) does this for free: its `resolve` legs get past `actions/checkout`. To check sooner, dispatch the real lane, knowing that it runs the resolver and may open a PR:

   ```bash
   gh workflow run issue-autopilot.yml --repo bamr87/it-journey -f resolve=true
   ```

5. **Delete the old token** on <https://github.com/settings/personal-access-tokens> if it is still listed, and record the rotation in the log below: the date, the expiry and the issue. Never the value.

`PAT_TOKEN` is the older second link of the same chain. No workflow reads it without `AUTO_PR_GITHUB_TOKEN` in front of it, so it is never reached while that secret is set.

## Rules

- The token goes from GitHub's page to the clipboard to `gh secret set`, and nowhere else. No `--body "<token>"` (it lands in shell history), no `.env` in this repository, no issue, PR, commit or chat message.
- Nothing prints a secret. To see whether a rotation landed, read the secret's date in `gh secret list`, not its value.
- An agent may prepare this procedure and check the result. Per the Warden Pact in [AGENTS.md](../../AGENTS.md) it never sets or changes a secret.

## Rotation log

| Date | Event |
| --- | --- |
| 2026-07-02 | `AUTO_PR_GITHUB_TOKEN` and `PAT_TOKEN` last set. |
| 2026-10-31 | Scheduled Issue Autopilot runs start failing at `resolve` checkout: the token is set but rejected ([bamr87/bamr87#761](https://github.com/bamr87/bamr87/issues/761)). |
| 2026-11-11 | Still failing the same way ([run 43076078155](https://github.com/bamr87/it-journey/actions/runs/43076078155)). Required permissions and this procedure written down; the re-issue is pending the owner. |
