---
title: 'MLOps Engineering: CI/CD Pipelines for ML in Production'
author: IT-Journey Team
description: 'Take ML models from notebook to production with MLflow tracking, a model registry, FastAPI serving, drift monitoring, and CI/CD retraining pipelines.'
excerpt: Take ML models to production with experiment tracking, serving, drift monitoring, and CI/CD
preview: images/previews/mlops-descriptive-subtitle.png
date: '2025-11-29T22:51:57.000Z'
lastmod: '2026-06-14T00:00:00.000Z'
level: '1101'
difficulty: 🔴 Hard
estimated_time: 4-5 hours
primary_technology: mlflow
quest_type: main_quest
quest_series: AI/ML Mastery
quest_line: The Oracle's Ascent
quest_arc: From Notebook to Production
quest_dependencies:
  required_quests:
  - /quests/1101/ml-fundamentals/
  recommended_quests:
  - /quests/1101/deep-learning-frameworks/
  unlocks_quests:
  - /quests/1101/ai-ethics/
skill_focus: ai-ml
learning_style: hands-on
prerequisites:
  knowledge_requirements:
  - Completion of the ML Fundamentals quest (train + evaluate a model)
  - Comfortable building a model with scikit-learn or PyTorch
  - Basic familiarity with HTTP APIs and Docker helps
  system_requirements:
  - Modern OS (macOS, Windows 10+, Linux)
  - Python 3.10+ with pip or conda
  - Docker installed for the serving section (optional but recommended)
  skill_level_indicators:
  - You can train and evaluate a model end to end
  - You want models that run reliably in production, not just notebooks
validation_criteria:
  completion_requirements:
  - All primary objectives completed
  - A tracked experiment plus a model served behind an HTTP endpoint
  skill_demonstrations:
  - Can log experiments and register a model version
  - Can serve a model and detect input drift
  knowledge_checks:
  - Understands why ML systems need monitoring beyond accuracy
  - Can describe a CI/CD pipeline for retraining
permalink: /quests/1101/mlops/
categories:
- Quests
- Data-Science
- Hard
tags:
- '1101'
- mlops
- mlflow
- ci-cd
- main_quest
- data-science
- hands-on
- gamified-learning
keywords:
  primary:
  - '1101'
  - mlops
  - mlflow
  secondary:
  - experiment-tracking
  - model-serving
  - drift-monitoring
  - ci-cd
fmContentType: quest
draft: false
comments: true
sub_title: 'Level 1101 (13) Quest: Main Quest - MLOps Engineering'
rewards:
  badges:
  - 🏆 Production Oracle - Shipped a model from notebook to live endpoint
  - 📡 Drift Watcher - Built monitoring that detects when a model goes stale
  skills_unlocked:
  - 🛠️ Experiment Tracking & Model Registry
  - 🧠 Model Serving & Monitoring
  progression_points: 75
  unlocks_features:
  - Access to the AI Ethics quest of Level 1101
layout: quest
---
*Greetings, brave adventurer! A model that lives only in a notebook helps no one. To matter, it must serve real requests, survive real data, and improve over time. This quest, **MLOps Engineering**, leads you into the **Foundry of Production**, where machine learning becomes a reliable system instead of a one-off experiment. By its end you will have tracked an experiment, registered a model, served it behind an HTTP endpoint, and built a guard that watches for drift.*

*Whether you have only ever run `model.fit()` once and walked away, or you already sense that "it works on my machine" is not good enough, this adventure forges the discipline that turns a data scientist into an ML engineer.*

## 📖 The Legend Behind This Quest

*Software has DevOps - the practice of shipping code continuously and safely. Machine learning needs more, because an ML system has three moving parts that can each rot: the code, the model, and the data. A model trained last year on last year's data quietly decays as the world shifts beneath it. **MLOps** is the craft of keeping all three healthy: tracking every experiment so results are reproducible, registering model versions so deployments are deliberate, serving models so they answer requests, and monitoring inputs so silent decay becomes a loud alert.*

*This quest teaches the lifecycle that production AI demands - the difference between a clever demo and a system you can trust at 3 a.m.*

## 🎯 Quest Objectives

By the time you complete this journey, you will have mastered:

### Primary Objectives (Required for Quest Completion)
- [ ] **Experiment Tracking** - Log parameters, metrics, and artifacts with MLflow so runs are reproducible
- [ ] **Model Registry** - Version, stage, and promote models deliberately
- [ ] **Model Serving** - Expose a trained model behind an HTTP endpoint
- [ ] **Drift & Monitoring** - Detect when incoming data no longer matches training data

### Secondary Objectives (Bonus Achievements)
- [ ] **Containerized Serving** - Package the model and API in a Docker image
- [ ] **CI/CD for ML** - Sketch a pipeline that tests, trains, and deploys automatically
- [ ] **A/B Comparison** - Compare two model versions on the same traffic

### Mastery Indicators
You'll know you've truly mastered this quest when you can:
- [ ] Explain why monitoring accuracy is not enough in production
- [ ] Reproduce a past result from a logged experiment
- [ ] Decide when drift warrants a retrain
- [ ] Describe a safe rollout strategy for a new model version

## 🗺️ Quest Prerequisites

### 📋 Knowledge Requirements
- [ ] Completion of the ML Fundamentals quest (train + evaluate a model)
- [ ] Comfortable building a model with scikit-learn or PyTorch
- [ ] Basic familiarity with HTTP requests and JSON

### 🛠️ System Requirements
- [ ] Modern operating system (Windows 10+, macOS 10.14+, or Linux)
- [ ] Python 3.10 or newer on your PATH
- [ ] Docker (recommended for the serving section)
- [ ] A text editor or IDE (VS Code recommended)

### 🧠 Skill Level Indicators
This **🔴 Hard** quest expects:
- [ ] You can train and evaluate a model end to end
- [ ] You are ready to think about systems, not just notebooks
- [ ] Ready for 4-5 hours of focused, hands-on learning

## 🌍 Choose Your Adventure Platform

*MLflow and FastAPI are cross-platform. Docker is optional but makes the serving section production-realistic.*

### 🍎 macOS Kingdom Path

<details>
<summary>Click to expand macOS instructions</summary>

```bash
python3 -m venv ~/mlops-quest && source ~/mlops-quest/bin/activate
pip install --upgrade pip
pip install mlflow scikit-learn fastapi "uvicorn[standard]" pandas numpy

# Verify MLflow, then launch its tracking UI on http://localhost:5000
python -c "import mlflow; print('mlflow', mlflow.__version__)"
# mlflow ui    # run this in a separate terminal to browse experiments
```

</details>

### 🪟 Windows Empire Path

<details>
<summary>Click to expand Windows instructions</summary>

```powershell
python -m venv $HOME\mlops-quest
& $HOME\mlops-quest\Scripts\Activate.ps1
pip install --upgrade pip
pip install mlflow scikit-learn fastapi "uvicorn[standard]" pandas numpy

python -c "import mlflow; print('mlflow', mlflow.__version__)"
# mlflow ui   # browse runs at http://localhost:5000
```

</details>

### 🐧 Linux Territory Path

<details>
<summary>Click to expand Linux instructions</summary>

```bash
sudo apt update && sudo apt install -y python3-venv python3-pip
python3 -m venv ~/mlops-quest && source ~/mlops-quest/bin/activate
pip install --upgrade pip
pip install mlflow scikit-learn fastapi "uvicorn[standard]" pandas numpy

python -c "import mlflow; print('mlflow', mlflow.__version__)"
```

</details>

### ☁️ Cloud Realms Path

<details>
<summary>Click to expand Cloud/Container instructions</summary>

```bash
# In a Codespace or container, the same stack runs. To serve in Docker,
# build an image with your API and model, then run it:
docker build -t my-model-api .
docker run -p 8000:8000 my-model-api
```

</details>

## 🧙‍♂️ Chapter 1: Experiment Tracking and the Model Registry

*A data scientist runs dozens of experiments. Without tracking, last week's best result is unrecoverable. **MLflow** logs every run's parameters, metrics, and the model artifact itself, so any result can be reproduced and the best one promoted.*

### ⚔️ Skills You'll Forge in This Chapter
- Logging parameters, metrics, and model artifacts
- Comparing runs to choose a winner
- Registering and versioning a model

### 🏗️ Tracking a Run With MLflow

```python
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

X, y = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

mlflow.set_experiment("cancer-classifier")

n_estimators = 200
with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te)

    # Log the inputs and the results so this run is reproducible
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_metric("accuracy", accuracy_score(y_te, pred))
    mlflow.log_metric("f1", f1_score(y_te, pred))
    mlflow.sklearn.log_model(model, "model")
    print("Logged run to MLflow. Run `mlflow ui` to compare experiments.")
```

