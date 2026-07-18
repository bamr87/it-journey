---
title: 'Kubernetes ConfigMaps and Secrets: The Vault'
author: IT-Journey Team
description: 'Manage Kubernetes config with ConfigMaps and Secrets: inject settings via env vars and volume mounts, and guard credentials beyond base64.'
excerpt: Manage Kubernetes configuration securely with ConfigMaps, Secrets, env vars, and volumes
preview: images/previews/kubernetes-configmaps-quest-title-secrets-configur.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1001'
difficulty: 🟡 Medium
estimated_time: 75-90 minutes
primary_technology: kubernetes
quest_type: main_quest
quest_series: Kubernetes Mastery
quest_line: The Warrior's Orchestration Citadel
quest_arc: The Vault and the Ledger
quest_dependencies:
  required_quests:
  - /quests/1001/kubernetes-fundamentals/
  - /quests/1001/k8s-pods-workloads/
  recommended_quests:
  - /quests/1001/k8s-services-networking/
  unlocks_quests:
  - /quests/1010/monitoring-fundamentals/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Completion of Kubernetes Fundamentals and Pods and Workloads
  - Comfort writing and applying Pod and Deployment manifests
  - Awareness of the twelve-factor config principle
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A running local cluster (kind, minikube, or k3d)
  - kubectl configured against that cluster
  skill_level_indicators:
  - Can deploy a workload and edit its container spec
  - Ready to separate configuration from code
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A Deployment that reads config from a ConfigMap and a Secret
  skill_demonstrations:
  - Can inject configuration via env vars and via mounted volumes
  - Can explain why Secrets are not encrypted by default
  knowledge_checks:
  - Understands the difference between ConfigMaps and Secrets
  - Can troubleshoot a Pod that fails to start due to missing config
permalink: /quests/1001/k8s-config-secrets/
categories:
- Quests
- Cloud-Engineering
- Medium
tags:
- '1001'
- kubernetes
- main_quest
- cloud-engineering
- hands-on
- gamified-learning
keywords:
  primary:
  - '1001'
  - kubernetes
  - main_quest
  secondary:
  - cloud-engineering
  - hands-on
  - gamified-learning
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1001 (9) Quest: Main Quest - K8s Config'
rewards:
  badges:
  - 🏆 Keeper of the Vault - Mastered ConfigMaps and Secrets
  - 🔐 Twelve-Factor Adept - Separated configuration from code
  skills_unlocked:
  - 🛠️ Configuration Injection (env + volumes)
  - 🧠 Secret Management Best Practices
  progression_points: 75
  unlocks_features:
  - Completion of the Level 1001 Kubernetes Orchestration quest line
layout: quest
---
*The final gate of the Orchestration Citadel, Warrior. Your workloads run, heal, and connect - but they are hardcoded, brittle things, their database passwords baked into images for any eye to see. A true master never welds configuration to code. In this quest you learn the **Vault and the Ledger**: ConfigMaps to hold non-sensitive settings, and Secrets to guard credentials, both injected cleanly into your Pods without rebuilding a single image.*

*Whether you are externalizing a feature flag, mounting a TLS certificate, or stopping a password from leaking into a Git history, this adventure teaches the discipline that separates production-grade clusters from accidents waiting to happen.*

## 📖 The Legend Behind This Quest

*In the dark ages, configuration lived wherever it was convenient: hardcoded in source, smuggled into container images, scrawled across deploy scripts. Then a single leaked image with an embedded password would unmake an entire kingdom. The twelve-factor doctrine declared a law: store config in the environment, never in the code. Kubernetes gave that law two instruments - the ConfigMap for the harmless and the Secret for the sensitive - so the same image runs unchanged in dev, staging, and production, with only the injected config differing.*

*This quest teaches the "why" behind configuration hygiene. Master it, and you close the most common door attackers walk through: secrets left lying in the open.*

## 🎯 Quest Objectives

