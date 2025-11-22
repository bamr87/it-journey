# Scripts Instructions Summary

## Overview

A comprehensive instructions file has been created to establish standards and best practices for all scripts in the IT-Journey repository.

## Files Created

### Primary File
**Location**: `.github/instructions/scripts.instructions.md`

**Purpose**: Comprehensive standards and best practices for scripts directory

**Front Matter**:
```yaml
---
applyTo: 'scripts/**/*'
---
```

This ensures AI agents automatically apply these instructions when working with any file in the `scripts/` directory.

## Key Sections Covered

### 1. Directory Structure & Organization
- **Core Scripts** (`core/`) - Environment setup and system management
- **Deployment Scripts** (`deployment/`) - Production deployment automation
- **Development Scripts** (`development/`) - Developer workflow tools
- **Monitoring Scripts** - Health checks and link validation

### 2. Universal Script Standards

#### Mandatory Components
- ✅ Comprehensive header with metadata
- ✅ Strict error handling (`set -euo pipefail`)
- ✅ Logging framework (debug, info, warn, error, fatal)
- ✅ Help and version flags
- ✅ Cleanup and trap handlers
- ✅ Dependency validation
- ✅ Dry-run mode support
- ✅ Verbose mode support
- ✅ Configuration file support

#### Script Template Structure
1. Shebang and metadata header
2. Strict mode and safety settings
3. Global variables and configuration
4. Logging and output functions
5. Cleanup and error handling
6. Utility and helper functions
7. Configuration management
8. Argument parsing
9. Environment validation
10. Core logic implementation
11. Main function and entry point

### 3. Security Standards

Comprehensive security guidelines including:
- **Secrets Management**: Never hardcode credentials
- **Input Sanitization**: Validate all user input
- **Safe File Operations**: Use mktemp, atomic writes, proper permissions
- **Path Validation**: Prevent directory traversal attacks

Examples provided for:
- Environment variable usage
- Configuration file handling
- Secrets file with permission checking
- Input validation patterns
- Filename sanitization
- Path validation

### 4. Python Scripts Standards

Separate standards for Python scripts with:
- Standard script structure template
- Type hints and docstrings
- Argparse for CLI arguments
- Proper logging setup
- Exception handling
- PEP 8 compliance

### 5. Testing Requirements

#### Comprehensive Testing Checklist
- **Syntax & Linting**: ShellCheck, bash -n, checkbashisms, pylint/ruff
- **Functionality**: All flags and modes tested
- **Platform Compatibility**: macOS, Linux, WSL
- **Security Review**: No secrets, proper validation, safe operations
- **Documentation**: Complete headers and README updates

#### Automated Testing
- BATS (Bash Automated Testing System) examples
- Unit test templates
- Test execution instructions

### 6. Performance Best Practices

- **Efficient Patterns**: Use bash builtins over external commands
- **Parallel Execution**: GNU parallel and background jobs
- **Progress Indicators**: User-friendly progress bars
- **Resource Management**: Proper cleanup and optimization

### 7. Git Integration

- **Pre-commit Hooks**: Automated validation before commits
- **Commit Message Standards**: Structured commit messages with types
- **Branch Naming**: Consistent naming conventions

### 8. Documentation Requirements

- **Script README Templates**: Standardized documentation format
- **Inline Documentation**: Function comment standards
- **Usage Examples**: Multiple examples for each script

### 9. CI/CD Integration

- **GitHub Actions Workflows**: Automated testing on push/PR
- **Continuous Validation**: ShellCheck and syntax checking
- **Test Execution**: Automated test runs

### 10. AI-Powered Script Generation

Integration with the **Bash-It prompt** for automated script generation:
- Reference to `/bash-it` command
- Blueprint generation workflow
- Customization guidelines
- Post-generation validation

### 11. Migration and Refactoring

- **Legacy Script Audit**: Checklist for upgrading old scripts
- **Script Consolidation**: Process for merging similar scripts
- **Deprecation Process**: How to phase out old scripts

### 12. Maintenance and Monitoring

- **Regular Maintenance Tasks**: Monthly and quarterly schedules
- **Health Check Scripts**: Automated validation tools
- **Update Procedures**: When and how to update scripts

