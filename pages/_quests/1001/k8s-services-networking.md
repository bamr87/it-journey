---
title: 'Kubernetes Services and Networking: Ingress and DNS'
author: IT-Journey Team
description: 'Master Kubernetes networking with Services, Ingress, and cluster DNS, choosing between ClusterIP, NodePort, and LoadBalancer to expose workloads.'
excerpt: Configure Kubernetes networking with Services, Ingress, and DNS for scalable applications
preview: images/previews/kubernetes-services-quest-title-networking-ingress.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1001'
difficulty: 🔴 Hard
estimated_time: 90-120 minutes
primary_technology: kubernetes
quest_type: main_quest
quest_series: Kubernetes Mastery
quest_line: The Warrior's Orchestration Citadel
quest_arc: Roads, Gates, and the Naming of Things
quest_dependencies:
  required_quests:
  - /quests/1001/kubernetes-fundamentals/
  - /quests/1001/k8s-pods-workloads/
  recommended_quests: []
  unlocks_quests:
  - /quests/1001/k8s-config-secrets/
skill_focus: devops
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Completion of Kubernetes Fundamentals and Pods and Workloads
  - Comfort deploying a Deployment and reading its labels
  - Basic understanding of TCP/IP, ports, and DNS
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - A running local cluster (kind, minikube, or k3d)
  - kubectl configured against that cluster
  skill_level_indicators:
  - Can deploy and scale a workload with a Deployment
  - Ready to reason about how traffic reaches a Pod
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A workload exposed via a Service and reachable through Ingress
  skill_demonstrations:
  - Can choose between ClusterIP, NodePort, and LoadBalancer
  - Can resolve a Service by its cluster DNS name from inside a Pod
  knowledge_checks:
  - Understands how Service selectors map to Pod endpoints
  - Can troubleshoot a Service that returns no endpoints
permalink: /quests/1001/k8s-services-networking/
categories:
- Quests
- Cloud-Engineering
- Hard
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
sub_title: 'Level 1001 (9) Quest: Main Quest - K8s Networking'
rewards:
  badges:
  - 🏆 Gatekeeper - Mastered Services and Ingress
  - 🧭 Pathfinder - Understands cluster DNS and service discovery
  skills_unlocked:
  - 🛠️ Service Exposure (ClusterIP/NodePort/LoadBalancer)
  - 🧠 Ingress Routing and DNS Resolution
  progression_points: 75
  unlocks_features:
  - Access to the Configuration and Secrets quest
layout: quest
---
*Warrior, your workloads now run resilient and self-healing - but they are islands. Pods are mortal: they are born, they die, and their IP addresses vanish with them. How then does one Pod find another? How does the outside world reach your service when the very addresses keep shifting? This quest teaches the **roads, gates, and naming** of the cluster: Services that give workloads a stable identity, DNS that lets them find each other by name, and Ingress that opens the gates to the world beyond.*

*Whether you are wiring a frontend to a backend, exposing an API to the internet, or debugging why a request never arrives, this adventure forges the networking intuition every cluster Warrior needs.*

## 📖 The Legend Behind This Quest

*In the old realms, a server had one address, written on a scroll and never changed. In the cluster, addresses are ephemeral - a Pod replaced during a rollout takes a new IP, and any client holding the old one is lost. Kubernetes solved this with an abstraction: the **Service**, a stable virtual address and name that always points at whichever Pods are currently healthy. Layered atop it, **Ingress** provides a single smart gate that routes external traffic by hostname and path. Together they turn a shifting sea of Pods into a dependable map.*

*This quest teaches the "why" behind every connection in your cluster. Master it, and the network stops being a mystery and becomes a tool.*

## 🎯 Quest Objectives

