# Crush Workflow System: Visual Architecture Guide

This document provides visual diagrams explaining how the Crush Workflow System operates.

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "User Interface"
        A[Journey.sh TUI]
        B[Command Line]
    end
    
    subgraph "Workflow Engine (.crush/workflows/)"
        C[engine.sh<br/>Main Orchestrator]
        D[state-manager.sh<br/>State Persistence]
        E[prompt-runner.sh<br/>AI Execution]
    end
    
    subgraph "Workflow Definitions"
        F[YAML Templates<br/>templates/*.yml]
    end
    
    subgraph "AI Prompts"
        G[Prompt Catalog<br/>.github/prompts/*.md]
    end
    
    subgraph "State Storage"
        H[Execution State<br/>work/workflows/]
        I[Checkpoints]
        J[Outputs]
        K[Logs]
    end
    
    subgraph "AI Engine"
        L[Crush<br/>AI Prompt Execution]
    end
    
    A --> C
    B --> C
    C --> F
    C --> D
    C --> E
    F --> C
    E --> G
    E --> L
    D --> H
    H --> I
    H --> J
    H --> K
    
    style A fill:#e1f5ff
    style C fill:#fff3e0
    style H fill:#e8f5e9
    style L fill:#f3e5f5
```

## 🔄 Workflow Execution Flow

```mermaid
sequenceDiagram
    participant User
    participant Journey.sh
    participant Engine
    participant State Manager
    participant Prompt Runner
    participant Crush AI
    participant File System
    
    User->>Journey.sh: Select "Run Workflow"
    Journey.sh->>Engine: Execute workflow.yml
    Engine->>State Manager: Initialize execution
    State Manager->>File System: Create work/workflows/exec-ID/
    
    loop For Each Step
        Engine->>Engine: Parse step definition
        Engine->>State Manager: Update step status = running
        Engine->>Prompt Runner: Execute prompt with inputs
        Prompt Runner->>Crush AI: Run AI prompt
        Crush AI-->>Prompt Runner: Generated content
        Prompt Runner->>File System: Save outputs/
        Prompt Runner-->>Engine: Step completed
        Engine->>State Manager: Update step status = completed
        Engine->>State Manager: Save outputs to state
        
        alt Checkpoint
            State Manager->>File System: Save checkpoint
        end
    end
    
    Engine->>State Manager: Mark workflow complete
    State Manager->>File System: Update state.json
    Engine-->>Journey.sh: Workflow finished
    Journey.sh-->>User: Show completion summary
```

## 📊 Article + Quest Workflow Breakdown

```mermaid
graph LR
    subgraph "Phase 1: Drafting"
        A[Draft Article<br/>Outline] --> B[Generate<br/>Article FM]
        B --> C[Create Quest<br/>Outline]
        C --> D[Generate<br/>Quest FM]
    end
    
    subgraph "Phase 2: Expansion"
        D --> E[Expand Article<br/>with Examples]
        E --> F[Refine Quest<br/>with Challenges]
    end
    
    subgraph "Phase 3: Improvement"
        F --> G[Kaizen Loop<br/>Iteration 1]
        G --> H[Kaizen Loop<br/>Iteration 2]
        H --> I[Kaizen Loop<br/>Iteration 3]
    end
    
    subgraph "Phase 4: Publishing"
        I --> J[Validate<br/>Content]
        J --> K{Pass?}
        K -->|Yes| L[Prepare<br/>Publishing]
        K -->|No| G
        L --> M[Complete &<br/>Summarize]
    end
    
    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#fff3e0
    style F fill:#fff3e0
    style G fill:#f3e5f5
    style H fill:#f3e5f5
    style I fill:#f3e5f5
    style J fill:#ffebee
    style L fill:#e8f5e9
    style M fill:#e8f5e9
```

## 🔀 Data Flow Between Steps

```mermaid
graph TD
    A[User Inputs<br/>topic, level, difficulty] --> B[Draft Article]
    
    B --> C[article_outline]
    B --> D[learning_objectives]
    B --> E[target_audience]
    
    C --> F[Generate Article Frontmatter]
    D --> F
    E --> F
    
    F --> G[article_frontmatter]
    
    C --> H[Create Quest Outline]
    D --> H
    A --> H
    
    H --> I[quest_outline]
    H --> J[quest_objectives]
    
    I --> K[Generate Quest Frontmatter]
    J --> K
    
    K --> L[quest_frontmatter]
    
    C --> M[Expand Article]
    G --> M
    
    M --> N[expanded_article]
    
    I --> O[Refine Quest]
    L --> O
    N --> O
    
    O --> P[refined_quest]
    
    N --> Q[Improvement Loop]
    P --> Q
    
    Q --> R[improved_article]
    Q --> S[improved_quest]
    
    R --> T[Validate]
    S --> T
    G --> T
    L --> T
    
    T --> U[validation_report]
    
    R --> V[Prepare Publishing]
    S --> V
    G --> V
    L --> V
    
    V --> W[Final Article<br/>pages/_posts/]
    V --> X[Final Quest<br/>pages/_quests/]
    
    style A fill:#e1f5ff
    style W fill:#e8f5e9
    style X fill:#e8f5e9
```

## 💾 State Management Structure

```mermaid
graph TB
    subgraph "Workflow Execution"
        A[Start Workflow]
        A --> B[Initialize State]
        B --> C[Execute Steps]
        C --> D[Save Checkpoints]
        C --> E[Store Outputs]
        D --> F[Complete/Fail]
        E --> F
    end
    
    subgraph "File System: work/workflows/"
        G[article-quest-creation/]
        G --> H[execution-20251120-143022/]
        H --> I[state.json]
        H --> J[inputs.json]
        H --> K[outputs/]
        H --> L[checkpoints/]
        H --> M[logs/]
        
        K --> N[draft_article/]
        K --> O[generate_article_frontmatter/]
        K --> P[create_quest_outline/]
        K --> Q[...]
        
        L --> R[checkpoint-1.json]
        L --> S[checkpoint-2.json]
        
        M --> T[workflow.log]
        M --> U[steps/]
    end
    
    B -.-> I
    C -.-> K
    D -.-> L
    C -.-> M
    
    style A fill:#e1f5ff
    style H fill:#fff3e0
    style I fill:#e8f5e9
    style K fill:#e8f5e9
    style L fill:#ffebee
    style M fill:#f3e5f5
```

## 🔁 Loop Step Execution

```mermaid
graph TD
    A[Enter Loop Step] --> B{Iteration < Max?}
    B -->|Yes| C[Set loop.iteration]
    C --> D[Execute Prompt<br/>with Context]
    D --> E[Save Iteration<br/>Outputs]
    E --> F{Continue<br/>Condition?}
    F -->|True| G[Increment<br/>Iteration]
    G --> B
    F -->|False| H[Exit Loop]
    B -->|No| H
    H --> I[Proceed to<br/>Next Step]
    
    style A fill:#e1f5ff
    style D fill:#fff3e0
    style E fill:#e8f5e9
    style H fill:#e8f5e9
    style I fill:#e8f5e9
```

## 🎯 Interactive Input Collection

```mermaid
sequenceDiagram
    participant User
    participant Engine
    participant Gum TUI
    participant Workflow YAML
    
    Engine->>Workflow YAML: Read inputs.required
    
    loop For Each Required Input
        Engine->>Gum TUI: Show input prompt
        Gum TUI->>User: Display description & example
        User->>Gum TUI: Enter value
        Gum TUI->>Engine: Return input value
        Engine->>Engine: Validate input
    end
    
    Engine->>Workflow YAML: Read inputs.optional
    
    loop For Each Optional Input
        Engine->>Engine: Use default value or<br/>prompt if interactive
    end
    
    Engine->>Engine: Build inputs JSON object
    Engine->>State: Save inputs.json
```

## 🛠️ Error Handling Flow

```mermaid
graph TD
    A[Execute Step] --> B{Success?}
    B -->|Yes| C[Mark Complete]
    B -->|No| D{Retry Enabled?}
    D -->|Yes| E{Retries < Max?}
    E -->|Yes| F[Wait Backoff]
    F --> G[Retry Step]
    G --> A
    E -->|No| H[Check on_failure]
    D -->|No| H
    
    H --> I{Strategy}
    I -->|abort| J[Stop Workflow]
    I -->|skip| K[Continue to Next]
    I -->|alternate_step| L[Execute Fallback]
    
    C --> M[Continue Workflow]
    K --> M
    L --> M
    J --> N[Save Error State]
    N --> O[Cleanup if Configured]
    
    style A fill:#e1f5ff
    style C fill:#e8f5e9
    style J fill:#ffebee
    style M fill:#e8f5e9
```

## 🎨 Journey.sh Menu Integration

```
┌─────────────────────────────────────────┐
│  🚀 IT-Journey Terminal Interface       │
│  Browse quests, docs, and manage repo   │
└─────────────────────────────────────────┘

Choose your destination:
  📜 Browse Quests
  📖 Read Quickstarts
  📝 View Posts
  📊 View Statistics
> 🎯 Run Content Workflow  ◄── NEW
  🐳 Docker Controls
  🚪 Exit

┌─────────────────────────────────────────┐
│     🔮 Crush Workflow System            │
│  AI-powered content creation pipelines  │
└─────────────────────────────────────────┘

Choose workflow:
> 📝 Article + Quest Creation (Full Pipeline)
  ⚔️ Quest Only
  📰 Article Only
  🔄 Resume Previous Workflow
  📊 View Recent Executions
  🔙 Back to Main Menu
```

## 📈 Workflow Metrics and Monitoring

```mermaid
graph LR
    subgraph "Execution Metrics"
        A[Start Time]
        B[End Time]
        C[Duration]
        D[Step Count]
        E[Iterations]
        F[Checkpoints]
    end
    
    subgraph "Quality Metrics"
        G[Validation Score]
        H[Success Rate]
        I[Retry Count]
        J[Error Rate]
    end
    
    subgraph "Resource Metrics"
        K[AI Tokens Used]
        L[Output Size]
        M[Memory Usage]
        N[Disk Usage]
    end
    
    subgraph "State File: state.json"
        O[metrics: {...}]
    end
    
    A --> O
    B --> O
    C --> O
    D --> O
    E --> O
    F --> O
    G --> O
    H --> O
    I --> O
    J --> O
    K --> O
    L --> O
    M --> O
    N --> O
    
    style O fill:#e8f5e9
```

---

**Diagrams created with Mermaid** - View in GitHub or any Mermaid-compatible renderer for interactive diagrams.

**Related Documentation**:
- [Main README](README.md) - Complete system documentation
- [Quick Start](QUICKSTART.md) - Get started in 5 minutes
- [Summary](../../CRUSH_WORKFLOW_SYSTEM_SUMMARY.md) - Implementation overview