By the time you complete this epic journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **ConfigMaps** - Store non-sensitive configuration and inject it into Pods
- [ ] **Secrets** - Hold credentials and sensitive data separately from code
- [ ] **Injection via Environment Variables** - Surface config as env vars in a container
- [ ] **Injection via Volumes** - Mount config and secrets as files

### Secondary Objectives (Bonus Achievements)
- [ ] **Config Hygiene** - Apply the twelve-factor "config in the environment" rule
- [ ] **Secret Security** - Understand that base64 is encoding, not encryption, and enable at-rest encryption
- [ ] **Live Reload Awareness** - Know which injection methods update without a restart

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain when to use a ConfigMap versus a Secret
- [ ] Inject the same data as both env vars and mounted files
- [ ] Explain why a Secret's value is not actually encrypted by default
- [ ] Diagnose a Pod stuck because a referenced ConfigMap is missing

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Completion of [Kubernetes Fundamentals](/quests/1001/kubernetes-fundamentals/) and [Pods and Workloads](/quests/1001/k8s-pods-workloads/)
- [ ] Comfort writing and applying Deployment manifests
- [ ] Awareness of why configuration should live outside code

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A running local cluster (`kind`, `minikube`, or `k3d`)
- [ ] `kubectl` configured and on your `PATH`

### 🧠 Skill Level Indicators
This **🟡 Medium** quest expects:
- [ ] You can deploy a workload and edit its container spec
- [ ] You are ready to separate configuration from code
- [ ] Ready for 75-90 minutes of hands-on practice

## 🌍 Choose Your Adventure Platform

*ConfigMaps and Secrets are pure Kubernetes objects - they behave identically on every platform. You only need a working cluster and `kubectl`.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Confirm the cluster and set a working namespace
kubectl config use-context kind-citadel
kubectl create namespace vault
kubectl config set-context --current --namespace=vault
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
kubectl config use-context kind-citadel
kubectl create namespace vault
kubectl config set-context --current --namespace=vault
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
kubectl create namespace vault
kubectl config set-context --current --namespace=vault
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# On managed clusters the same objects work. Production clusters often integrate
# an external secret store (AWS Secrets Manager, Vault) via the Secrets Store CSI driver:
kubectl create namespace vault
kubectl config set-context --current --namespace=vault
```

**Cloud-Specific Notes:**
- Cloud KMS can encrypt Secrets at rest in etcd - enable it for production.
- External Secrets Operator and the Secrets Store CSI driver sync from cloud vaults.

</details>

## 🧙‍♂️ Chapter 1: ConfigMaps - The Ledger of Settings

*A **ConfigMap** holds non-sensitive key-value configuration: log levels, feature flags, service URLs, entire config files. Decoupling these from the image means one image runs everywhere, configured by its environment.*

### ⚔️ Skills You'll Forge in This Chapter
- Creating ConfigMaps imperatively and declaratively
- The two shapes: simple keys and whole config files
- Inspecting a ConfigMap

### 🏗️ Create a ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"            # simple key-value settings
  FEATURE_DARK_MODE: "true"
  app.properties: |            # an entire file as one value
    server.port=8080
    cache.ttl=300
    welcome.message=Greetings, adventurer
```

```bash
# Apply the manifest...
kubectl apply -f app-config.yaml

# ...or create one imperatively from literals or files
kubectl create configmap app-config \
  --from-literal=LOG_LEVEL=info \
  --from-literal=FEATURE_DARK_MODE=true

# Inspect it
kubectl get configmap app-config -o yaml
kubectl describe configmap app-config
```

### 🔍 Knowledge Check: ConfigMaps
- [ ] What kind of data belongs in a ConfigMap?
- [ ] How can a ConfigMap hold an entire config file?
- [ ] Name two ways to create a ConfigMap.

### ⚡ Quick Wins and Checkpoints
- [ ] **ConfigMap Created**: `kubectl get configmap app-config` succeeds
- [ ] **Data Verified**: You can see your keys in `describe` output

## 🧙‍♂️ Chapter 2: Secrets - The Guarded Vault