By the time you complete this epic journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **The Service Abstraction** - Give a set of Pods a single stable virtual IP and DNS name
- [ ] **Service Types** - Choose correctly between ClusterIP, NodePort, and LoadBalancer
- [ ] **Cluster DNS and Discovery** - Resolve a Service by name from inside a Pod
- [ ] **Ingress Routing** - Route external HTTP traffic by host and path through one entry point

### Secondary Objectives (Bonus Achievements)
- [ ] **Endpoints** - Inspect how a Service maps its selector to live Pod IPs
- [ ] **NetworkPolicies** - Restrict which Pods may talk to which
- [ ] **Troubleshooting** - Diagnose a Service returning no endpoints

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain why a Service is needed even though Pods already have IPs
- [ ] Pick the right Service type for internal, dev, and production exposure
- [ ] Resolve `service.namespace.svc.cluster.local` and explain each segment
- [ ] Find why a Service has zero endpoints from `kubectl describe`

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Completion of [Kubernetes Fundamentals](/quests/1001/kubernetes-fundamentals/) and [Pods and Workloads](/quests/1001/k8s-pods-workloads/)
- [ ] Comfort deploying a Deployment and reading its labels
- [ ] Basic understanding of ports, TCP/IP, and DNS

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] A running local cluster (`kind`, `minikube`, or `k3d`)
- [ ] `kubectl` configured and on your `PATH`

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can deploy and scale a workload
- [ ] You are ready to reason about how traffic reaches a Pod
- [ ] Ready for 90-120 minutes of hands-on practice

## 🌍 Choose Your Adventure Platform

*Services and DNS work identically everywhere. Ingress requires a controller, which differs by platform - we'll use the NGINX Ingress controller, available on every cluster type.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
# Deploy a backend workload to expose
kubectl create deployment web --image=nginx:1.27 --replicas=3
# Install the NGINX Ingress controller (kind variant)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller --timeout=120s
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
kubectl create deployment web --image=nginx:1.27 --replicas=3
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=120s
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
# On minikube, the addon is the simplest route:
minikube addons enable ingress
# On kind, apply the controller manifest:
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl create deployment web --image=nginx:1.27 --replicas=3
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# On managed clusters, a Service of type LoadBalancer provisions a real cloud LB:
kubectl expose deployment web --type=LoadBalancer --port=80
kubectl get service web --watch   # EXTERNAL-IP fills in when the cloud LB is ready
```

**Cloud-Specific Notes:**
- `LoadBalancer` only provisions an external IP on clouds; locally it stays `<pending>`.
- Managed clusters also offer cloud-native Ingress controllers (AWS ALB, GKE Ingress).

</details>

## 🧙‍♂️ Chapter 1: The Service - A Stable Address Over Shifting Pods

*Pods come and go, and each gets a fresh IP. A **Service** is a stable virtual IP (the ClusterIP) plus a DNS name that always forwards to whichever Pods currently match its **selector**. This is the cornerstone of all Kubernetes networking.*

### ⚔️ Skills You'll Forge in This Chapter
- How a Service selector maps to live Pod endpoints
- The ClusterIP type for internal communication
- Inspecting the Endpoints object behind a Service

### 🏗️ Define a Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  type: ClusterIP          # internal-only stable virtual IP (the default)
  selector:
    app: web               # routes to every Pod carrying label app=web
  ports:
    - port: 80             # the port the Service listens on
      targetPort: 80       # the container port it forwards to
      protocol: TCP
```

```bash
# Apply it and inspect what it found
kubectl apply -f web-service.yaml
kubectl get service web
kubectl get endpoints web      # the live Pod IPs the Service forwards to
kubectl describe service web   # selector, ports, and endpoints in one view
```

The **Endpoints** object is the magic: the Service controller watches Pods matching the selector and keeps this list of healthy Pod IPs current. If the list is empty, the Service has nothing to forward to - the single most common Service bug.

### 🔍 Knowledge Check: The Service
- [ ] What links a Service to the Pods it serves?
- [ ] What is the difference between `port` and `targetPort`?
- [ ] What does an empty Endpoints list tell you?

