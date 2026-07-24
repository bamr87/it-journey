---
title: 'Quest Walkthrough — System Engineer · Level 1001 (Kubernetes Orchestration)'
date: '2026-07-24T12:19:36.000Z'
character: system-engineer
level: '1001'
theme: Kubernetes Orchestration
tier: Warrior
quest_count: 4
mode: execute
overall_verdict: warn
session:
  window: '2 of 2 (offset 5, size 5)'
  level_total_quests: 9
  quests_walked: 4
  engine_average: 84.0
  engine_counts: '3 pass · 1 warn · 0 fail'
  engine_cost_usd: 3.2495
  evidence_source: sealed walk-evidence.json (agentic execute engine, real kind cluster k8s v1.36.1)
---

## 🎯 Session Summary

I walked the **second window (4 quests) of the 9-quest System Engineer / Level 1001 "Kubernetes Orchestration" slice** as a Warrior-tier learner would: Pods & Workloads → Services & Networking → ConfigMaps & Secrets → The Sigils of Trust. The machine evidence was pre-sealed by the workflow's `--mode execute` engine run against a **real kind cluster (k8s v1.36.1)**, so command outcomes below are witnessed, not asserted. Three quests pass cleanly (86 / 82 / 91) and one warns (77); engine average **84.0%**.

The headline for a maintainer: the individual quests are technically strong — nearly every runnable snippet executed and matched its claims — but the **linked journey has two real friction points**. First, two of the three Kubernetes quests open with a hardcoded `kubectl config use-context kind-citadel`, which the sandbox reproduced *failing* with `no context exists` for any learner who used minikube/k3d or a differently-named cluster (the stated prerequisites explicitly allow those). Second, the slice's fourth quest, **"The Sigils of Trust," belongs to an entirely different campaign** (The Self-Operating Website / GitHub Actions OAuth) and only shares the `1001` level code as a *difficulty* signal — a jarring topic switch for anyone reading the level top-to-bottom. Overall verdict: **warn** — no data-loss or unsafe content, but a real beginner would stall at command 1 of two quests, and the chain does not read as one coherent path.

## 🗺️ The Journey

| # | Verdict | Quest | Score | One-line takeaway |
|---|:--:|---|--:|---|
| 1 | ✅ | Kubernetes Pods and Workloads: Deployments and StatefulSets | 86 | Every workload controller (RS/Deployment/StatefulSet/DaemonSet/Job) verified on a real cluster; the macOS/Windows path's `kind-citadel` context is the one hole. |
| 2 | ✅ | Kubernetes Services and Networking: Ingress and DNS | 82 | Services, DNS, and Ingress all worked; the kind `extraPortMappings` fix arrives in Ch3, *after* the Platform Path already installs the controller without it. |
| 3 | ✅ | Kubernetes ConfigMaps and Secrets: The Vault | 91 | Cleanest quest of the slice — byte-for-byte base64 match verified; only a copy-the-whole-block `already exists` snag in Ch1. |
| 4 | ⚠️ | The Sigils of Trust: Auth, Secrets, and the Kill Switch | 77 | Solid GitHub-Actions security content, but `$OWNER/$REPO` are used in bash before ever being set — and it's off-theme for this level. |

## 🔬 Evidence

All statuses below come from the sealed `walk-evidence.json` (engine ran the snippets in a disposable kind cluster). "reasoned" = judged statically (no runner available for that step); "skipped" = could not be safely/​feasibly run in the sandbox.

### 1 · Pods and Workloads — 86 (pass) · ran 17/19 recorded snippets (16 passed · 1 failed · 2 reasoned)
Dimensions: commands_work **5**, content_accuracy 4, completeness 4, clarity 4, structure 4, safety 4.

- ✅ `kubectl apply -f web-rs.yaml` → 3 Pods `Running`; `kubectl delete pod -l app=web --wait=false` then `--watch` → **fresh Pods recreated within ~10s** (self-healing claim confirmed).
- ✅ `kubectl set image deployment/web web=nginx:1.27.1` → gradual rolling update via `maxUnavailable=1/maxSurge=1`; `kubectl rollout undo` reverted the image to `nginx:1.27` (verified via jsonpath).
- ✅ StatefulSet produced ordered names **db-0, db-1, db-2**; DaemonSet scheduled one Pod on the single node; Job reached `Completed`, `kubectl logs job/migrate` printed "running migration"/"done".
- ✅ `kubectl scale deployment/web --replicas=5` → 5/5 Ready.
- ❌ **`kubectl config use-context kind-citadel`** (macOS & Windows paths) → *"error: no context exists with the name: kind-citadel"*. The engine reproduced this directly; it only passed in the sandbox because a kind cluster named `citadel` was created explicitly. The Linux/Cloud paths avoid the assumption.
- 🧠 mermaid ownership diagram — no renderer in sandbox; syntax valid and later confirmed to match real `ownerReferences` (Deployment→ReplicaSet→Pod).

