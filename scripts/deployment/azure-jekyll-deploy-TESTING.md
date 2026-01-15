## Testing Checklist

### Syntax Validation
- [ ] ShellCheck analysis: `shellcheck scripts/deployment/azure-jekyll-deploy.sh`
- [ ] Bash syntax check: `bash -n scripts/deployment/azure-jekyll-deploy.sh`
- [ ] POSIX compliance: `checkbashisms scripts/deployment/azure-jekyll-deploy.sh` (if POSIX required)

### Functionality Tests
- [ ] Help display: `./scripts/deployment/azure-jekyll-deploy.sh --help`
- [ ] Version display: `./scripts/deployment/azure-jekyll-deploy.sh --version`
- [ ] Dry-run mode: `./scripts/deployment/azure-jekyll-deploy.sh --dry-run --verbose setup`
- [ ] Verbose mode: `./scripts/deployment/azure-jekyll-deploy.sh --verbose --dry-run`
- [ ] Invalid arguments: `./scripts/deployment/azure-jekyll-deploy.sh --invalid-option`
- [ ] Core functionality with valid inputs (dry-run mode)
- [ ] Error handling with invalid inputs
- [ ] Cleanup on normal exit
- [ ] Cleanup on interrupted execution (CTRL+C)

### Platform Testing
- [ ] Linux (Ubuntu 20.04+)
- [ ] Linux (RHEL/CentOS/Rocky 8+)
- [ ] macOS (12.0+)
- [ ] WSL2 (Ubuntu)

### Security Review
- [ ] No hardcoded credentials
- [ ] Safe temp file handling
- [ ] Proper file permissions
- [ ] Input sanitization
- [ ] Command injection protection
- [ ] Path traversal protection

### Integration Tests
- [ ] Azure CLI integration (mocked in dry-run)
- [ ] GitHub CLI integration (mocked in dry-run)
- [ ] Jekyll build integration
- [ ] Configuration file loading
- [ ] Environment variable handling

### Performance & Edge Cases
- [ ] Empty input handling
- [ ] Large repository handling
- [ ] Network failure resilience
- [ ] Disk space exhaustion handling
- [ ] Concurrent execution (if applicable)
- [ ] Idempotency verification
- [ ] Long-running operation interruption

### Command-Specific Tests
- [ ] `setup` command creates resource group and configures Jekyll
- [ ] `deploy` command performs full deployment pipeline
- [ ] `configure` command updates Jekyll config only
- [ ] `azure-create` command creates Azure resources only
- [ ] `github-workflow` command sets up CI/CD only
- [ ] `domain-setup` command configures custom domain
- [ ] `cleanup` command removes Azure resources

### Configuration Tests
- [ ] Default configuration loading
- [ ] Custom config file loading
- [ ] Environment variable override
- [ ] Command-line argument precedence
- [ ] Configuration validation
- [ ] Invalid configuration handling

### Logging Tests
- [ ] Log file creation in correct location
- [ ] Verbose logging captures debug information
- [ ] Quiet mode suppresses non-error output
- [ ] Log rotation and cleanup
- [ ] Error logging captures stack traces
- [ ] Log format consistency

### Error Recovery Tests
- [ ] Azure login failure handling
- [ ] Resource creation failure rollback
- [ ] GitHub API failure handling
- [ ] Jekyll build failure recovery
- [ ] Network timeout handling
- [ ] Permission denied error handling