Change `n_estimators`, rerun, and MLflow records each attempt. The UI (`mlflow ui`) shows every run side by side so you pick a winner on evidence, not memory. Promote that run's model into the **registry**, which assigns it a version and a stage (Staging, Production) so deployments are deliberate and reversible.

### 🔍 Knowledge Check: Tracking
- [ ] Why log parameters as well as metrics?
- [ ] What problem does a model registry solve that file copies do not?
- [ ] What does "promoting to Production" stage actually decide?

### ⚡ Quick Wins and Checkpoints
- [ ] **Environment ready**: `import mlflow` works
- [ ] **First run logged**: You see a run in the MLflow UI

## 🧙‍♂️ Chapter 2: Serving a Model Behind an Endpoint

*A registered model still does nothing until it answers requests. **Serving** wraps the model in an HTTP API so applications can send features and receive predictions. FastAPI makes this a few lines.*

### ⚔️ Skills You'll Forge in This Chapter
- Wrapping a model in a FastAPI endpoint
- Validating request payloads
- Returning predictions as JSON

### 🏗️ A FastAPI Prediction Service

```python
# save as serve.py, then run: uvicorn serve:app --reload
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

# Train once and persist (in production you would load from the registry)
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
X, y = load_breast_cancer(return_X_y=True)
joblib.dump(RandomForestClassifier(n_estimators=200, random_state=42).fit(X, y), "model.joblib")

model = joblib.load("model.joblib")
app = FastAPI(title="Cancer Classifier")

class Features(BaseModel):
    values: list[float]    # 30 feature values per the dataset

@app.post("/predict")
def predict(req: Features):
    pred = int(model.predict([req.values])[0])
    proba = float(model.predict_proba([req.values])[0][pred])
    return {"prediction": pred, "confidence": round(proba, 4)}

@app.get("/health")
def health():
    return {"status": "ok"}
```

Run `uvicorn serve:app --reload`, then POST feature values to `http://localhost:8000/predict`. The `/health` route is what a load balancer or Kubernetes probe checks to know the service is alive. To make it portable, package it in Docker:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY serve.py model.joblib ./
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 🔍 Knowledge Check: Serving
- [ ] Why validate the request payload before predicting?
- [ ] What is the purpose of a `/health` endpoint?
- [ ] Why containerize the service instead of running it bare?

## 🧙‍♂️ Chapter 3: Monitoring, Drift, and CI/CD for ML

*A deployed model degrades silently. The world changes, incoming data drifts away from the training distribution, and accuracy quietly falls - often before anyone notices. **Monitoring** catches this. The simplest signal is **data drift**: are today's inputs statistically different from training?*

### ⚔️ Skills You'll Forge in This Chapter
- Detecting input drift with a statistical test
- Understanding model drift versus data drift
- Sketching a CI/CD retraining pipeline

### 🏗️ A Simple Drift Detector

```python
import numpy as np
from scipy.stats import ks_2samp

rng = np.random.default_rng(0)

# Training distribution for one feature
train_feature = rng.normal(loc=50, scale=5, size=1000)

# Two batches of "live" data: one in-distribution, one drifted
live_ok = rng.normal(loc=50, scale=5, size=300)
live_drifted = rng.normal(loc=58, scale=5, size=300)   # the world shifted

def drift_alert(reference, live, alpha=0.05):
    # Kolmogorov-Smirnov test: small p-value => distributions differ
    stat, p = ks_2samp(reference, live)
    return {"p_value": round(p, 4), "drift": p < alpha}

print("in-distribution:", drift_alert(train_feature, live_ok))      # drift False
print("shifted input:  ", drift_alert(train_feature, live_drifted)) # drift True
```

When drift fires, you investigate and often **retrain**. This is where **CI/CD for ML** closes the loop: a pipeline (GitHub Actions, for example) runs on new data or on a drift alert, retrains the model, evaluates it against a held-out set and a quality gate, and - only if it beats the current Production model - promotes the new version in the registry and rolls it out (often canary or A/B first). Code, data, and model all version together so any release is reproducible and reversible.

### 🔍 Knowledge Check: Monitoring & CI/CD
- [ ] What is the difference between data drift and model drift?
- [ ] Why might accuracy be unavailable in real time, making drift a useful proxy?
- [ ] What quality gate should block a retrained model from shipping?