### 2 · Services and Networking — 82 (pass) · ran 13/18 recorded (13 passed · 0 failed · 3 skipped · 2 reasoned)
Dimensions: commands_work **5**, content_accuracy 4, completeness 4, clarity 3, structure 3, safety 4.

- ✅ ingress-nginx kind manifest applied (19 objects); `kubectl wait ... --for=condition=ready` → *"pod/ingress-nginx-controller-… condition met"*.
- ✅ `web-service.yaml` (ClusterIP) → Endpoints immediately populated with all 3 Pod IPs (`10.244.0.7-9:80`), exactly as the text promises.
- ✅ The quest's own **`;` vs `&&` busybox nslookup caveat verified true**: `nslookup web` printed NXDOMAIN search-domain noise yet resolved `web.default.svc.cluster.local`, and the following `wget` still returned the nginx page — a naive `&&` chain would have skipped it. Genuinely load-bearing, accurate warning.
- ✅ Ingress applied; `kubectl get ingress web-ingress` showed `ADDRESS=localhost` — **but only because the cluster was created up-front with the Ch3 `extraPortMappings` config** (see Issues).
- ✅ NetworkPolicy `db-allow-web` applied; no enforcement observed, consistent with the quest's own caveat about kind's default CNI.
- ⏭️ `curl -H "Host: app.local" http://localhost/` — the sandbox Bash tool denies `curl`/`wget` outright (tool-permission limit, unrelated to the quest); substituted an in-cluster `kubectl run` pod. `minikube addons enable ingress` and the cloud `LoadBalancer` path were also skipped (no minikube/cloud provider); LoadBalancer-stays-`<pending>`-locally was corroborated indirectly by the controller Service sitting at `EXTERNAL-IP <pending>`.

### 3 · ConfigMaps and Secrets — 91 (pass) · ran 9/11 recorded (8 passed · 1 failed · 1 skipped · 1 reasoned)
Dimensions: commands_work 4, content_accuracy **5**, completeness **5**, clarity 4, structure **5**, safety **5**.

- ✅ **Byte-for-byte match**: both `kubectl create secret --from-literal=DB_PASSWORD='s3cr3t-p@ss'` and the `stringData` YAML produced base64 `czNjcjN0LXBAc3M=`, exactly the value the quest tells the learner to `base64 --decode`.
- ✅ Deployment with `env`/`envFrom`/`volumeMounts` rolled out; `kubectl exec` showed `LOG_LEVEL=info`, `FEATURE_DARK_MODE=true`, and the mounted files under `/etc/appconfig` + `/etc/secrets` with exact `app.properties` content.
- ✅ Live-reload demonstrated: patching the ConfigMap updated the mounted `/etc/appconfig/LOG_LEVEL` file (kubelet sync, ~60s) while the env var stayed stale until `kubectl rollout restart` — confirming the quest's env-vs-volume table.
- ❌ **Ch1 ConfigMap block**: `kubectl apply -f app-config.yaml` followed by the imperative `kubectl create configmap app-config …` in the same block → *"configmaps app-config already exists"*. These are alternatives, not a sequence, but the doc doesn't say so.

### 4 · The Sigils of Trust — 77 (warn) · ran 0/6 recorded (0 passed · 2 skipped · 4 reasoned)
Dimensions: commands_work 3, content_accuracy 4, completeness 4, clarity 4, structure **5**, safety **5**.

- 🧠 All three workflow YAML excerpts (`content-factory.yml`, kill-switch, checkout token) parsed as valid YAML via `yaml.safe_load` after stripping the Jekyll `{% raw %}` tags.
- ⏭️ `gh secret set BOT_PAT --repo "$OWNER/$REPO"` and `gh variable set CONTENT_FACTORY_ENABLED …` could not be run — `gh` reported "not logged into any GitHub hosts" and each needs a real owned repo. Flag existence/usage was confirmed via `gh … --help`; `read -rs` silent capture was verified directly.
- 🧠 mermaid quest-network diagram — `mermaid-cli` failed on a sandboxed-Chromium launch error (environment limit, not a syntax issue); `graph LR` syntax is well-formed.
- This quest earns its **warn** honestly: it is almost entirely non-executable in this sandbox (2 runnable snippets, both requiring live GitHub auth), so the score leans on reasoning, and the one real usability defect (unset `$OWNER/$REPO`) is a `commands_work` deduction.