### ⚡ Quick Wins and Checkpoints
- [ ] **Service Created**: `kubectl get service web` shows a ClusterIP
- [ ] **Endpoints Populated**: `kubectl get endpoints web` lists Pod IPs

## 🧙‍♂️ Chapter 2: Service Types and Cluster DNS - Reaching In and Finding by Name

*A ClusterIP is invisible from outside the cluster. To open it up, you choose a Service **type**. And to let Pods find each other, every Service gets a predictable DNS name.*

### ⚔️ Skills You'll Forge in This Chapter
- The three exposure types and when to use each
- The cluster DNS naming scheme
- Service discovery from inside a Pod

### 🏗️ The Three Service Types

| Type | What it does | Use when |
| --- | --- | --- |
| **ClusterIP** | Internal-only virtual IP (default) | Pod-to-Pod traffic inside the cluster |
| **NodePort** | Opens a port (30000-32767) on every node | Quick external access in dev / on-prem |
| **LoadBalancer** | Provisions a cloud load balancer with a public IP | Production external access on a cloud |

```yaml
# A NodePort Service: reach the app at <node-ip>:30080
apiVersion: v1
kind: Service
metadata:
  name: web-nodeport
spec:
  type: NodePort
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30080      # fixed node port (omit to let Kubernetes pick one)
```

### 🏗️ Cluster DNS - Finding Services by Name

Kubernetes runs an internal DNS service (CoreDNS). Every Service is resolvable at:

```text
<service-name>.<namespace>.svc.cluster.local
```

From a Pod in the same namespace, the short name `web` is enough. Prove it:

```bash
# Launch a throwaway Pod and resolve the Service by name
kubectl run netcheck --rm -it --image=busybox:1.36 --restart=Never -- \
  sh -c "nslookup web && wget -qO- http://web"

# Full FQDN works across namespaces:
kubectl run netcheck --rm -it --image=busybox:1.36 --restart=Never -- \
  nslookup web.default.svc.cluster.local
```

This is **service discovery**: your frontend connects to `http://backend` and never needs to know a Pod IP. CoreDNS resolves the name to the Service's stable ClusterIP, and the Service load-balances across healthy Pods.

### 🔍 Knowledge Check: Types and DNS
- [ ] When would you pick NodePort over LoadBalancer?
- [ ] What does each segment of `web.default.svc.cluster.local` mean?
- [ ] Why can a frontend hardcode `http://backend` safely?

## 🧙‍♂️ Chapter 3: Ingress and NetworkPolicy - The Smart Gate and the Walls

*Exposing every service as its own LoadBalancer is wasteful and costly. **Ingress** is a single smart gate that routes external HTTP(S) traffic to many Services by hostname and path. **NetworkPolicy** then lets you wall off who may talk to whom.*

### ⚔️ Skills You'll Forge in This Chapter
- Routing external traffic with Ingress rules
- Host- and path-based routing
- Restricting traffic with NetworkPolicy

### 🏗️ An Ingress Rule

An Ingress needs an **Ingress controller** running in the cluster (installed in the platform step). The Ingress resource then declares routing rules:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: app.local        # route requests for this hostname
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web     # forward to the 'web' Service
                port:
                  number: 80
```

```bash
# Apply the Ingress and verify it
kubectl apply -f web-ingress.yaml
kubectl get ingress web-ingress

# Test it (kind maps the controller to localhost). Send the Host header:
curl -H "Host: app.local" http://localhost/
```

One Ingress can route `app.local/` to the web Service and `app.local/api` to an API Service - many backends behind one gate.

### 🏗️ NetworkPolicy - Default-Deny Walls

By default, every Pod can talk to every other Pod. A **NetworkPolicy** restricts this. This policy says: Pods labeled `app=db` accept traffic *only* from Pods labeled `app=web`:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-allow-web
spec:
  podSelector:
    matchLabels:
      app: db
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: web
      ports:
        - protocol: TCP
          port: 5432
```