### 13. Contributing Guidelines

Comprehensive checklist for new script submissions:
- Template compliance
- Documentation requirements
- Testing verification
- Security validation
- Cross-platform testing
- PR description template

## Related Files Updated

### 1. Instructions README
**File**: `.github/instructions/README.md`

**Changes**:
- Added `scripts.instructions.md` to the instruction files table
- Updated "Last Updated" date to 2025-11-18
- Documented target audience: "Script developers and automation engineers"

### 2. Scripts Directory README
**File**: `scripts/README.md`

**Changes**:
- Added link to new scripts instructions at top of Related Documentation
- Provides easy access for developers working in scripts directory

## How to Use These Instructions

### For Script Developers

1. **Creating New Scripts**:
   - Reference the script template in the instructions
   - Follow the mandatory components checklist
   - Use the testing checklist before committing

2. **Using AI Assistance**:
   - Invoke `/bash-it` with your requirements
   - AI will automatically apply `scripts.instructions.md` when working in `scripts/`
   - Review and customize generated scripts

3. **Updating Existing Scripts**:
   - Use the legacy script audit checklist
   - Apply security standards
   - Add missing mandatory components

### For AI Agents

When users work on files in `scripts/**/*`:
1. Automatically load `scripts.instructions.md`
2. Apply the standards and patterns
3. Validate against the comprehensive checklists
4. Suggest improvements based on best practices

### For Code Reviewers

Use the instructions to verify:
- Script follows the template
- All mandatory components present
- Security standards met
- Testing completed
- Documentation updated

## Benefits

### Consistency
- All scripts follow the same patterns
- Predictable structure and behavior
- Easier to maintain and debug

### Quality
- Comprehensive error handling
- Security built-in from the start
- Proper testing and validation

### Maintainability
- Self-documenting code
- Clear upgrade paths
- Consistent logging and debugging

### Collaboration
- New contributors can follow clear guidelines
- AI agents provide consistent assistance
- Code reviews are more efficient

### Educational Value
- Scripts serve as learning examples
- Best practices are documented
- Security patterns are demonstrated

## Integration with IT-Journey Principles

The instructions embody IT-Journey's core development principles:

- **DFF (Design for Failure)**: Comprehensive error handling and validation
- **DRY (Don't Repeat Yourself)**: Reusable utility functions and templates
- **KIS (Keep It Simple)**: Clear, readable code with minimal complexity
- **REnO (Release Early and Often)**: Version management and continuous improvement
- **MVP (Minimum Viable Product)**: Start simple, add features based on needs
- **COLAB (Collaboration)**: Consistent patterns enable team contribution
- **AIPD (AI-Powered Development)**: Leverage Bash-It for script generation

## Next Steps

1. **Review the Instructions**: Read through `scripts.instructions.md` to understand all standards

2. **Audit Existing Scripts**: Use the legacy script audit checklist to identify scripts needing updates

3. **Apply Standards Gradually**: Update scripts as you work on them, don't try to update everything at once

4. **Use for New Scripts**: Apply the template and standards to all new script development

5. **Provide Feedback**: If you find areas for improvement, open an issue or PR

6. **Share with Team**: Ensure all script developers are aware of the new standards

## Resources

### Internal
- [Scripts Instructions](./scripts.instructions.md) - Full instructions document
- [Bash-It Prompt](../.github/prompts/bash-it.prompt.md) - AI script generation
- [Core Instructions](./core.instructions.md) - Universal development principles
- [Scripts README](../../scripts/README.md) - Scripts directory documentation

### External
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [ShellCheck](https://github.com/koalaman/shellcheck)
- [BATS Testing](https://github.com/bats-core/bats-core)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)

## Questions and Feedback

- **Script Questions**: Open an issue with the `scripts` label
- **Standards Feedback**: Suggest improvements via PR to `scripts.instructions.md`
- **AI Assistance Issues**: Tag issues with `ai-assistance` label
- **General Discussion**: Use GitHub Discussions

---

**Created**: 2025-11-18  
**Author**: IT-Journey AI Assistant (Bash-It)  
**Purpose**: Document the creation and usage of comprehensive scripts standards