> Machine summary quoted from `walk-evidence.md`: *"3 pass · 1 warn · 0 fail · avg 84.0% · ~$3.2495."*

## 🐞 Issues Found

- **HIGH · Pods and Workloads · macOS + Windows Platform Path (lines 147 & 164)** — `kubectl config use-context kind-citadel` **failed** in the sandbox with *"no context exists with the name: kind-citadel"*. The prerequisites explicitly allow kind, minikube, *or* k3d and never establish a context named `kind-citadel`, so this is the *very first command* a beginner runs and it strands anyone who didn't happen to name their kind cluster `citadel`. **Fix:** use `kubectl config current-context` / `kubectl get nodes` like the Linux/Cloud paths already do, or say "substitute your own context name from the prior quest."
- **HIGH · ConfigMaps and Secrets · macOS + Windows Platform Path (lines 147 & 160)** — same hardcoded `kubectl config use-context kind-citadel` as above (reasoned by inspection; the engine ran against a cluster deliberately named `citadel`). Same fix. Flagging separately because it means **two of the three K8s quests in this slice** repeat the identical blocker.
- **HIGH · Services and Networking · Platform Path vs Chapter 3 (lines 144-151 vs 351-375)** — the kind `extraPortMappings` + `ingress-ready` fix that makes `curl … http://localhost/` work is documented in Ch3, *after* the Platform Path already installs the ingress-nginx controller. A learner going top-to-bottom hits *connection refused*, then has to recreate the cluster and reinstall the controller. **Fix:** move the "kind users — map the host ports first" callout up into System Requirements / Platform Path, before the controller install.
- **HIGH · The Sigils of Trust · Ch1 bash block + Mastery Challenge (lines 149-166)** — `$OWNER/$REPO` are used in `gh secret set --repo "$OWNER/$REPO"` and `gh variable set` but are **never shown being set**. Ironically the quest carefully warns about an *empty PAT* two lines later; an unset `$OWNER/$REPO` fails just as silently. **Fix:** add an explicit `export OWNER="your-username" REPO="your-repo"` before the first `gh` command.
- **MEDIUM · ConfigMaps and Secrets · Ch1 (lines 222-229)** — `kubectl apply -f app-config.yaml` then the imperative `kubectl create configmap app-config …` in one block **failed** with "already exists" when run verbatim. **Fix:** split into two blocks or add "run only one of these two."
- **MEDIUM · Pods and Workloads · Ch3 skills list + decision table (lines 357 & 451)** — Ch3 promises "Running batch work with Jobs and **CronJobs**" and the table lists CronJob, but no CronJob manifest is ever shown. **Fix:** add a short CronJob snippet or drop the overpromise.
- **MEDIUM · Services and Networking · Secondary objective "Troubleshooting" (line 108)** — "Diagnose a Service returning no endpoints" is listed as an objective and mastery indicator but has **no worked exercise**. **Fix:** add a deliberately-mismatched-selector example showing empty `kubectl get endpoints` and the fix.
- **LOW · Sigils of Trust · Prerequisites (line 101)** — "Generate the OAuth token from your Claude Code setup" is vague; give a concrete CLI command / doc link.
- **LOW · Pods and Workloads · YAML→filename mapping** — manifest filenames (`web-rs.yaml`, etc.) appear only inside later `kubectl apply -f …` lines, never labeled above the code fence; a first-timer must infer them.
- **LOW · Services and Networking · deprecation/​annotation nits** — `kubectl get endpoints` now emits a v1 Endpoints deprecation warning (mention `EndpointSlice`); the `rewrite-target: /` annotation on the root-Prefix Ingress is an inert no-op worth a one-line note.
- **LOW · Pods and Workloads · `rollout history` CHANGE-CAUSE** — shows `<none>` unless a `kubernetes.io/change-cause` annotation is added; worth a note so learners aren't confused by the sparse table.

## 🔗 Chain Continuity

**Where the chain holds (good pedagogy):**
- The forward-references are genuinely well-wired. Pods & Workloads plants `POSTGRES_PASSWORD: changeme` with an inline "move this to a Secret in the next quest," and the StatefulSet's `serviceName: db` is annotated "needs a headless Service (next quest)." ConfigMaps & Secrets Ch2 then *pays off* the Secret thread, and Services & Networking teaches exactly the Service the StatefulSet asked for. That's a real, deliberate through-line across quests 1→2→3.
- Quest 2 (Services) correctly declares quest 1 (Pods) as a `required_quest`, and quest 3 (Config) requires both — the dependency metadata matches the teaching order.

