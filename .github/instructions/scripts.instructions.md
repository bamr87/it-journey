---
applyTo: 'scripts/**/*'
---

# Scripts Directory Standards & Best Practices

Comprehensive standards and best practices for the IT-Journey scripts directory. This guide ensures all automation scripts are robust, maintainable, well-documented, and follow consistent patterns across different script categories.

## Overview

The `scripts/` directory contains automation tools, utilities, and deployment scripts that power the IT-Journey infrastructure. Scripts are organized by purpose into logical subdirectories and follow a unified architecture pattern for consistency and maintainability.

### Directory Structure

```
scripts/
├── core/                    # Core environment and system scripts
│   ├── environment-setup.sh # Development environment configuration
│   ├── version-manager.sh   # Version management utilities
│   └── README.md           # Core scripts documentation
├── deployment/             # Deployment and infrastructure scripts
│   └── update-settings.sh  # Configuration update automation
├── development/            # Development workflow scripts
│   ├── build/             # Build automation
│   ├── content/           # Content management scripts
│   └── testing/           # Testing utilities
├── examples/              # Example scripts and templates
│   └── data/             # Example data for testing
├── link-checker.py        # Link health monitoring (Python)
├── azure-jekyll-deploy.sh # Azure deployment automation
└── README.md             # Scripts directory documentation
```

## Script Categories

### Core Scripts (`core/`)

**Purpose**: Fundamental system setup and environment management

**Standards**:
- Must be idempotent (safe to run multiple times)
- Support both interactive and non-interactive modes
- Detect and adapt to different operating systems (macOS, Linux, WSL)
- Provide clear progress indicators and status messages
- Include comprehensive help documentation
- Validate prerequisites before making changes

**Examples**:
- `environment-setup.sh` - Complete development environment setup
- `version-manager.sh` - Manage tool versions (Ruby, Node.js, etc.)

### Deployment Scripts (`deployment/`)

**Purpose**: Production deployment and infrastructure management

**Standards**:
- Include dry-run mode for testing
- Implement rollback capabilities
- Log all operations for audit trails
- Validate deployment prerequisites
- Support multiple environments (dev, staging, production)
- Include health checks and validation steps
- Handle secrets securely (never hardcode credentials)

**Examples**:
- `update-settings.sh` - Configuration management
- `azure-jekyll-deploy.sh` - Azure Static Web Apps deployment

### Development Scripts (`development/`)

**Purpose**: Developer workflow automation and tooling

**Standards**:
- Optimize for developer experience
- Provide verbose output for debugging
- Include examples and usage demonstrations
- Support custom configuration
- Fast execution for frequent use
- Clear error messages with resolution steps

**Subdirectories**:
- `build/` - Build automation scripts
- `content/` - Content management and generation
- `testing/` - Test runners and validation scripts

### Monitoring Scripts

**Purpose**: System health, link checking, and monitoring

**Standards**:
- Support scheduled execution (cron, GitHub Actions)
- Generate structured output (JSON, Markdown)
- Include multiple analysis levels
- Create actionable reports
- Support both local and CI/CD execution
- Handle failures gracefully

**Examples**:
- `link-checker.py` - Comprehensive link health monitoring with AI analysis

## Universal Script Standards

All scripts in the repository MUST follow these standards:

### 1. Script Header Template

Every script must include a comprehensive header:

```bash
#!/usr/bin/env bash
#
# Script: script-name.sh
# Description: One-line description of what this script does
# Author: IT-Journey Team
# Version: 1.0.0
# Last Modified: YYYY-MM-DD
# Dependencies: list, of, required, commands
# Tested On: macOS 13+, Ubuntu 22.04+, WSL2
#
# Usage: script-name.sh [OPTIONS] [ARGUMENTS]
#        script-name.sh --help
#
# Exit Codes:
#   0 - Success
#   1 - General error
#   2 - Misuse of command (invalid arguments)
#   3 - Missing dependency
#   4 - Permission denied
#   5 - Configuration error
#   6 - Runtime error
#
# Related:
#   - Docs: link to relevant documentation
#   - Quest: link to related quest if applicable
```

### 2. Strict Error Handling

All bash scripts MUST use strict mode:

```bash
set -o errexit   # Exit on error (set -e)
set -o nounset   # Exit on undefined variable (set -u)
set -o pipefail  # Catch errors in pipes

# Optional for debugging
# set -o xtrace  # Enable for debugging (set -x)
```

### 3. Mandatory Features

Every script MUST include:

- ✅ **Shebang**: `#!/usr/bin/env bash` or `#!/usr/bin/env python3`
- ✅ **Help Function**: `--help` flag with usage examples
- ✅ **Version Information**: Version number and `--version` flag
- ✅ **Exit Codes**: Documented exit codes (0-255)
- ✅ **Logging**: At minimum: info, warn, error functions
- ✅ **Cleanup**: Trap handlers for EXIT, ERR, INT, TERM
- ✅ **Validation**: Dependency checking before execution
- ✅ **Dry-Run Mode**: `--dry-run` for safe testing (when applicable)
- ✅ **Verbose Mode**: `--verbose` for detailed output
- ✅ **Configuration**: Support config files or environment variables

### 4. Logging Framework

Implement a consistent logging system:

```bash
# Log levels
readonly LOG_LEVEL_DEBUG=0
readonly LOG_LEVEL_INFO=1
readonly LOG_LEVEL_WARN=2
readonly LOG_LEVEL_ERROR=3
readonly LOG_LEVEL_FATAL=4

log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    
    echo "[${timestamp}] [${level}] ${message}" >> "${LOG_FILE}" 2>/dev/null || true
    
    case "${level}" in
        DEBUG) [[ "${VERBOSE}" -eq 1 ]] && echo -e "${CYAN}[DEBUG]${NC} ${message}" >&2 ;;
        INFO)  echo -e "${GREEN}[INFO]${NC} ${message}" >&2 ;;
        WARN)  echo -e "${YELLOW}[WARN]${NC} ${message}" >&2 ;;
        ERROR) echo -e "${RED}[ERROR]${NC} ${message}" >&2 ;;
        FATAL) echo -e "${RED}[FATAL]${NC} ${message}" >&2 ;;
    esac
}

log_debug() { log "DEBUG" "$@"; }
log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }
log_fatal() { log "FATAL" "$@"; }
```

### 5. Cleanup and Error Handling

Always implement proper cleanup:

```bash
cleanup() {
    local exit_code=$?
    
    log_debug "Running cleanup (exit code: ${exit_code})"
    
    # Remove temporary files/directories
    if [[ -d "${TMP_DIR}" ]]; then
        rm -rf "${TMP_DIR}" 2>/dev/null || log_warn "Failed to remove temp dir"
    fi
    
    # Additional cleanup operations
    
    if [[ ${exit_code} -eq 0 ]]; then
        log_info "Script completed successfully"
    else
        log_error "Script exited with code ${exit_code}"
    fi
    
    exit "${exit_code}"
}

error_handler() {
    local line_number="$1"
    local exit_code="${2:-1}"
    log_fatal "Error occurred at line ${line_number} (exit code: ${exit_code})"
    exit "${exit_code}"
}

# Set trap handlers
trap cleanup EXIT
trap 'error_handler ${LINENO} $?' ERR
trap 'log_warn "Received SIGINT"; exit 130' INT
trap 'log_warn "Received SIGTERM"; exit 143' TERM
```

### 6. Utility Functions

Implement these standard utility functions:

```bash
# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Require specific commands
require_commands() {
    local missing_commands=()
    for cmd in "$@"; do
        if ! command_exists "${cmd}"; then
            missing_commands+=("${cmd}")
        fi
    done
    if [[ ${#missing_commands[@]} -gt 0 ]]; then
        log_fatal "Missing required commands: ${missing_commands[*]}"
        exit 3
    fi
}

# Safe directory creation
safe_mkdir() {
    local dir="$1"
    local perms="${2:-0755}"
    if [[ ! -d "${dir}" ]]; then
        mkdir -p "${dir}" || { log_error "Failed to create: ${dir}"; return 1; }
        chmod "${perms}" "${dir}"
    fi
}

# Confirmation prompt
confirm() {
    local prompt="$1"
    if [[ "${INTERACTIVE}" -eq 0 ]] || [[ "${FORCE_YES:-0}" -eq 1 ]]; then
        return 0
    fi
    local response
    read -r -p "${prompt} [y/N] " response
    [[ "${response}" =~ ^[yY]([eE][sS])?$ ]]
}
```

## Security Standards

### Secrets Management

**NEVER hardcode credentials**. Use these patterns:

```bash
# Environment variables (preferred)
: "${API_KEY:?API_KEY environment variable is required}"
: "${DATABASE_URL:?DATABASE_URL environment variable is required}"

# Configuration file
if [[ -f "${CONFIG_FILE}" ]]; then
    # shellcheck disable=SC1090
    source "${CONFIG_FILE}"
fi

# Secrets file with restricted permissions
readonly SECRETS_FILE="${HOME}/.it-journey/secrets"
if [[ -f "${SECRETS_FILE}" ]]; then
    # Verify permissions (should be 0600)
    local perms="$(stat -f %Lp "${SECRETS_FILE}" 2>/dev/null || stat -c %a "${SECRETS_FILE}" 2>/dev/null)"
    if [[ "${perms}" != "600" ]]; then
        log_error "Secrets file has incorrect permissions: ${perms} (should be 600)"
        exit 5
    fi
    # shellcheck disable=SC1090
    source "${SECRETS_FILE}"
fi
```

### Input Sanitization

Always validate and sanitize user input:

```bash
# Validate input matches expected pattern
validate_input() {
    local input="$1"
    local pattern="$2"
    if [[ ! "${input}" =~ ${pattern} ]]; then
        log_error "Invalid input: ${input}"
        return 1
    fi
}

# Sanitize filename
sanitize_filename() {
    local filename="$1"
    # Remove path components and dangerous characters
    basename "${filename}" | sed 's/[^a-zA-Z0-9._-]/_/g'
}

# Validate file path is within allowed directory
validate_path() {
    local target="$1"
    local allowed_base="$2"
    local resolved="$(cd "$(dirname "${target}")" && pwd)/$(basename "${target}")"
    [[ "${resolved}" == "${allowed_base}"* ]]
}
```

### Safe File Operations

```bash
# Use mktemp for temporary files
readonly TMP_DIR="$(mktemp -d -t "${SCRIPT_NAME%.sh}.XXXXXX")"

# Backup before modifying
backup_file() {
    local file="$1"
    if [[ -f "${file}" ]]; then
        cp -p "${file}" "${file}.backup.${TIMESTAMP}"
    fi
}

# Atomic file updates
atomic_write() {
    local target="$1"
    local content="$2"
    local tmpfile="${target}.tmp.$$"
    echo "${content}" > "${tmpfile}"
    chmod --reference="${target}" "${tmpfile}" 2>/dev/null || chmod 0644 "${tmpfile}"
    mv -f "${tmpfile}" "${target}"
}
```

## Python Scripts Standards

For Python scripts (like `link-checker.py`):

### Structure

```python
#!/usr/bin/env python3
"""
Script: script-name.py
Description: Brief description

Usage: script-name.py [OPTIONS]

Exit Codes:
    0: Success
    1: General error
    2: Invalid arguments
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('script.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show what would be done')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # Script logic here
        return 0
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
```

### Standards

- Use type hints for function signatures
- Include docstrings for all functions and classes
- Use `argparse` for command-line arguments
- Implement proper logging with levels (DEBUG, INFO, WARNING, ERROR)
- Handle exceptions gracefully
- Return meaningful exit codes
- Use `pathlib` for path operations
- Follow PEP 8 style guide

## Testing Requirements

### Script Testing Checklist

Before committing any script, verify:

#### Syntax & Linting
- [ ] **ShellCheck**: `shellcheck script-name.sh` (no errors)
- [ ] **Bash Syntax**: `bash -n script-name.sh` (validates syntax)
- [ ] **POSIX Check**: `checkbashisms script-name.sh` (if POSIX needed)
- [ ] **Python Lint**: `pylint script-name.py` or `ruff check script-name.py`

#### Functionality
- [ ] **Help Display**: `./script-name.sh --help` works
- [ ] **Version Display**: `./script-name.sh --version` works
- [ ] **Dry-Run Mode**: `./script-name.sh --dry-run` shows actions without executing
- [ ] **Verbose Mode**: `./script-name.sh --verbose` shows detailed output
- [ ] **Error Cases**: Invalid arguments produce clear error messages
- [ ] **Exit Codes**: Script exits with documented exit codes
- [ ] **Cleanup**: Temporary files removed on exit (normal and interrupted)

#### Platform Compatibility
- [ ] **macOS**: Tested on macOS 13+ (if applicable)
- [ ] **Linux**: Tested on Ubuntu 22.04+ (if applicable)
- [ ] **WSL**: Tested on WSL2 (if applicable)
- [ ] **CI/CD**: Runs successfully in GitHub Actions

#### Security
- [ ] **No Hardcoded Secrets**: No credentials in code
- [ ] **Input Validation**: User input is validated
- [ ] **Safe Temp Files**: Uses `mktemp` for temporary files
- [ ] **Proper Permissions**: Files created with appropriate permissions
- [ ] **No Command Injection**: Arguments properly quoted