> Note: NetworkPolicies only take effect if your cluster's CNI plugin enforces them (Calico, Cilium). The kind default CNI does not - install Calico to practice enforcement.

### 🔍 Knowledge Check: Ingress and Policy
- [ ] What does an Ingress give you that many LoadBalancers do not?
- [ ] What must be running in the cluster for an Ingress resource to work?
- [ ] What is the default Pod-to-Pod traffic posture before any NetworkPolicy?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Expose with a ClusterIP
**Objective**: Put a stable internal address in front of the `web` Deployment.

**Requirements**:
- [ ] Create a ClusterIP Service selecting `app=web`
- [ ] Confirm its Endpoints list the Pod IPs
- [ ] Reach it by name from a throwaway Pod

**Validation**: `wget -qO- http://web` from inside the cluster returns the nginx page.

### 🟡 Intermediate Challenge: Resolve and Route
**Objective**: Prove DNS discovery and add NodePort access.

**Requirements**:
- [ ] `nslookup web` resolves to the ClusterIP from a Pod
- [ ] Add a NodePort Service and reach it on a node port
- [ ] Explain each segment of the FQDN

**Validation**: You can curl the app via both the cluster DNS name and the node port.

### 🔴 Advanced Challenge: Gate It With Ingress
**Objective**: Route external traffic through a single Ingress.

**Requirements**:
- [ ] Install/verify an Ingress controller
- [ ] Create an Ingress routing a hostname to the `web` Service
- [ ] Reach the app through the Ingress with the correct Host header
- [ ] (Bonus) Add a NetworkPolicy and reason about its effect

**Validation**: `curl -H "Host: app.local" http://localhost/` returns the app.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Gatekeeper** - You master Services and Ingress
- 🧭 **Pathfinder** - You understand cluster DNS and discovery

**🛠️ Skills Unlocked**:
- **Service Exposure** - ClusterIP, NodePort, and LoadBalancer
- **Ingress Routing and DNS Resolution** - One gate, many backends

**🔓 Unlocked Quests**:
- ConfigMaps and Secrets - Configure your now-connected workloads

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [ConfigMaps and Secrets](/quests/1001/k8s-config-secrets/) - Inject configuration safely

**Explore Side Adventures**:
- ⚔️ [Pods and Workloads](/quests/1001/k8s-pods-workloads/) - Revisit the workloads you exposed

### Character Class Recommendations

**💻 Software Developer**: Continue to [ConfigMaps and Secrets](/quests/1001/k8s-config-secrets/)  
**🏗️ System Engineer**: Revisit [Pods and Workloads](/quests/1001/k8s-pods-workloads/)  
**🛡️ Security Specialist**: Study the NetworkPolicy section above closely

## 📚 Resources

### Official Documentation
- [Service](https://kubernetes.io/docs/concepts/services-networking/service/) - ClusterIP, NodePort, LoadBalancer
- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) - HTTP routing rules
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) - The naming scheme
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) - Restricting Pod traffic

### Community Resources
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/) - The controller used above
- [CoreDNS](https://coredns.io/) - The cluster DNS server

### Learning Materials
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) - Service and Ingress commands
- [Killercoda Networking Scenarios](https://killercoda.com/kubernetes) - Hands-on networking labs

## 🤝 Quest Completion Checklist

Before marking this quest as complete, ensure you've:

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Exposed a workload with a Service
- [ ] ✅ Resolved a Service by its DNS name
- [ ] ✅ Routed external traffic through an Ingress
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/notes/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1001 (9) - Kubernetes Orchestration]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Prerequisites:** [[Kubernetes Fundamentals: Container Orchestration Essentials]] · [[Kubernetes Pods and Workloads: Deployments and StatefulSets]]
**Unlocks:** [[Kubernetes ConfigMaps and Secrets: Configuration Management Best Practices]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