**Where a real learner would snag (reasoned — the engine scored each quest in isolation on a fresh `default` namespace, so it could not see these cross-quest interactions):**
- **Namespace drift.** Quest 1 ends with `kubectl config set-context --current --namespace=legions`; Quest 3 sets namespace `vault`; but **Quest 2 sets no namespace at all** and its DNS examples hardcode `web.default.svc.cluster.local`. A learner who carried the `legions` context out of Quest 1 into Quest 2 would land the `web` Deployment in `legions`, and the FQDN `web.default.svc.cluster.local` would **not resolve**. Quest 2 should either reset the namespace to `default` in its Platform Path or template the namespace segment. (Reasoned, not tested — high-confidence from reading the three Platform Paths back-to-back.)
- **The `kind-citadel` assumption is a chain artifact, not a per-quest one.** Quests 1 and 3 both assume a context named `kind-citadel` "from the previous quest," but the fundamentals quest that would create it is *outside this window* and the prerequisite text only guarantees "a running local cluster (kind/minikube/k3d)." Two of the three K8s quests therefore fail at command 1 for a learner who followed the prerequisites literally. Quest 2 gets this right — the inconsistency is clearly avoidable.
- **Thematic break at Quest 4.** "The Sigils of Trust" is `quest_series: The Autonomous Realm / quest_line: The Self-Operating Website`, `primary_technology: oauth`, `required_quests: []`, and recommends a *level-1000* war-machine chapter — it is **not part of the Kubernetes Orchestration line** at all. The quest even opens with a note that its `1001` is a *difficulty* signal, "not whatever general theme a level number might otherwise suggest." So a learner sweeping level 1001 in order gets three cohesive Kubernetes quests and then an abrupt pivot to GitHub Actions auth. The only connective tissue is a surface pun (K8s *Secrets* vs GitHub *secrets*). This is a planner/level-taxonomy observation for a maintainer, not a defect in the quest itself — but it means this slice does **not** read as one journey.

**Net:** quests 1-3 form a solid, correctly-ordered Kubernetes mini-arc with two fixable setup blockers; quest 4 is an off-theme co-resident of the level.

## 🧠 Reasoning & Method

- **Mode:** `execute` — evidence pre-sealed by the workflow's deterministic engine step against a real kind cluster (k8s v1.36.1, Docker 28.0.4). I consumed `walk-plan.json` + `walk-evidence.json`/`.md` **as-is**; I did not run, regenerate, or edit the engine (its child `claude` processes cannot authenticate from my Bash tool, per the skill).
- **What I ran myself:** only read-only inspection — I read all four quest sources in plan order and parsed the sealed evidence JSON. I executed **no** quest commands directly; every ✅/❌/⏭️ above is quoted from the sealed engine record.
- **What is `reasoned` vs `tested`:** the four continuity findings (namespace drift, `kind-citadel` chain artifact, thematic break, and the second quest's shared context blocker) are **reasoned** from reading the sources side-by-side — the engine scores each quest in an isolated fresh `default` namespace, so it structurally cannot observe carry-over state between quests. That gap is exactly this pass's value-add, and I've labeled it as reasoned, not witnessed.
- **Coverage & limits (honest):**
  - This is a **windowed** run — **4 of the level's 9 quests** (window 2 of 2, offset 5). The earlier five quests (including `kubernetes-fundamentals`, which supplies the `kind-citadel` cluster the K8s quests assume) were **not** walked this session; the perfection ledger accumulates the other window separately.
  - **Quest 4 is weak evidence:** 0 of 6 recorded snippets actually ran (2 skipped for live-GitHub-auth requirements, 4 reasoned). Its 77 leans on static reasoning — treat that score as lower-confidence than the three K8s quests, which were exercised for real.
  - Sandbox limits noted in the evidence: the Bash tool denies `curl`/`wget` (worked around in-cluster), no minikube/cloud-provider/PowerShell/mermaid renderer, so the macOS-vs-Windows and cloud paths and diagrams were reasoned as equivalent to the executed bash paths.
- **Confidence:** High on the three Kubernetes quests (real cluster, matching output). Medium on Sigils of Trust (mostly reasoned). High on the continuity findings as *reading* observations, explicitly reasoned rather than tested.
- **Scope discipline:** one slice, one report. No quest content edited; no branch/commit/PR. The caller handles git.