*A **Secret** looks like a ConfigMap but is meant for sensitive data: passwords, tokens, TLS keys. Kubernetes treats Secrets with extra care - but a critical truth: **Secret values are only base64-encoded, not encrypted, by default.** Encoding is not security.*

### ⚔️ Skills You'll Forge in This Chapter
- Creating Secrets safely
- Why base64 is not encryption
- Enabling encryption at rest

### 🏗️ Create a Secret

Prefer creating Secrets imperatively or from files so plaintext never lands in a committed YAML:

```bash
# From literals (Kubernetes base64-encodes for you)
kubectl create secret generic db-credentials \
  --from-literal=DB_USER=appuser \
  --from-literal=DB_PASSWORD='s3cr3t-p@ss'

# A TLS Secret from cert files (common for Ingress)
kubectl create secret tls web-tls --cert=tls.crt --key=tls.key

# Inspect - note the values are base64, NOT encrypted
kubectl get secret db-credentials -o yaml
echo 'czNjcjN0LXBAc3M=' | base64 --decode   # anyone can decode this!
```

If you must declare a Secret in YAML, use `stringData` so you write plaintext and Kubernetes encodes it - but **never commit such a file to Git**:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
stringData:                    # plaintext in, base64 stored (keep out of version control)
  DB_USER: appuser
  DB_PASSWORD: s3cr3t-p@ss
```

> ⚠️ Base64 is encoding, not encryption. Protect real Secrets with RBAC (limit who can `get secrets`), enable **encryption at rest** for etcd, and in production sync from an external vault (AWS Secrets Manager, HashiCorp Vault) via the External Secrets Operator.

### 🔍 Knowledge Check: Secrets
- [ ] Why is a Secret's value not actually secret on its own?
- [ ] Why prefer `kubectl create secret` over a committed YAML file?
- [ ] What three controls harden Secrets in production?

## 🧙‍♂️ Chapter 3: Injecting Configuration - Env Vars and Volumes

*Configuration is useless until it reaches your container. Kubernetes offers two injection styles: **environment variables** (simple, but fixed at start) and **mounted volumes** (files, which can update live).*

### ⚔️ Skills You'll Forge in This Chapter
- Injecting ConfigMaps and Secrets as env vars
- Mounting them as files via volumes
- Knowing which method updates without a restart

### 🏗️ Inject Everything Into a Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: busybox:1.36
          command: ["sh", "-c", "env | sort; cat /etc/appconfig/app.properties; sleep 3600"]
          env:
            - name: LOG_LEVEL                 # single key from a ConfigMap
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: LOG_LEVEL
            - name: DB_PASSWORD               # single key from a Secret
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: DB_PASSWORD
          envFrom:
            - configMapRef:                   # import ALL keys as env vars
                name: app-config
          volumeMounts:
            - name: config-volume             # mount the ConfigMap as files
              mountPath: /etc/appconfig
            - name: secret-volume             # mount the Secret as files
              mountPath: /etc/secrets
              readOnly: true
      volumes:
        - name: config-volume
          configMap:
            name: app-config
        - name: secret-volume
          secret:
            secretName: db-credentials
```

```bash
# Apply and verify the injection worked
kubectl apply -f app-deployment.yaml
kubectl rollout status deployment/app

# Confirm env vars landed
kubectl exec deploy/app -- sh -c 'echo $LOG_LEVEL; echo $FEATURE_DARK_MODE'

# Confirm mounted files exist (each key becomes a file)
kubectl exec deploy/app -- ls /etc/appconfig /etc/secrets
kubectl exec deploy/app -- cat /etc/appconfig/app.properties
```

**Env vars vs volumes - the live-update difference:**

| Method | Updates without restart? | Best for |
| --- | --- | --- |
| `env` / `envFrom` | No - env is fixed at container start | Simple scalar settings |
| Volume mount | Yes - the kubelet syncs changes into the file (with a short delay) | Files, certs, settings that may change |

After editing a ConfigMap, env-var consumers need a rollout to pick up changes:

