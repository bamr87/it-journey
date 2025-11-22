---
applyTo: '**/*'
---

# Work Directory Instructions for AI Agents

AI agent instructions for implementing, managing, and optimizing the `work/` directory pattern in development environments, build systems, automation scripts, and CI/CD pipelines. These instructions guide AI assistants in helping developers create fast, isolated, cacheable, and disposable workspaces that improve organization, performance, and reproducibility across all development workflows.

## 🤖 AI Agent Role in Work Directory Implementation

### Primary Objectives
- **Assist in Workspace Design**: Help developers structure `work/` directories for optimal organization, performance, and maintainability
- **Automate Pattern Implementation**: Generate configuration files, scripts, and workflows that follow `work/` best practices
- **Optimize Performance**: Suggest caching strategies, parallel processing, and resource optimization techniques
- **Ensure Reproducibility**: Validate that implementations maintain consistency and cross-platform compatibility
- **Prevent Common Pitfalls**: Identify and resolve issues related to state leakage, disk exhaustion, path conflicts, and workspace pollution

### AI Assistant Boundaries
- **AI Does**: Generate directory structures, create workflow configurations, optimize caching strategies, automate cleanup scripts
- **AI Doesn't**: Make infrastructure decisions, determine business requirements, approve production deployments
- **Human Does**: Define project requirements, approve architectural decisions, monitor production performance
- **Human Validates**: Ensures security compliance, validates business logic, approves resource allocation

## 📋 Work Directory Pattern Detection and Implementation

### Intent Recognition for Work Directory Tasks

**When users express intent to use or optimize work directories, determine the specific need:**

1. **Performance Optimization**
   - Keywords: "slow build", "optimize", "cache dependencies", "speed up", "performance"
   - Guide to: Work directory structure implementation, caching strategies, parallel processing

2. **Workspace Organization**
   - Keywords: "organize", "clean workspace", "artifact management", "output structure", "directory structure"
   - Guide to: Directory structure design, artifact management patterns, separation of concerns

3. **Development Environment Issues**
   - Keywords: "inconsistent results", "works locally", "state pollution", "path conflicts", "environment setup"
   - Guide to: Ephemeral workspace design, cleanup strategies, isolation patterns

4. **Dependency and Resource Management**
   - Keywords: "dependency cache", "download time", "package management", "resource optimization"
   - Guide to: Selective caching patterns, resource allocation strategies

5. **Script and Automation Workflows**
   - Keywords: "script organization", "automation", "workflow management", "task execution"
   - Guide to: Work directory patterns for scripts, automation workflows, task isolation

### AI Prompt Templates for Work Directory Implementation

```markdown
// Analyze work directory requirements to implement work/ pattern:
// - Tools, dependencies, and workflows used
// - Development environment and platform constraints
// - Performance and organization requirements
// - Current workflow efficiency and resource usage
// - Platform compatibility needs (macOS, Windows, Linux, containers)
// - Usage context (development, CI/CD, scripts, automation)
//
// Once analyzed, generate appropriate work/ structure and configuration
```

## 🎯 AI-Assisted Work Directory Workflows

### Workflow 1: General Development Work Directory Setup

**Step 1: Context Analysis**
```markdown
// Prompt: "Analyze the development context for [project/script/workflow] and determine work/ directory needs:
// - What type of work is being performed (development, scripting, automation, building)
// - What tools and resources are involved
// - What artifacts need to be organized or cached
// - What cleanup and isolation requirements exist
// - Platform and environment constraints"
```

**Step 2: Directory Structure Design**
```markdown
// Generate work/ structure based on usage context:
// For general development:
// work/
// ├── cache/           # PERSISTENT - reusable resources
// ├── output/          # GENERATED - results and artifacts
// ├── temp/            # EPHEMERAL - temporary processing files
// ├── data/            # INPUT - source data and resources
// └── logs/            # TRACKING - execution and debug logs
//
// For specialized contexts, adapt structure accordingly
```

**Step 3: Usage Pattern Implementation**
```markdown
// Generate scripts and configurations that:
// - Initialize work/ structure for the specific use case
// - Implement appropriate caching and cleanup strategies
// - Use environment variables for path configuration
// - Include monitoring and validation as needed
// - Support cross-platform usage
```

### Workflow 2: CI/CD and Build System Integration

**Step 1: Build Environment Analysis**
```markdown
// Prompt: "Analyze the current build environment for [project] and generate a work/ directory structure that:
// - Separates persistent caches from ephemeral build outputs
// - Optimizes for [build tools: npm/pip/maven/gradle/cargo]
// - Supports [CI platform: GitHub Actions/GitLab CI/CircleCI/Jenkins]
// - Provides [performance target: <5min builds/<30s cache restore]
// - Ensures cross-platform compatibility for [platforms]"
```

