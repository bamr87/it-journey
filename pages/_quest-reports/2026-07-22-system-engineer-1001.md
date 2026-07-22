---
title: System Engineer · L1001 · 2026-07-22
description: Quest-perfection walkthrough of the Kubernetes Orchestration slice system-engineer/1001 on
  2026-07-22, engine verdict warn (avg 71.8%). An evidence-based…
date: '2026-07-22T00:00:00.000Z'
author: Quest Perfection Loop
categories:
- Quest Reports
- System Engineer
tags:
- system-engineer
- level-1001
- walkthrough
- quest-perfection
- warn
- kubernetes-orchestration
render_with_liquid: false
excerpt: 'System Engineer · Level 1001 — Kubernetes Orchestration: an evidence-based quest-perfection
  walkthrough from 2026-07-22.'
slice: system-engineer/1001
character: system-engineer
level: '1001'
theme: Kubernetes Orchestration
tier: Warrior
verdict: warn
quest_count: 4
engine_average: 71.8
walk_date: '2026-07-22'
run_url: https://github.com/bamr87/it-journey/actions/runs/29916378064
source_report: test/quest-validator/walkthroughs/2026-07-22-system-engineer-1001.md
---

> **Slice** `system-engineer/1001` · **Level** 1001 (Kubernetes Orchestration) · **Warrior tier** · **Engine verdict** ⚠️ warn (avg 71.8%) · **Walked** 2026-07-22
>
> 🔗 [Perfection run](https://github.com/bamr87/it-journey/actions/runs/29916378064) · 🏠 [Perfection dashboard](/quest-reports/) · 📄 [Raw report](https://github.com/bamr87/it-journey/blob/main/test/quest-validator/walkthroughs/2026-07-22-system-engineer-1001.md) · 🕘 [Change history](https://github.com/bamr87/it-journey/commits/main/test/quest-validator/walkthroughs/2026-07-22-system-engineer-1001.md)

---

## 🎯 Session Summary

I walked the second window (quests 6–9) of the **System Engineer · Level 1001 "Kubernetes Orchestration"** slice as a learner: four `main_quest` pages, three 🔴 Hard and one 🟡 Medium. The machine evidence (execute mode, real `kubectl` against a live `kind` cluster) landed at **avg 71.8%** — **2 pass, 2 fail**. The conceptual teaching across the whole slice is genuinely strong (safety scored 5/5 everywhere, content accuracy 3–5), but **both Hard Kubernetes quests fail on their own advertised "prove it" commands**, and a linear beginner *will* get stuck at them without fixes.

Headline verdict: **⚠️ warn** — no safety problems and no conceptual rot, but two high-severity, reproducible command bugs (a StatefulSet that CrashLoopBackOffs for a missing `POSTGRES_PASSWORD`, and an Ingress `curl` that can never connect because the required `kind` port-mapping is never shown) block completion of two of the four quests. All defects are small and targeted; a maintainer can clear the blockers in an afternoon. One structural note for the curriculum owner: the fourth quest in this slice ("The Sigils of Trust") is a *different campaign* (GitHub Actions security) that only shares the `1001` level *number* — it does not continue the Kubernetes journey the first three build.

## 🗺️ The Journey

Walked in plan order (dependency-sorted window):

1. ❌ **Kubernetes Pods and Workloads: Deployments and StatefulSets** — 58 — solid pedagogy, but the Ch.3 StatefulSet never becomes Ready (no `POSTGRES_PASSWORD`) and the Ch.1 ReplicaSet is never cleaned up, so it collides with the Ch.2 Deployment's `app: web` selector and doubles the Pod counts the checkpoints promise.
2. ❌ **Kubernetes Services and Networking: Ingress and DNS** — 59 — Service/NodePort/Ingress/NetworkPolicy YAML all apply cleanly, but the two capstone proofs (chained `nslookup && wget` DNS check, and the `curl` to `localhost` for Ingress) both fail as written.
3. ✅ **Kubernetes ConfigMaps and Secrets: The Vault** — 88 — technically excellent; every core claim verified true on a real cluster. Only copy-paste hazards (an apply+create sequence, an unrunnable TLS example) and a missing cleanup step.
4. ✅ **The Sigils of Trust: Auth, Secrets, and the Kill Switch** — 82 — accurate and safety-conscious GitHub Actions/auth quest; the one defect is `$OWNER`/`$REPO` used but never defined, which breaks copy-paste with a cryptic `gh` format error.

## 🔬 Evidence

All results below come from the sealed `walk-evidence.json` (execute mode, `mock: false`), where the engine ran each quest's safe snippets for real in a disposable `kind` cluster. Per-dimension scores are on a 1–5 scale.

### 1. k8s-pods-workloads — ❌ fail · 58% · ran 13/7 runnable groups (11 passed · 2 failed · 2 reasoned)
- dimensions: commands_work **2**, content_accuracy 3, completeness 3, clarity 3, structure 3, safety 5
- **passed**: `kubectl apply -f web-rs.yaml` + delete/self-heal loop; `web-deployment.yaml` apply + `kubectl rollout status`; `kubectl set image deployment/web web=nginx:1.27.1` rolling update; `kubectl rollout history`; `kubectl rollout undo`; `kubectl scale deployment/web --replicas=5`; DaemonSet and Job apply + `kubectl logs job/migrate`.
- **failed** — `web-deployment.yaml` group: the Ch.1 ReplicaSet (`app: web`) is never deleted, so the Ch.2 Deployment's `app: web` selector adopts/overlaps those Pods — `kubectl get pods -l app=web` shows roughly double the count the quest's checkpoint claims ("shows three Pods").
- **failed** — `db-statefulset.yaml` group: `postgres:16` CrashLoopBackOffs because `POSTGRES_PASSWORD` is unset; the StatefulSet never reaches Ready, so the Advanced Challenge's "confirm ordered Pod names db-0/db-1/db-2 Running" cannot pass.
- **reasoned** (not executed): the mermaid ownership diagram; the Windows PowerShell platform block.

### 2. k8s-services-networking — ❌ fail · 59% · ran 11/7 runnable (9 passed · 2 failed · 1 skipped · 2 reasoned)
- dimensions: commands_work **2**, content_accuracy 3, completeness 3, clarity 3, structure 4, safety 5
- **passed**: `kubectl create deployment web --image=nginx:1.27 --replicas=3`; ingress-nginx `kind` deploy manifest + `kubectl wait ... --for=condition=ready`; `web-service.yaml`/`web-nodeport.yaml` apply + `get endpoints`/`describe service`; `web-ingress.yaml` apply + `kubectl get ingress`; NetworkPolicy apply; the *unchained* `nslookup web.default.svc.cluster.local`.
- **failed** — Ch.2 DNS proof: `kubectl run netcheck ... -- sh -c "nslookup web && wget -qO- http://web"` returns non-zero. busybox's `nslookup` exits non-zero from probing the search-domain list even after resolving, so the `&&` short-circuits and the pod shows `Error`, contradicting the quest's success framing.
- **failed** — Ch.3 / Advanced Challenge: `curl -H "Host: app.local" http://localhost/` → connection refused. The quest never shows the `kind create cluster --config` step with `extraPortMappings` (80/443) + `node-labels: ingress-ready=true`, so `localhost:80` was never mapped into the cluster on any platform tab.
- **skipped**: `minikube addons enable ingress` (alternate platform path, not the sandbox's cluster). **reasoned**: Windows PowerShell block; `kubectl expose ... --type=LoadBalancer` watch.

### 3. k8s-config-secrets — ✅ pass · 88% · ran 8/8 runnable (6 passed · 2 failed · 3 reasoned)
- dimensions: commands_work 4, content_accuracy **5**, completeness 4, clarity 4, structure 5, safety 5
- **passed**: ConfigMap YAML apply; Secret `stringData` YAML; the `app` Deployment with `valueFrom`/`envFrom`/volume mounts, then `kubectl exec` proving env vars (`$LOG_LEVEL`, `$FEATURE_DARK_MODE`) and mounted files (`/etc/appconfig`, `/etc/secrets`); `kubectl edit configmap` + `kubectl rollout restart` (live-reload behavior verified true).
- **failed** — the combined Ch.1 block runs `kubectl apply -f app-config.yaml && kubectl create configmap app-config --from-literal=...`: the create hits `AlreadyExists` after the apply, so copy-pasting the whole block errors.
- **failed** — Ch.2 `kubectl create secret tls web-tls --cert=tls.crt --key=tls.key`: `tls.crt`/`tls.key` are never generated, so the command can't run as written.
- **reasoned** (not executed): the Windows, Linux, and Cloud platform namespace-setup blocks. Note the engine still returned a **pass** — these two are copy-paste hazards, not conceptual defects.

### 4. self-operating-website-04-the-sigils-of-trust — ✅ pass · 82% · ran 2/2 runnable (0 passed · 2 failed · 4 reasoned)
- dimensions: commands_work 3, content_accuracy **5**, completeness 4, clarity 4, structure 5, safety 5
- **reasoned** (verified by inspection, not run — they need a real GitHub repo): three YAML excerpts (content-factory workflow job/step gating, kill-switch split, checkout token wiring) all parse cleanly and the auth claims check out against `gh 2.96.0`.
- **failed** — both runnable bash snippets: `gh secret set BOT_PAT --repo "$OWNER/$REPO" ...` and `gh variable set CONTENT_FACTORY_ENABLED --repo "$OWNER/$REPO" ...` use `$OWNER`/`$REPO` that the quest never defines, producing `expected the "[HOST/]OWNER/REPO" format, got "/"`. This is the *only* concrete defect; the quest's teaching is otherwise accurate.

**Machine summary (quoted from `walk-evidence.md`):** "4 quests evaluated · ✅ 2 pass · ⚠️ 0 warn · ❌ 2 fail · avg 71.8% · ~$3.4234".

## 🐞 Issues Found

Grouped by severity; every item cites evidence from §Evidence (a real command result) or the exact quest source. These are for a content pass — I did **not** edit any quest.

**HIGH**
1. **high** · *k8s-pods-workloads* · Ch.3 StatefulSet (`db-statefulset.yaml`, quest lines ~358–390) · **observed**: `postgres:16` CrashLoopBackOffs, StatefulSet never Ready (engine failed group). · **fix**: add `env: [{name: POSTGRES_PASSWORD, value: "changeme"}]` (or `POSTGRES_HOST_AUTH_METHOD=trust` for a demo) to the container spec.
2. **high** · *k8s-pods-workloads* · Ch.1→Ch.2 transition (ReplicaSet lines ~221–249 → Deployment lines ~271–336) · **observed**: `kubectl get pods -l app=web` shows ~double the "three Pods" the checkpoint (line 257) claims, because the Ch.1 ReplicaSet is never deleted and shares the `app: web` selector. · **fix**: `kubectl delete -f web-rs.yaml` before Ch.2, or relabel the ReplicaSet example (`app: web-rs-demo`).
3. **high** · *k8s-services-networking* · Ch.3 / Advanced Challenge · **observed**: `curl -H "Host: app.local" http://localhost/` → connection refused; no `extraPortMappings` step exists anywhere in the quest. · **fix**: add the `kind create cluster --config -` step with `extraPortMappings` (80/443) + `node-labels: ingress-ready=true` on every `kind` platform tab, before the ingress-nginx install.
4. **high** · *k8s-services-networking* · Ch.2 DNS proof · **observed**: `sh -c "nslookup web && wget -qO- http://web"` exits non-zero (busybox `nslookup` non-zero after a successful resolve), so the pod shows `Error`. · **fix**: split into two commands (`nslookup web; wget -qO- http://web`) or use `getent hosts web`.
5. **high** · *self-operating-website-04* · Ch.1 & Ch.2 bash snippets · **observed**: `$OWNER`/`$REPO` undefined → `expected the "[HOST/]OWNER/REPO" format, got "/"`. · **fix**: prepend `export OWNER="your-username" REPO="your-repo"` or use an inline literal placeholder with a substitution note.

**MEDIUM**
6. **medium** · *k8s-pods-workloads* · end of quest · no cleanup section; a learner leaves 5+ workloads + PVCs running. · **fix**: add `kubectl delete namespace legions`.
7. **medium** · *k8s-services-networking* · Secondary "Troubleshooting" objective · only described in prose, never exercised. · **fix**: add a hands-on step — apply a Service with a mismatched selector, `kubectl describe service`, read the empty Endpoints list.
8. **medium** · *k8s-config-secrets* · Ch.1 ConfigMap bash block · **observed**: `apply` then `create` on the same name → `AlreadyExists`. · **fix**: split declarative vs imperative into two blocks or add a "run only one" note.
9. **medium** · *k8s-config-secrets* · Ch.2 TLS Secret example · **observed**: `kubectl create secret tls` references `tls.crt`/`tls.key` that are never generated. · **fix**: add a one-line `openssl req ...` to make it runnable, or mark it a non-runnable reference.

**LOW**
10. **low** · *k8s-pods-workloads* · Ch.1 comment (line 244) says "delete a Pod" but the command `kubectl delete pod -l app=web` deletes *all* matching Pods. · **fix**: reword the comment.
11. **low** · *k8s-pods-workloads* · decision table (lines 435–443) lists CronJob but no CronJob example is given. · **fix**: add a short CronJob manifest or drop the row.
12. **low** · *k8s-services-networking* · Linux tab lacks the `kubectl wait --namespace ingress-nginx --for=condition=ready` step the macOS/Windows tabs have. · **fix**: add it for consistency.
13. **low** · *k8s-services-networking* · Ch.1 uses `kubectl get endpoints` (deprecated ≥ K8s 1.33). · **fix**: note/prefer `kubectl get endpointslices`.
14. **low** · *k8s-config-secrets* · file-saving is only implied before `kubectl apply -f <file>`. · **fix**: instruct learners to save each YAML block to its filename first.
15. **low** · *self-operating-website-04* · references `scripts/ai/run.sh content-curator` from the prior chapter without a pointer; add a one-line "assumed from Chapter III" note plus sample expected output for the unverifiable snippets.

## 🔗 Chain Continuity

Reading the four sources in plan order as one learner's journey:

- **The three Kubernetes quests form a coherent, well-sequenced arc.** Frontmatter dependencies are clean: `k8s-pods-workloads` requires `kubernetes-fundamentals`; `k8s-services-networking` requires fundamentals + pods-workloads; `k8s-config-secrets` requires fundamentals + pods-workloads and recommends services-networking. Concepts genuinely build (workloads → exposing them → configuring them), and quest 3 even reuses the `app` Deployment shape from quest 1. This ordering matches how a learner would actually progress.
- **Shared-cluster prerequisite is assumed but never re-established in this window.** All three K8s quests assume the `kind-citadel` context created back in `kubernetes-fundamentals` (window 0, not walked this run). That's acceptable for a windowed sweep, but note the **`kind` ingress port-mapping gap** (Issue #3) is a *continuity* failure, not just a quest-local bug: no quest in the level ever configures `extraPortMappings`, so quest 2's Ingress capstone is unreachable no matter how faithfully a learner followed the earlier quests. A fundamentals-level fix (mint the cluster with port mappings) would repair quest 2 downstream.
- **Namespace hygiene across the chain is inconsistent** — quest 1 works in `legions`, quest 2 in `default`, quest 3 in `vault`, and quest 1 never cleans up (Issue #6). A linear learner accumulates leftover objects; the Ch.1→Ch.2 selector collision (Issue #2) is a direct symptom of that missing cleanup discipline.
- **The fourth quest is a thematic outlier that breaks the journey.** "The Sigils of Trust" is Chapter IV of the *Self-Operating Website* campaign (GitHub Actions auth, PATs, kill switches) — its own frontmatter note (line 73) says it sits at `1001` purely as a *difficulty* signal, "not whatever general theme a level number might otherwise suggest." Its `required_quests` is empty and it recommends `self-operating-website-03` (a level-1000 quest), **not** any Kubernetes quest. So while it's a strong quest in isolation, a System Engineer walking "1001 = Kubernetes Orchestration" hits an abrupt topic switch with no bridge. This is a **planner/curriculum-taxonomy observation**, not a quest defect: the slice is defined by level code, and this level code mixes two campaigns. Worth flagging to whoever owns the level→theme mapping.

## 🧠 Reasoning & Method

- **Mode:** `execute` (real commands in a disposable `kind` sandbox), consumed from the **workflow-sealed** `walk-evidence.json` / `walk-evidence.md`. Per the skill, the execute engine cannot run from inside my agent (auth env is scrubbed from Bash-tool subprocesses), so I did **not** re-run it and did **not** edit the plan or evidence — I read them as-is.
- **What I ran vs. reasoned:** I did *not* execute quest commands myself. My evidence for every `passed`/`failed` is a command the sealed engine actually ran (cited per quest in §Evidence). My independent contribution is the **linked-journey reasoning** in §Chain Continuity, produced by reading all four quest sources in plan order (`Read` on each `path`) and cross-referencing frontmatter dependencies — those findings are `reasoned` (static), and I've labeled them so. Items marked `reasoned` in §Evidence are the engine's own non-executed snippets (platform-specific blocks, diagrams, GitHub-repo-dependent bash).
- **Coverage & limits:** This is **window 1 of 2** of the level (`stats`: offset 5, size 5) — **4 of the level's 9 quests** were walked this run; quests 1–5 (including `kubernetes-fundamentals`) are a separate window and were **not** walked here, so I cannot vouch for the fundamentals cluster-setup step that quest 2's Ingress issue ultimately traces back to. Engine spend for this window: ~$3.4234, 0 errored quests. The GitHub-auth quest's two runnable snippets are genuinely un-executable in the sandbox (no real repo), so its `commands_work` rests on 0 executed + 4 reasoned — weaker evidence, reflected honestly in its score.
- **Confidence:** High on the five HIGH command bugs — each is a concrete, reproducible engine failure with a clear cause and a one-to-three-line fix. Medium on the thematic-outlier continuity finding, which is a judgment call about curriculum taxonomy rather than a code defect. No safety issues observed anywhere (safety 5/5 across all four quests); no destructive commands were run.

**Overall slice verdict: ⚠️ warn** — conceptually strong and safe, but two of four quests carry high-severity blocking command bugs that stop a linear learner cold, plus a structural taxonomy mismatch on the fourth quest. Small, well-scoped fixes would move this slice to a clean pass.