```bash
kubectl edit configmap app-config        # change a value
kubectl rollout restart deployment/app   # required for env vars to refresh
```

### 🔍 Knowledge Check: Injection
- [ ] What is the difference between `valueFrom` and `envFrom`?
- [ ] Which injection method reflects ConfigMap edits without a restart?
- [ ] What happens to each ConfigMap key when mounted as a volume?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Externalize a Setting
**Objective**: Move a hardcoded setting into a ConfigMap.

**Requirements**:
- [ ] Create a ConfigMap with at least two keys
- [ ] Inject one key as an env var into a Pod
- [ ] Confirm the value is visible inside the container

**Validation**: `kubectl exec` shows the env var set from the ConfigMap.

### 🟡 Intermediate Challenge: Guard a Credential
**Objective**: Store a password in a Secret and consume it safely.

**Requirements**:
- [ ] Create a Secret with `kubectl create secret` (no committed plaintext)
- [ ] Inject it as an env var AND mount it as a file
- [ ] Explain why the stored value is base64, not encrypted

**Validation**: Both the env var and the mounted file contain the password.

### 🔴 Advanced Challenge: Full Config-Driven Deployment
**Objective**: Run one Deployment fully configured by external ConfigMaps and Secrets.

**Requirements**:
- [ ] Use `envFrom` to import all ConfigMap keys
- [ ] Mount both a ConfigMap and a Secret as volumes
- [ ] Edit the ConfigMap and demonstrate the volume update vs the env-var restart requirement
- [ ] State one production hardening step for the Secret

**Validation**: You can show config arriving via env vars and files, and explain the reload behavior of each.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Keeper of the Vault** - You master ConfigMaps and Secrets
- 🔐 **Twelve-Factor Adept** - You separate configuration from code

**🛠️ Skills Unlocked**:
- **Configuration Injection** - Env vars and volume mounts
- **Secret Management Best Practices** - Encoding vs encryption, RBAC, at-rest encryption

**🔓 Unlocked Quests**:
- Monitoring Fundamentals - Observe the cluster you now fully command

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [Monitoring Fundamentals](/quests/1010/monitoring-fundamentals/) - See inside your cluster

**Explore Side Adventures**:
- ⚔️ [Services and Networking](/quests/1001/k8s-services-networking/) - Revisit how config flows between services

### Character Class Recommendations

**💻 Software Developer**: Advance to [Monitoring Fundamentals](/quests/1010/monitoring-fundamentals/)  
**🏗️ System Engineer**: Revisit [Services and Networking](/quests/1001/k8s-services-networking/)  
**🛡️ Security Specialist**: Study the Secret hardening notes above closely

## 📚 Resources

### Official Documentation
- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) - Non-sensitive configuration
- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) - Sensitive data handling
- [Configure a Pod to Use a ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/) - Injection patterns
- [Encrypting Confidential Data at Rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) - Protect etcd

### Community Resources
- [The Twelve-Factor App: Config](https://12factor.net/config) - The config-in-the-environment principle
- [External Secrets Operator](https://external-secrets.io/) - Sync Secrets from cloud vaults
- [Secrets Store CSI Driver](https://secrets-store-csi-driver.sigs.k8s.io/) - Mount external secrets as volumes

### Learning Materials
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) - ConfigMap and Secret commands
- [Killercoda Configuration Scenarios](https://killercoda.com/kubernetes) - Hands-on config labs

## 🤝 Quest Completion Checklist

Before marking this quest as complete, ensure you've:

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Created a ConfigMap and a Secret
- [ ] ✅ Injected config via both env vars and volumes
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1001 (9) - Kubernetes Orchestration]] **Overworld:** [[🏰 Overworld - Master Quest Map]] **Prerequisites:** [[Kubernetes Fundamentals: Container Orchestration Essentials]] · [[Kubernetes Pods and Workloads: Deployments and StatefulSets]] **Sequel quests:** [[Monitoring Fundamentals: Master Metrics, Logs & Traces for Observability]] **Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
