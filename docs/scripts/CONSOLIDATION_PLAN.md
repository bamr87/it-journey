<!--
@file docs/script-consolidation-plan.md
@description Comprehensive plan for consolidating and refactoring script directories
@author IT-Journey Team <team@it-journey.org>
@created 2025-07-07
@lastModified 2025-07-07
@version 1.0.0

@relatedIssues 
  - Script directory cleanup and organization

@relatedEvolutions
  - v1.0.0: Initial consolidation plan

@dependencies
  - Multiple script directories across workspace

@changelog
  - 2025-07-07: Initial creation - ITJ

@usage Reference document for script reorganization
@notes Follows IT-Journey principles for organization
-->

# Script Directory Consolidation Plan

## Current State Analysis

### Existing Script Directories:
- **ai-evolution-engine-seed/scripts/** - 25 evolution-related scripts
- **it-journey/scripts/** - 2 files (minimal)
- **it-journey/script/** - 11 mixed utility scripts
- **zer0-mistakes/scripts/** - 5 gem management scripts

## Consolidation Strategy

### 1. Standardize Directory Names
- **Rename** `it-journey/script/` → `it-journey/scripts/`
- **Maintain** consistent `/scripts` naming across all projects

### 2. Organize by Functional Categories

#### it-journey/scripts/ Structure:
```
scripts/
├── README.md                    # Main documentation
├── core/                        # Core utilities
│   ├── version-manager.sh       # Unified version management
│   ├── environment-setup.sh     # Environment configuration
│   └── git-hooks.sh            # Git automation
├── development/                 # Development tools
│   ├── build/
│   │   ├── create-dockerfile.sh
│   │   ├── create-gemfile.sh
│   │   └── build-site.sh
│   ├── content/
│   │   ├── jupyter-to-markdown.sh
│   │   └── append-feature.py
│   └── testing/
│       └── cibuild
├── deployment/                  # Deployment automation
│   └── update-settings.sh
└── legacy/                     # Deprecated scripts
    ├── zer0.sh
    ├── zer0.py
    └── zer0_md_to_sh.py
```

### 3. Eliminate Redundancies

#### Version Management Consolidation:
- **Merge** `it-journey/script/version-number.sh` + `zer0-mistakes/scripts/version.sh`
- **Create** unified `scripts/core/version-manager.sh`

#### Setup Script Consolidation:
- **Merge** `it-journey/script/zer0.sh` + `zer0-mistakes/scripts/setup.sh`
- **Create** unified `scripts/core/environment-setup.sh`

### 4. Refactoring Guidelines

#### Follow IT-Journey Principles:
- **DRY**: Single source of truth for common functionality
- **DFF**: Comprehensive error handling in all scripts
- **KIS**: Clear, focused scripts with single responsibilities
- **COLAB**: Consistent coding standards and documentation

#### Script Standards:
- **Headers**: All scripts must include standardized file headers
- **Logging**: Consistent logging and output formatting
- **Error Handling**: Graceful failure modes with meaningful messages
- **Documentation**: Inline comments and usage examples

## Implementation Plan

### Phase 1: Directory Restructuring
1. Create new organized directory structure
2. Move existing scripts to appropriate categories
3. Update all path references

### Phase 2: Script Consolidation
1. Merge redundant version management scripts
2. Consolidate setup and environment scripts
3. Refactor common utility functions

### Phase 3: Enhancement
1. Add standardized headers to all scripts
2. Implement consistent error handling
3. Update documentation and READMEs

### Phase 4: Integration
1. Update CI/CD workflows to use new paths
2. Test all script functionality
3. Archive legacy scripts safely

## Benefits

- **Reduced Maintenance**: Single source of truth for common operations
- **Improved Discoverability**: Logical organization by function
- **Better Documentation**: Comprehensive READMEs and inline docs
- **Consistent Quality**: Standardized error handling and logging
- **Enhanced Collaboration**: Clear conventions for script development