**Step 2: Directory Structure Generation**
```markdown
// Generate work/ structure following this template:
// work/
// ├── cache/           # PERSISTENT - survives job runs
// │   ├── npm/         # Node.js package cache
// │   ├── pip/         # Python package cache  
// │   ├── maven/       # Java .m2 repository
// │   └── [tool]/      # Tool-specific caches
// ├── build/           # EPHEMERAL - regenerated each run
// │   ├── dist/        # Distribution packages
// │   └── reports/     # Test/coverage reports → ARTIFACTS
// ├── runtime/         # JOB-LOCAL - services for current run
// │   └── test-db/     # Temporary database instances
// └── temp/            # DISPOSABLE - aggressive cleanup
//     └── scratch/     # Temporary computation files
```

**Step 3: Configuration File Generation**
```markdown
// Generate CI/CD configuration that:
// - Creates work/ structure at job start
// - Implements selective caching for work/cache/ only
// - Outputs build artifacts to work/build/
// - Cleans work/temp and work/runtime on job completion
// - Uses environment variables for path configuration
// - Includes disk usage monitoring and cleanup
```

### Workflow 3: Resource Caching and Optimization Strategy

**Step 1: Cache Analysis**
```markdown
// Analyze current caching approach for [project] and optimize:
// - Identify cacheable vs regeneratable components
// - Design cache keys based on dependency files
// - Implement multi-layer fallback cache keys
// - Calculate optimal cache TTL based on update frequency
// - Design cache partitioning by tool/language
// - Plan cache invalidation strategies
```

**Step 2: Cache Implementation**
```markdown
// Implement caching strategy that:
// - Caches only work/cache/ directories (inputs, not outputs)
// - Uses composite cache keys: os-tool-version-hash(lockfile)
// - Provides fallback keys for partial cache hits
// - Implements separate caches per tool/language
// - Includes cache size monitoring and cleanup
// - Validates cache integrity and performance
```

### Workflow 4: Performance and Efficiency Optimization

**Step 1: Performance Analysis**
```markdown
// Analyze build performance for [project] and suggest optimizations:
// - Measure current build time breakdown by stage
// - Identify I/O bottlenecks and CPU-bound operations
// - Evaluate cache hit rates and restore times
// - Assess parallel build opportunities
// - Consider RAM disk mounting for compilation-heavy builds
// - Calculate resource utilization and constraints
```

**Step 2: Optimization Implementation**
```markdown
// Implement performance optimizations that:
// - Mount work/ as tmpfs/RAM disk for I/O-intensive builds
// - Partition builds into parallel work/build/partitions/
// - Pre-warm caches in setup jobs for monorepos
// - Use BuildKit cache mounts for Docker builds
// - Implement intelligent dependency resolution
// - Monitor and alert on performance regression
```

## 🔧 AI Generation Templates and Patterns

### General Purpose Work Directory Script Template

```bash
#!/usr/bin/env bash
# AI-generated general work/ directory management script

set -euo pipefail

# Configuration
WORK_DIR="${WORK_DIR:-./work}"
USAGE_CONTEXT="${WORK_CONTEXT:-development}"

# Platform detection
detect_platform() {
    case "$(uname -s)" in
        Darwin*)  echo "macos" ;;
        Linux*)   echo "linux" ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*) echo "windows" ;;
        *) echo "unknown" ;;
    esac
}

# Initialize work directory structure based on context
setup_work_structure() {
    local context="$1"
    local work_dir="$2"
    
    echo "Setting up work/ directory for context: $context"
    
    case "$context" in
        "development"|"general")
            mkdir -p "${work_dir}"/{cache,output,temp,data,logs}
            ;;
        "build"|"ci")
            mkdir -p "${work_dir}"/{cache/{npm,pip,maven},build/{dist,reports},runtime,temp}
            ;;
        "script"|"automation")
            mkdir -p "${work_dir}"/{cache,output,temp,logs,state}
            ;;
        "data-processing")
            mkdir -p "${work_dir}"/{cache,input,output,temp,logs,checkpoints}
            ;;
        *)
            # Default structure
            mkdir -p "${work_dir}"/{cache,output,temp,logs}
            ;;
    esac
    
    echo "Work directory structure created for $context"
    ls -la "$work_dir" 2>/dev/null || true
}

# Cleanup function
cleanup_work_directory() {
    local work_dir="$1"
    local context="$2"
    
    echo "Cleaning up work/ directory..."
    
    # Always clean temp
    rm -rf "${work_dir}/temp"/* 2>/dev/null || true
    
    # Context-specific cleanup
    case "$context" in
        "build"|"ci")
            rm -rf "${work_dir}"/{runtime,build} 2>/dev/null || true
            ;;
        "script"|"automation")
            # Keep state, clean output if specified
            if [[ "${CLEAN_OUTPUT:-false}" == "true" ]]; then
                rm -rf "${work_dir}/output"/* 2>/dev/null || true
            fi
            ;;
    esac
    
    echo "Work directory cleanup completed"
}

# Main execution
main() {
    local platform=$(detect_platform)
    echo "Work Directory Manager - Platform: $platform, Context: $USAGE_CONTEXT"
    
    setup_work_structure "$USAGE_CONTEXT" "$WORK_DIR"
    
    # Export standard environment variables
    export WORK_DIR
    export WORK_CACHE_DIR="${WORK_DIR}/cache"
    export WORK_OUTPUT_DIR="${WORK_DIR}/output"
    export WORK_TEMP_DIR="${WORK_DIR}/temp"
    export WORK_LOG_DIR="${WORK_DIR}/logs"
    
    echo "Environment variables set:"
    echo "WORK_DIR=$WORK_DIR"
    echo "WORK_CACHE_DIR=$WORK_CACHE_DIR"
    echo "WORK_OUTPUT_DIR=$WORK_OUTPUT_DIR"
    echo "WORK_TEMP_DIR=$WORK_TEMP_DIR"
    echo "WORK_LOG_DIR=$WORK_LOG_DIR"
    
    # Set up cleanup trap
    trap 'cleanup_work_directory "$WORK_DIR" "$USAGE_CONTEXT"' EXIT
}

# Execute if run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

### GitHub Actions Workflow Template

```yaml
# AI-generated template for GitHub Actions work/ integration
name: Build with Work Directory Pattern
on: [push, pull_request]