## 🎮 Mastery Challenges

### 🟢 Novice Challenge: Compare Three Runs
**Objective**: Use tracking to choose a model.

**Requirements**:
- [ ] Log three MLflow runs with different `n_estimators`
- [ ] Open `mlflow ui` and sort by F1
- [ ] State which run you would promote and why

**Validation**: You can point to the highest-F1 run in the UI and justify the choice.

### 🟡 Intermediate Challenge: Serve and Call
**Objective**: Stand up the prediction service and query it.

**Requirements**:
- [ ] Run the FastAPI service from Chapter 2
- [ ] POST a real feature vector and capture the JSON response
- [ ] Confirm `/health` returns `ok`

**Validation**: You receive a prediction and confidence for a valid request.

### 🔴 Advanced Challenge: Drift to Retrain Trigger
**Objective**: Wire drift detection into a decision.

**Requirements**:
- [ ] Run the KS drift detector on an in-distribution and a drifted batch
- [ ] Write a function that returns `"retrain"` when drift fires on 2+ features
- [ ] Describe in three sentences what your CI/CD pipeline does on that signal

**Validation**: Your function recommends retraining only when meaningful drift is present.

## 🏆 Quest Rewards & Achievements

**🎖️ Badges Earned**:
- 🏆 **Production Oracle** - You shipped a model from notebook to live endpoint
- 📡 **Drift Watcher** - You built monitoring that detects a stale model

**🛠️ Skills Unlocked**:
- **Experiment Tracking & Model Registry** - Reproducible, versioned ML
- **Model Serving & Monitoring** - Endpoints plus drift detection

**🔓 Unlocked Quests**:
- AI Ethics - Govern the models you now deploy responsibly

**📊 Progression Points**: +75 XP

## 🗺️ Next Steps in Your Journey

**Continue the Main Story**:
- 🎯 [AI Ethics](/quests/1101/ai-ethics/) - Govern the models you can now deploy

**Explore Side Adventures**:
- ⚔️ [Deep Learning Frameworks](/quests/1101/deep-learning-frameworks/) - Build deeper models to deploy
- ⚔️ [ML Fundamentals](/quests/1101/ml-fundamentals/) - Refresh the evaluation discipline

### Character Class Recommendations

**💻 Software Developer**: Continue to [AI Ethics](/quests/1101/ai-ethics/)  
**🏗️ System Engineer**: Explore [AI Ethics](/quests/1101/ai-ethics/)  
**📊 Data Scientist**: Advance to [Deep Learning Frameworks](/quests/1101/deep-learning-frameworks/)

## 📚 Resources

### Official Documentation
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html) - Tracking, registry, and deployment
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - The serving framework used here
- [Docker Documentation](https://docs.docker.com/) - Containerizing the service

### Community Resources
- [Made With ML: MLOps Course](https://madewithml.com/) - A respected end-to-end course
- [Evidently AI Docs](https://docs.evidentlyai.com/) - Production drift and data-quality monitoring
- [Awesome MLOps](https://github.com/visenger/awesome-mlops) - Curated tools and reading

### Learning Materials
- [Google: MLOps - Continuous delivery for ML](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) - The MLOps maturity model
- ["Hidden Technical Debt in ML Systems" (Sculley et al.)](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) - Why ML systems rot

## 🤝 Quest Completion Checklist

- [ ] ✅ Completed all primary objectives
- [ ] ✅ Tracked an experiment and served a model
- [ ] ✅ Answered all knowledge check questions
- [ ] ✅ Completed at least one mastery challenge
- [ ] ✅ Explored the resource library
- [ ] ✅ Identified your next quest in the journey

## 🕸️ Knowledge Graph

*Structured wiki-links connect this quest to the IT-Journey knowledge graph. Open the [Obsidian Graph View](/docs/obsidian/graph/) to explore connections.*

**Level hub:** [[Level 1101 - Machine Learning & AI]]
**Overworld:** [[🏰 Overworld - Master Quest Map]]
**Required:** [[Machine Learning Fundamentals: Supervised & Unsupervised Learning with Scikit-Learn]]
**Unlocks:** [[AI Ethics and Responsible AI: Bias Detection, Fairness & Governance]]
**Obsidian docs:** [[Obsidian Knowledge Graph and Wiki Links]]