#### Documentation
- [ ] **Header Complete**: All metadata filled out
- [ ] **Usage Examples**: At least 2-3 examples provided
- [ ] **Exit Codes**: All exit codes documented
- [ ] **Dependencies**: All requirements listed
- [ ] **README Updated**: Added to relevant README if new script

### Automated Testing

For complex scripts, include unit tests:

```bash
# Using bats (Bash Automated Testing System)
# File: test_script_name.bats

#!/usr/bin/env bats

@test "script exists and is executable" {
    [ -x "./script-name.sh" ]
}

@test "help flag displays usage" {
    run ./script-name.sh --help
    [ "$status" -eq 0 ]
    [[ "$output" =~ "Usage:" ]]
}

@test "invalid option produces error" {
    run ./script-name.sh --invalid-option
    [ "$status" -eq 2 ]
    [[ "$output" =~ "Unknown option" ]]
}

@test "dry-run mode does not modify files" {
    local before_count=$(ls -1 | wc -l)
    run ./script-name.sh --dry-run
    local after_count=$(ls -1 | wc -l)
    [ "$before_count" -eq "$after_count" ]
}
```

Run tests:
```bash
bats test_script_name.bats
```

## Performance Best Practices

### Efficient Patterns

```bash
# Good: Use built-in parameter expansion
filename="${path##*/}"      # basename
dirname="${path%/*}"        # dirname
extension="${filename##*.}" # get extension

# Bad: Unnecessary external commands
filename="$(basename "$path")"

# Good: Use bash arrays
files=()
while IFS= read -r file; do
    files+=("$file")
done < <(find . -name "*.sh")

# Bad: Word splitting issues
files=$(find . -name "*.sh")

# Good: Use [[ ]] for tests (bash builtin)
if [[ -f "$file" && -r "$file" ]]; then
    echo "File exists and is readable"
fi

# Bad: Use [ ] (external command)
if [ -f "$file" -a -r "$file" ]; then
    echo "File exists and is readable"
fi
```

### Parallel Execution

For processing multiple items:

```bash
# Process items in parallel
process_item() {
    local item="$1"
    # Do work on item
}

export -f process_item

# Use GNU parallel if available
if command_exists parallel; then
    printf '%s\n' "${items[@]}" | parallel -j 4 process_item
else
    # Fallback: background jobs
    for item in "${items[@]}"; do
        process_item "${item}" &
    done
    wait
fi
```

### Progress Indicators

```bash
# Show progress for long operations
show_progress() {
    local current=$1
    local total=$2
    local percent=$((current * 100 / total))
    local filled=$((percent / 2))
    local empty=$((50 - filled))
    
    printf "\rProgress: ["
    printf "%${filled}s" | tr ' ' '#'
    printf "%${empty}s" | tr ' ' '-'
    printf "] %d%%" "${percent}"
}

# Usage
total=${#items[@]}
for i in "${!items[@]}"; do
    process_item "${items[$i]}"
    show_progress "$((i + 1))" "${total}"
done
echo # Newline after progress bar
```

## Git Integration

### Pre-commit Hooks

Scripts should pass these checks before commit:

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running pre-commit checks..."