env:
  WORK_DIR: ${{ github.workspace }}/work
  CACHE_DIR: ${{ github.workspace }}/work/cache
  BUILD_DIR: ${{ github.workspace }}/work/build

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # 1. Initialize work/ structure
      - name: Setup work directory
        run: |
          mkdir -p work/{cache/{npm,pip,maven},build/{dist,reports},runtime,temp}
          echo "Work directory initialized:"
          tree -L 2 work/ || ls -R work/
      
      # 2. Restore selective cache (only work/cache/)
      - name: Restore dependency cache
        uses: actions/cache@v4
        with:
          path: work/cache/**
          key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', '**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-deps-
      
      # 3. Install dependencies with cache
      - name: Install dependencies
        run: |
          npm install --cache $CACHE_DIR/npm --prefer-offline
          pip install -r requirements.txt --cache-dir $CACHE_DIR/pip
      
      # 4. Build to work/build/
      - name: Build application
        run: |
          npm run build -- --output-path=$BUILD_DIR/dist
      
      # 5. Test and generate reports
      - name: Run tests
        run: |
          npm test -- --outputFile=$BUILD_DIR/reports/junit.xml
          pytest --junitxml=$BUILD_DIR/reports/pytest.xml
      
      # 6. Upload artifacts (not cached)
      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-outputs
          path: work/build/
      
      # 7. Cleanup ephemeral directories
      - name: Cleanup
        if: always()
        run: |
          rm -rf work/{temp,runtime,build}
          du -sh work/ || echo "Work directory cleaned"
```

### GitLab CI Configuration Template

```yaml
# AI-generated template for GitLab CI work/ integration
variables:
  WORK_DIR: "${CI_PROJECT_DIR}/work"
  CACHE_DIR: "${CI_PROJECT_DIR}/work/cache"
  BUILD_DIR: "${CI_PROJECT_DIR}/work/build"

cache:
  key:
    files:
      - package-lock.json
      - requirements.txt
  paths:
    - work/cache/

before_script:
  - mkdir -p work/{cache/{npm,pip},build/{dist,reports},runtime,temp}

stages:
  - dependencies
  - build
  - test
  - deploy

install_dependencies:
  stage: dependencies
  script:
    - npm install --cache $CACHE_DIR/npm
    - pip install -r requirements.txt --cache-dir $CACHE_DIR/pip

build_application:
  stage: build
  script:
    - npm run build -- --output-path=$BUILD_DIR/dist
  artifacts:
    paths:
      - work/build/dist/
    expire_in: 30 days

run_tests:
  stage: test
  script:
    - npm test -- --outputFile=$BUILD_DIR/reports/junit.xml
  artifacts:
    reports:
      junit: work/build/reports/junit.xml

after_script:
  - rm -rf work/{temp,runtime,build}
```

### Docker Configuration Template

```dockerfile
# AI-generated Dockerfile with work/ pattern
FROM node:18-alpine

# Set working directory and work/ structure
WORKDIR /app
RUN mkdir -p work/{cache,build,runtime,temp}

# Copy dependency files first for cache optimization
COPY package*.json ./
COPY requirements.txt ./

# Install dependencies with cache mounts
RUN --mount=type=cache,target=/app/work/cache/npm \
    npm install --cache /app/work/cache/npm --prefer-offline

RUN --mount=type=cache,target=/app/work/cache/pip \
    pip install -r requirements.txt --cache-dir /app/work/cache/pip

# Copy source and build
COPY . .
RUN npm run build -- --output-path=/app/work/build/dist

# Production stage (minimal, no caches)
FROM node:18-alpine
WORKDIR /app
COPY --from=0 /app/work/build/dist ./dist
CMD ["node", "dist/server.js"]
```

### Cross-Platform Script Template

```bash
#!/usr/bin/env bash
# AI-generated cross-platform work/ setup script

set -euo pipefail

# Platform detection
detect_platform() {
    case "$(uname -s)" in
        Darwin*)  echo "macos" ;;
        Linux*)   echo "linux" ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*) echo "windows" ;;
        *) echo "unknown" ;;
    esac
}

# Work directory setup
setup_work_directory() {
    local work_dir="${WORK_DIR:-./work}"
    
    echo "Setting up work/ directory structure..."
    mkdir -p "${work_dir}"/{cache,build,runtime,temp}
    mkdir -p "${work_dir}"/cache/{npm,pip,maven,gradle,cargo}
    mkdir -p "${work_dir}"/build/{dist,reports}
    
    # Platform-specific optimizations
    local platform=$(detect_platform)
    case "$platform" in
        "macos"|"linux")
            # Check for tmpfs/RAM disk option
            if [[ "${USE_RAMDISK:-false}" == "true" ]] && command -v mount >/dev/null; then
                echo "Setting up RAM disk for work/ directory..."
                setup_ramdisk "${work_dir}"
            fi
            ;;
        "windows")
            # Windows-specific optimizations
            echo "Applying Windows optimizations..."
            ;;
    esac
}

# RAM disk setup for performance
setup_ramdisk() {
    local work_dir="$1"
    local size="${RAMDISK_SIZE:-4G}"
    
    case "$(detect_platform)" in
        "macos")
            # macOS RAM disk setup
            diskutil erasevolume HFS+ "WorkRAM" `hdiutil attach -nomount ram://$(($(echo $size | sed 's/G//')*2097152))`
            ln -sf /Volumes/WorkRAM "${work_dir}"
            ;;
        "linux")
            # Linux tmpfs setup
            sudo mount -t tmpfs -o size="$size" tmpfs "${work_dir}"
            ;;
    esac
}

# Cleanup function
cleanup_work_directory() {
    local work_dir="${WORK_DIR:-./work}"
    
    echo "Cleaning up ephemeral work/ directories..."
    rm -rf "${work_dir}"/{temp,runtime,build}
    
    # Disk usage report
    if [[ -d "$work_dir" ]]; then
        echo "Remaining work/ size: $(du -sh "$work_dir" 2>/dev/null || echo "0B")"
    fi
}

# Trap cleanup on exit
trap cleanup_work_directory EXIT

# Main execution
main() {
    echo "Work Directory Setup - Platform: $(detect_platform)"
    setup_work_directory
    
    # Export environment variables
    export WORK_DIR="${WORK_DIR:-./work}"
    export CACHE_DIR="${WORK_DIR}/cache"
    export BUILD_DIR="${WORK_DIR}/build"
    export RUNTIME_DIR="${WORK_DIR}/runtime"
    
    echo "Work directory setup complete!"
    echo "WORK_DIR=$WORK_DIR"
    echo "CACHE_DIR=$CACHE_DIR"
    echo "BUILD_DIR=$BUILD_DIR"
}

# Execute if run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

## 📊 Validation and Quality Assurance Templates

### Performance Monitoring Script Template

```python
#!/usr/bin/env python3
"""
AI-generated performance monitoring script for work/ directory pattern
"""

import os
import time
import json
import subprocess
from pathlib import Path
from typing import Dict, Any

class WorkDirectoryMonitor:
    def __init__(self, work_dir: str = "./work"):
        self.work_dir = Path(work_dir)
        self.metrics = {}
    
    def measure_cache_performance(self) -> Dict[str, Any]:
        """Measure cache hit rates and restore times"""
        cache_dir = self.work_dir / "cache"
        
        metrics = {
            "cache_size": self._get_directory_size(cache_dir),
            "cache_age": self._get_oldest_file_age(cache_dir),
            "restore_time": None
        }
        
        # Measure cache restore time
        start_time = time.time()
        # Simulate cache operations
        for tool_cache in cache_dir.iterdir():
            if tool_cache.is_dir():
                list(tool_cache.rglob("*"))
        metrics["restore_time"] = time.time() - start_time
        
        return metrics
    
    def measure_build_performance(self) -> Dict[str, Any]:
        """Measure build times and output sizes"""
        build_dir = self.work_dir / "build"
        
        start_time = time.time()
        # Run build command (customize based on project)
        try:
            result = subprocess.run(
                ["npm", "run", "build", "--", f"--output-path={build_dir}/dist"],
                capture_output=True,
                text=True,
                timeout=600
            )
            build_success = result.returncode == 0
        except subprocess.TimeoutExpired:
            build_success = False
        
        build_time = time.time() - start_time
        
        return {
            "build_time": build_time,
            "build_success": build_success,
            "output_size": self._get_directory_size(build_dir / "dist") if build_success else 0,
            "artifact_count": len(list((build_dir / "dist").rglob("*"))) if build_success else 0
        }
    
    def check_disk_usage(self) -> Dict[str, Any]:
        """Monitor disk usage and cleanup needs"""
        total_size = self._get_directory_size(self.work_dir)
        cache_size = self._get_directory_size(self.work_dir / "cache")
        build_size = self._get_directory_size(self.work_dir / "build")
        
        # Check available disk space
        statvfs = os.statvfs(self.work_dir)
        available_space = statvfs.f_frsize * statvfs.f_bavail
        
        return {
            "total_work_size": total_size,
            "cache_size": cache_size,
            "build_size": build_size,
            "available_space": available_space,
            "cleanup_needed": total_size > available_space * 0.1  # 10% threshold
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        report = {
            "timestamp": time.time(),
            "work_directory": str(self.work_dir),
            "cache_performance": self.measure_cache_performance(),
            "build_performance": self.measure_build_performance(),
            "disk_usage": self.check_disk_usage()
        }
        
        # Calculate recommendations
        cache_metrics = report["cache_performance"]
        build_metrics = report["build_performance"]
        
        recommendations = []
        if cache_metrics["restore_time"] > 30:
            recommendations.append("Consider partitioning cache by tool/language")
        if build_metrics["build_time"] > 300:
            recommendations.append("Consider RAM disk mounting for build/ directory")
        if report["disk_usage"]["cleanup_needed"]:
            recommendations.append("Cleanup old cache files and temporary directories")
        
        report["recommendations"] = recommendations
        return report
    
    def _get_directory_size(self, directory: Path) -> int:
        """Get total size of directory in bytes"""
        if not directory.exists():
            return 0
        
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        return total_size
    
    def _get_oldest_file_age(self, directory: Path) -> float:
        """Get age of oldest file in directory (seconds)"""
        if not directory.exists():
            return 0
        
        oldest_time = time.time()
        for filepath in directory.rglob("*"):
            if filepath.is_file():
                file_time = filepath.stat().st_mtime
                oldest_time = min(oldest_time, file_time)
        
        return time.time() - oldest_time

if __name__ == "__main__":
    monitor = WorkDirectoryMonitor()
    report = monitor.generate_report()
    
    # Output JSON report
    print(json.dumps(report, indent=2))
    
    # Summary for humans
    print("\n=== Work Directory Performance Summary ===")
    print(f"Cache restore time: {report['cache_performance']['restore_time']:.2f}s")
    print(f"Build time: {report['build_performance']['build_time']:.2f}s")
    print(f"Total work/ size: {report['disk_usage']['total_work_size'] / 1024 / 1024:.1f} MB")
    
    if report['recommendations']:
        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"  - {rec}")
```

### Validation Checklist Template

```yaml
# AI-generated validation checklist for work/ directory implementation
work_directory_validation:
  structure:
    - [ ] work/ directory exists and is gitignored
    - [ ] cache/ subdirectories exist for each build tool
    - [ ] build/ directory includes dist/ and reports/ subdirectories
    - [ ] runtime/ and temp/ directories exist for ephemeral data
    - [ ] Environment variables are set for all paths
  
  caching:
    - [ ] Only work/cache/ is included in CI/CD cache configuration
    - [ ] Cache keys include relevant dependency file hashes
    - [ ] Fallback cache keys are configured for partial hits
    - [ ] Cache TTL is set appropriately for tool update frequency
    - [ ] Cache size monitoring and cleanup is implemented
  
  build_process:
    - [ ] Dependencies install to work/cache/ directories
    - [ ] Build outputs go to work/build/dist/
    - [ ] Test reports generate in work/build/reports/
    - [ ] Temporary files use work/temp/ or work/runtime/
    - [ ] All paths use environment variables, not hardcoded paths
  
  cleanup:
    - [ ] work/temp/ and work/runtime/ are cleaned after each job
    - [ ] work/build/ is cleaned after artifact upload
    - [ ] Disk usage monitoring alerts when >90% full
    - [ ] Old cache files are cleaned based on TTL
    - [ ] Failed builds trigger cleanup procedures
  
  performance:
    - [ ] Build time improvement measured and documented
    - [ ] Cache hit rate >80% after initial runs
    - [ ] Cache restore time <30 seconds
    - [ ] Total work/ size stays under resource limits
    - [ ] No performance regression on cache misses
  
  cross_platform:
    - [ ] Paths work correctly on Windows, macOS, and Linux
    - [ ] Scripts handle platform-specific optimizations
    - [ ] Container builds use proper work/ mounting
    - [ ] Permission issues are handled appropriately
    - [ ] Platform-specific cleanup works correctly
```

## 🔍 AI Troubleshooting Guide Templates

### Common Issue Detection and Resolution

```markdown
// AI Assistant Troubleshooting Decision Tree for Work Directory Issues

# Issue Category 1: Cache Problems
## Symptoms: Cache restored but build still slow
### AI Diagnosis Process:
1. Check if cache path matches installation path
2. Verify cache key includes correct dependency files
3. Validate cache wasn't corrupted or truncated
4. Confirm tool respects cache directory configuration

### AI Resolution Steps:
1. Generate debug commands to inspect cache contents
2. Create cache validation script
3. Update cache key to be more specific
4. Add cache integrity checks to workflow

# Issue Category 2: Disk Space Problems  
## Symptoms: "No space left on device" errors
### AI Diagnosis Process:
1. Measure current work/ directory sizes
2. Identify largest subdirectories and files
3. Check cache TTL and cleanup policies
4. Analyze disk usage trends over time

### AI Resolution Steps:
1. Generate emergency cleanup script
2. Implement proactive disk monitoring
3. Adjust cache TTL based on usage patterns
4. Add disk usage alerts to CI/CD pipeline

# Issue Category 3: Build Inconsistency
## Symptoms: Different results between local and CI builds
### AI Diagnosis Process:
1. Compare environment variables between environments
2. Check for absolute vs relative path issues
3. Validate work/ directory structure consistency
4. Identify missing cleanup between builds

### AI Resolution Steps:
1. Generate environment comparison script
2. Update paths to use absolute references
3. Add structure validation to build process
4. Implement comprehensive cleanup procedures
```

### Automated Issue Detection Script Template

```bash
#!/usr/bin/env bash
# AI-generated work/ directory health check script

set -euo pipefail

WORK_DIR="${WORK_DIR:-./work}"
ISSUES_FOUND=0

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    ((ISSUES_FOUND++))
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Check 1: Directory structure validation
check_directory_structure() {
    log_info "Checking work/ directory structure..."
    
    if [[ ! -d "$WORK_DIR" ]]; then
        log_error "work/ directory does not exist"
        return
    fi
    
    local required_dirs=("cache" "build" "runtime" "temp")
    for dir in "${required_dirs[@]}"; do
        if [[ ! -d "$WORK_DIR/$dir" ]]; then
            log_error "Missing required directory: $WORK_DIR/$dir"
        fi
    done
    
    # Check if work/ is gitignored
    if git check-ignore "$WORK_DIR" >/dev/null 2>&1; then
        log_info "work/ directory is properly gitignored"
    else
        log_warning "work/ directory is not gitignored - add 'work/' to .gitignore"
    fi
}

# Check 2: Cache configuration validation
check_cache_configuration() {
    log_info "Checking cache configuration..."
    
    # Check for common cache directories
    local cache_dirs=("npm" "pip" "maven" "gradle" "cargo")
    local found_caches=0
    
    for cache_dir in "${cache_dirs[@]}"; do
        if [[ -d "$WORK_DIR/cache/$cache_dir" ]]; then
            ((found_caches++))
            local cache_size=$(du -sh "$WORK_DIR/cache/$cache_dir" 2>/dev/null | cut -f1)
            log_info "Found $cache_dir cache: $cache_size"
        fi
    done
    
    if [[ $found_caches -eq 0 ]]; then
        log_warning "No tool-specific cache directories found"
    fi
}

# Check 3: Disk usage validation
check_disk_usage() {
    log_info "Checking disk usage..."
    
    if [[ -d "$WORK_DIR" ]]; then
        local work_size=$(du -sh "$WORK_DIR" 2>/dev/null | cut -f1)
        log_info "Total work/ directory size: $work_size"
        
        # Check available disk space
        local available=$(df -h "$WORK_DIR" | tail -1 | awk '{print $4}')
        local usage_percent=$(df -h "$WORK_DIR" | tail -1 | awk '{print $5}' | sed 's/%//')
        
        log_info "Available disk space: $available"
        
        if [[ $usage_percent -gt 90 ]]; then
            log_error "Disk usage is ${usage_percent}% - cleanup needed"
        elif [[ $usage_percent -gt 85 ]]; then
            log_warning "Disk usage is ${usage_percent}% - consider cleanup"
        fi
    fi
}

# Check 4: Environment variable validation
check_environment_variables() {
    log_info "Checking environment variables..."
    
    local required_vars=("WORK_DIR" "CACHE_DIR" "BUILD_DIR")
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            log_warning "Environment variable $var is not set"
        else
            log_info "$var=${!var}"
        fi
    done
}

# Check 5: Build artifact validation
check_build_artifacts() {
    log_info "Checking build artifacts..."
    
    if [[ -d "$WORK_DIR/build" ]]; then
        local artifact_count=$(find "$WORK_DIR/build" -type f 2>/dev/null | wc -l)
        if [[ $artifact_count -gt 0 ]]; then
            log_info "Found $artifact_count build artifacts"
            
            # Check for common build outputs
            if [[ -d "$WORK_DIR/build/dist" ]]; then
                local dist_size=$(du -sh "$WORK_DIR/build/dist" 2>/dev/null | cut -f1)
                log_info "Distribution build size: $dist_size"
            fi
            
            if [[ -d "$WORK_DIR/build/reports" ]]; then
                local report_count=$(find "$WORK_DIR/build/reports" -name "*.xml" -o -name "*.json" -o -name "*.html" | wc -l)
                log_info "Found $report_count test/coverage reports"
            fi
        else
            log_info "No build artifacts found (clean state)"
        fi
    fi
}

# Check 6: Performance indicators
check_performance_indicators() {
    log_info "Checking performance indicators..."
    
    # Look for signs of successful caching
    if [[ -d "$WORK_DIR/cache" ]]; then
        local cache_age=$(find "$WORK_DIR/cache" -type f -printf '%T@ %p\n' 2>/dev/null | sort -n | head -1 | cut -d' ' -f1)
        if [[ -n "$cache_age" ]]; then
            local current_time=$(date +%s)
            local age_hours=$(( (current_time - ${cache_age%.*}) / 3600 ))
            
            if [[ $age_hours -gt 168 ]]; then  # 7 days
                log_warning "Cache is $age_hours hours old - consider refresh"
            else
                log_info "Cache age: $age_hours hours (fresh)"
            fi
        fi
    fi
}

# Main execution
main() {
    echo "=== Work Directory Health Check ==="
    echo "Checking: $WORK_DIR"
    echo
    
    check_directory_structure
    check_cache_configuration
    check_disk_usage
    check_environment_variables
    check_build_artifacts
    check_performance_indicators
    
    echo
    echo "=== Health Check Summary ==="
    
    if [[ $ISSUES_FOUND -eq 0 ]]; then
        log_info "Work directory configuration appears healthy!"
    else
        log_error "Found $ISSUES_FOUND issue(s) that need attention"
        exit 1
    fi
}

# Run health check
main "$@"
```

## 📚 AI Learning Resources and Best Practices

### Continuous Learning for AI Agents

```markdown
// AI Agent should stay updated on these work/ directory patterns:

1. **Development Environment Patterns**
   - Monitor new development tools and workflows
   - Track container and virtualization improvements
   - Follow workspace organization best practices
   - Watch for new dependency and resource management tools

2. **Performance Optimization Techniques**
   - File system optimization across different platforms
   - Parallel processing strategies and resource allocation
   - Cache partitioning and optimization strategies
   - Cross-platform compatibility improvements

3. **Security and Best Practices**
   - Workspace security best practices
   - File permission and access control patterns
   - Resource isolation and sandboxing techniques
   - Compliance requirements for different domains

4. **Tool and Platform Integration Patterns**
   - Language and framework-specific optimizations
   - Development tool integration patterns
   - Platform-specific workspace optimizations
   - Automation and scripting best practices

5. **Emerging Workflow Patterns**
   - New development methodologies and their workspace needs
   - Cloud development environment patterns
   - Remote development and collaboration workflows
   - AI-assisted development workspace optimization
```

### AI Quality Metrics and Success Criteria

```yaml
# Metrics AI agents should track for work/ directory implementations
success_metrics:
  performance:
    workflow_efficiency_improvement: ">30% faster execution with optimization"
    cache_effectiveness_rate: ">80% cache hits when applicable"
    resource_access_time: "<30 seconds for cached resources"
    disk_usage_efficiency: "Appropriate size for context (<4GB for typical use)"
  
  reliability:
    output_consistency: ">95% reproducible results"
    resource_integrity_rate: "<1% corruption or access issues"
    cleanup_success_rate: "100% of scheduled cleanups"
    cross_platform_compatibility: "All target platforms supported"
  
  maintainability:
    configuration_simplicity: "Minimal setup and maintenance overhead"
    documentation_completeness: "All patterns and usage documented"
    monitoring_coverage: "Key metrics tracked when applicable"
    troubleshooting_effectiveness: "Issues resolved efficiently"
  
  usability:
    setup_time: "<5 minutes for new workspace setup"
    learning_curve: "Clear patterns easy to understand and apply"
    flexibility: "Adaptable to different use cases and contexts"
    integration_ease: "Works well with existing tools and workflows"
```

## 🔧 Integration with IT-Journey Development Principles

### Alignment with Core Principles

#### Design for Failure (DFF) in Work Directory Pattern
```markdown
// AI should implement work/ patterns that anticipate and handle failures:
// - Cache corruption: Implement validation and fallback strategies
// - Disk exhaustion: Monitor usage and implement cleanup policies
// - Build failures: Preserve artifacts for debugging while cleaning temp files
// - Platform differences: Provide fallbacks for platform-specific features
// - Network issues: Design for offline capability with cached dependencies
```

#### Don't Repeat Yourself (DRY) in Work Directory Implementation
```markdown
// AI should generate reusable work/ configurations:
// - Template workflows that work across multiple projects
// - Shared scripts for common operations (setup, cleanup, monitoring)
// - Parameterized configurations using environment variables
// - Modular cache strategies that can be composed
// - Cross-platform scripts that handle OS differences automatically
```

#### Keep It Simple (KIS) for Work Directory Management
```markdown
// AI should prioritize simplicity in work/ implementations:
// - Minimal configuration required for basic functionality
// - Clear directory structure that's self-documenting
// - Simple environment variable approach to path management
// - Straightforward cleanup and monitoring procedures
// - Obvious separation between cached and ephemeral data
```

### Educational Integration for IT-Journey

```markdown
// When implementing work/ patterns for IT-Journey, AI should:
// - Generate educational content explaining the why behind each decision
// - Include learning objectives for understanding build optimization
// - Provide troubleshooting guides that teach debugging skills
// - Create exercises for practicing performance optimization
// - Document the connection between work/ patterns and DevOps principles
// - Show how work/ directories support iterative development (REnO)
// - Demonstrate collaboration benefits through shared cache strategies (COLAB)
```

## 🚀 Advanced AI Automation Patterns

### Intelligent Cache Management

```python
# AI-generated intelligent cache management system
class IntelligentCacheManager:
    def __init__(self, work_dir: str, ci_platform: str):
        self.work_dir = work_dir
        self.ci_platform = ci_platform
        self.cache_metrics = {}
    
    def analyze_cache_effectiveness(self):
        """AI analyzes cache patterns and suggests optimizations"""
        # Track cache hit rates, restore times, and disk usage
        # Generate recommendations for cache key optimization
        # Suggest partitioning strategies based on usage patterns
        # Identify opportunities for cache pre-warming
        pass
    
    def auto_optimize_cache_strategy(self):
        """AI automatically optimizes cache configuration"""
        # Adjust cache TTL based on dependency update frequency
        # Partition caches when restore time exceeds thresholds
        # Implement predictive cache warming for common patterns
        # Auto-cleanup stale caches based on usage analytics
        pass
    
    def generate_custom_workflows(self):
        """AI generates optimized CI/CD workflows"""
        # Create platform-specific optimizations
        # Generate parallel build strategies
        # Implement intelligent resource allocation
        # Add performance monitoring and alerting
        pass
```

### Self-Healing Build Systems

```markdown
// AI-powered self-healing capabilities for work/ directories:

1. **Automatic Issue Detection**
   - Monitor build performance trends and detect degradation
   - Identify cache corruption and automatically regenerate
   - Detect disk space issues and trigger cleanup procedures
   - Recognize platform-specific failures and apply fixes

2. **Predictive Maintenance**
   - Forecast cache invalidation needs based on dependency patterns
   - Predict disk space requirements and pre-allocate resources
   - Anticipate build failures and pre-warm alternative caches
   - Schedule maintenance windows for optimal cache refresh

3. **Adaptive Configuration**
   - Adjust cache strategies based on project evolution
   - Optimize parallel build allocation based on resource usage
   - Fine-tune cleanup policies based on disk usage patterns
   - Update monitoring thresholds based on performance trends
```

---

**Version:** 1.0.0 | **Last Modified:** 2025-11-16 | **Author:** IT-Journey Team

**Related Files:**
- `features.instructions.md`: CI/CD pipeline integration patterns
- `contributing.instructions.md`: General contribution workflow guidance
- `copilot-instructions.md`: Core AI agent principles and integration

**Usage:** AI agents should reference these instructions when helping developers implement, optimize, or troubleshoot work/ directory patterns in any development context including local development, scripting, automation, CI/CD pipelines, and project organization. Focus on appropriate structure, performance, reliability, and maintainability while ensuring educational value for IT-Journey contributors.