# Check all shell scripts
for script in $(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(sh|bash)$'); do
    echo "Checking ${script}..."
    
    # ShellCheck
    if ! shellcheck "${script}"; then
        echo "ShellCheck failed for ${script}"
        exit 1
    fi
    
    # Syntax check
    if ! bash -n "${script}"; then
        echo "Syntax check failed for ${script}"
        exit 1
    fi
done

# Check Python scripts
for script in $(git diff --cached --name-only --diff-filter=ACM | grep '\.py$'); do
    echo "Checking ${script}..."
    
    # Ruff check
    if command -v ruff >/dev/null 2>&1; then
        if ! ruff check "${script}"; then
            echo "Ruff check failed for ${script}"
            exit 1
        fi
    fi
done

echo "Pre-commit checks passed!"
```

### Commit Message Standards

When committing scripts:

```
<type>(scripts): <brief description>

<detailed description>

Related: #<issue-number>
Quest: <quest-name> (if applicable)

Changes:
- Added: <what was added>
- Modified: <what was changed>
- Fixed: <what was fixed>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

Example:
```
feat(scripts): add Azure deployment automation script

Comprehensive script for deploying Jekyll sites to Azure Static Web Apps
with validation, rollback capabilities, and health checks.

Related: #123
Quest: azure-ascension-01

Changes:
- Added: azure-jekyll-deploy.sh with full deployment workflow
- Added: Configuration validation and prerequisite checking
- Added: Dry-run mode for safe testing
```

## Documentation Requirements

### Script README

Each subdirectory should have a README.md:

```markdown
# Directory Name

Brief description of the scripts in this directory.

## Scripts

### script-name.sh

**Purpose**: Brief description

**Usage**:
```bash
./script-name.sh [OPTIONS] [ARGUMENTS]
```

**Options**:
- `--option1`: Description
- `--option2`: Description

**Examples**:
```bash
# Example 1
./script-name.sh --option1 value

# Example 2
./script-name.sh --option2
```

**Dependencies**: List dependencies

**Tested On**: Platforms tested

## Contributing

When adding scripts to this directory:
1. Follow the script template
2. Include comprehensive help
3. Add examples to this README
4. Test on multiple platforms
```

### Inline Documentation

Use clear comments:

```bash
#######################################
# Function description
# 
# Arguments:
#   $1 - Description of first argument
#   $2 - Description of second argument
# 
# Returns:
#   0 on success, non-zero on error
#
# Globals:
#   GLOBAL_VAR - Description if the function uses/modifies globals
#######################################
function_name() {
    local arg1="$1"
    local arg2="$2"
    
    # Implementation with inline comments for complex logic
}
```

## CI/CD Integration

### GitHub Actions Workflow

Scripts should integrate with CI/CD:

```yaml
name: Script Tests

on:
  push:
    paths:
      - 'scripts/**'
  pull_request:
    paths:
      - 'scripts/**'

jobs:
  test-scripts:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install ShellCheck
        run: sudo apt-get install -y shellcheck
      
      - name: Lint Shell Scripts
        run: |
          for script in scripts/**/*.sh; do
            echo "Checking ${script}..."
            shellcheck "${script}"
          done
      
      - name: Test Script Execution
        run: |
          for script in scripts/**/*.sh; do
            echo "Testing ${script}..."
            bash -n "${script}"
            "${script}" --help || true
          done
```

## AI-Powered Script Generation

### Using the Bash-It Prompt

For generating new scripts, use the `/bash-it` prompt:

```markdown
/bash-it

Context: [Article/Quest/Documentation]
Goal: [What the script should accomplish]
Requirements:
- Requirement 1
- Requirement 2
- Requirement 3

Platforms: macOS, Ubuntu, WSL
Dependencies: git, curl, jq
```

The Bash-It agent will generate:
1. Script architecture blueprint
2. Complete production-ready script
3. Testing checklist
4. Installation documentation
5. Integration examples

### Customizing Generated Scripts

After generation:
1. Review and validate all logic
2. Add IT-Journey specific configurations
3. Update paths and variables
4. Test on target platforms
5. Add to appropriate subdirectory
6. Update README

## Migration and Refactoring

### Upgrading Legacy Scripts

When updating older scripts:

```bash
# Legacy script audit checklist
- [ ] Add comprehensive header
- [ ] Implement strict mode (set -euo pipefail)
- [ ] Add trap handlers for cleanup
- [ ] Implement logging framework
- [ ] Add --help and --version flags
- [ ] Document exit codes
- [ ] Add dependency checking
- [ ] Implement dry-run mode
- [ ] Add verbose mode
- [ ] Add configuration file support
- [ ] Update documentation
- [ ] Add tests
- [ ] Run ShellCheck
```

### Script Consolidation

When multiple scripts do similar things:

1. **Analyze**: Identify common functionality
2. **Design**: Create unified script architecture
3. **Implement**: Build consolidated script
4. **Test**: Verify all original functionality works
5. **Document**: Update READMEs and migration guide
6. **Deprecate**: Mark old scripts as deprecated
7. **Remove**: Delete old scripts after transition period

Example deprecation notice:

```bash
#!/usr/bin/env bash
echo "WARNING: This script is deprecated."
echo "Please use: scripts/core/environment-setup.sh"
echo ""
echo "This script will be removed in version 2.0.0"
echo ""
read -p "Continue with deprecated script? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi
```

## Maintenance and Monitoring

### Regular Maintenance Tasks

Monthly:
- [ ] Run ShellCheck on all scripts
- [ ] Check for broken dependencies
- [ ] Update documentation
- [ ] Review and close deprecated scripts
- [ ] Test on latest OS versions

Quarterly:
- [ ] Security audit
- [ ] Performance review
- [ ] Update dependencies
- [ ] Refactor complex scripts
- [ ] Review and consolidate similar scripts

### Health Checks

```bash
# scripts/health-check.sh
#!/usr/bin/env bash
# Verify all scripts meet standards

echo "Checking scripts health..."

for script in scripts/**/*.sh; do
    echo "Checking ${script}..."
    
    # Check shebang
    if ! head -1 "${script}" | grep -q '^#!/'; then
        echo "  ❌ Missing shebang"
    fi
    
    # Check strict mode
    if ! grep -q 'set -euo pipefail' "${script}"; then
        echo "  ⚠️  Missing strict mode"
    fi
    
    # Check help function
    if ! grep -q '\-\-help' "${script}"; then
        echo "  ⚠️  Missing help function"
    fi
    
    # ShellCheck
    if ! shellcheck "${script}" 2>/dev/null; then
        echo "  ❌ ShellCheck failed"
    fi
done
```

## Contributing New Scripts

### Submission Checklist

Before submitting a new script:

- [ ] **Follows Template**: Uses the standard script header and structure
- [ ] **Documentation**: Includes comprehensive help and examples
- [ ] **Testing**: Passes all linting and functionality tests
- [ ] **Security**: No hardcoded secrets, proper input validation
- [ ] **Cross-Platform**: Tested on macOS and Linux (where applicable)
- [ ] **Dependencies**: All dependencies documented and checked
- [ ] **README**: Added to appropriate README.md
- [ ] **Logging**: Implements standard logging framework
- [ ] **Error Handling**: Proper exit codes and error messages
- [ ] **Cleanup**: Trap handlers and resource cleanup
- [ ] **Version**: Version 1.0.0 for new scripts
- [ ] **Author**: Proper attribution in header

### PR Description Template

```markdown
## Script Addition: [Script Name]

### Purpose
Brief description of what the script does and why it's needed.

### Category
- [ ] Core
- [ ] Deployment
- [ ] Development
- [ ] Monitoring

### Testing
- [ ] Tested on macOS
- [ ] Tested on Ubuntu
- [ ] Tested on WSL
- [ ] ShellCheck passed
- [ ] Dry-run mode verified
- [ ] Help documentation complete

### Related
- Quest: [Quest name if applicable]
- Issue: #[Issue number]
- Documentation: [Link to docs]

### Examples
```bash
# Example 1
./script-name.sh --option1

# Example 2
./script-name.sh --option2 --verbose
```

### Checklist
- [ ] Follows script template
- [ ] Includes comprehensive header
- [ ] Implements strict mode
- [ ] Has --help and --version flags
- [ ] Includes logging framework
- [ ] Has trap handlers for cleanup
- [ ] Documented in README
- [ ] No hardcoded secrets
- [ ] Input validation implemented
- [ ] Tests included or tested manually
```

## Related Resources

### IT-Journey Resources
- [Bash-It Prompt](../.github/prompts/bash-it.prompt.md) - AI script generation agent
- [Core Instructions](./core.instructions.md) - Universal development principles
- [Bash Instructions](../../bamr87/.github/instructions/bash.instructions.md) - Comprehensive bash guide
- [Scripts README](../../scripts/README.md) - Scripts directory documentation

### External Resources
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [ShellCheck Wiki](https://github.com/koalaman/shellcheck/wiki)
- [Bash Hackers Wiki](https://wiki.bash-hackers.org/)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
- [BATS Testing Framework](https://github.com/bats-core/bats-core)

## IT-Journey Development Principles Applied

These scripts embody IT-Journey's core principles:

- **DFF (Design for Failure)**: Comprehensive error handling and validation
- **DRY (Don't Repeat Yourself)**: Reusable utility functions and templates
- **KIS (Keep It Simple)**: Clear, readable code with minimal complexity
- **REnO (Release Early and Often)**: Version management and continuous improvement
- **MVP (Minimum Viable Product)**: Start simple, add features based on needs
- **COLAB (Collaboration)**: Consistent patterns enable team contribution
- **AIPD (AI-Powered Development)**: Leverage Bash-It for script generation

## Questions and Support

- **Script Issues**: Open an issue with the `scripts` label
- **Feature Requests**: Describe the automation need in an issue
- **Contributions**: Follow the submission checklist above
- **Questions**: Check existing scripts for examples or ask in discussions

---

**Remember**: Good scripts are reliable, maintainable, and self-documenting. Follow these standards to create automation that others (including future you) will appreciate! 🚀

