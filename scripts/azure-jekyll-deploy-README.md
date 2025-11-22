## Installation

### Quick Install
```bash
# Clone or navigate to the IT-Journey repository
cd /path/to/it-journey

# Make script executable (already done)
chmod +x scripts/azure-jekyll-deploy.sh

# Optional: Create symlink for global access
sudo ln -sf $(pwd)/scripts/azure-jekyll-deploy.sh /usr/local/bin/azure-jekyll-deploy

# Verify installation
azure-jekyll-deploy --version
```

### Dependencies Installation

#### Azure CLI
**macOS (Homebrew):**
```bash
brew update
brew install azure-cli
```

**Ubuntu/Debian:**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**RHEL/CentOS/Rocky:**
```bash
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo dnf install -y https://packages.microsoft.com/config/rhel/8/packages-microsoft-prod.rpm
sudo dnf install -y azure-cli
```

**WSL2:**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

#### GitHub CLI (Optional, for automated secret setup)
```bash
# macOS
brew install gh

# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

#### Jekyll Dependencies (if not already installed)
```bash
# Install Ruby (if not present)
# macOS
brew install ruby

# Ubuntu/Debian
sudo apt install ruby-full build-essential

# Install Jekyll
gem install bundler jekyll
```

### Configuration
Create a configuration file at `~/.azure-jekyll-deploy.conf`:

```bash
# Azure Configuration
AZURE_SUBSCRIPTION="your-subscription-id"
AZURE_RESOURCE_GROUP="jekyll-citadel-rg"
AZURE_LOCATION="EastUS"
AZURE_APP_NAME="your-jekyll-site-name"

# GitHub Configuration
GITHUB_REPO="https://github.com/yourusername/your-jekyll-repo"
GITHUB_TOKEN="your-github-personal-access-token"

# Domain Configuration (optional)
CUSTOM_DOMAIN="www.yourdomain.com"

# Jekyll Configuration
JEKYLL_SOURCE_DIR="."
```

**Security Note:** Store sensitive values like `GITHUB_TOKEN` securely. Consider using a password manager or environment variables for production use.

## Usage Examples

### Example 1: Interactive Setup and Deployment
```bash
# Start with basic setup
./scripts/azure-jekyll-deploy.sh setup

# Then perform full deployment (will prompt for configuration)
./scripts/azure-jekyll-deploy.sh deploy
```

### Example 2: Automated Deployment with Configuration
```bash
# Deploy with all parameters specified
./scripts/azure-jekyll-deploy.sh deploy \
  --app-name my-awesome-jekyll-site \
  --github-repo https://github.com/myusername/my-jekyll-blog \
  --custom-domain blog.mywebsite.com \
  --verbose
```

### Example 3: Dry-Run to Preview Changes
```bash
# See what would happen without making changes
./scripts/azure-jekyll-deploy.sh --dry-run --verbose deploy \
  --app-name test-site \
  --github-repo https://github.com/user/test-repo
```

### Example 4: Step-by-Step Deployment
```bash
# 1. Configure Jekyll site only
./scripts/azure-jekyll-deploy.sh configure --jekyll-dir ./my-site

# 2. Create Azure resources
./scripts/azure-jekyll-deploy.sh azure-create \
  --app-name my-site \
  --github-repo https://github.com/user/my-site

# 3. Setup CI/CD pipeline
./scripts/azure-jekyll-deploy.sh github-workflow \
  --github-repo https://github.com/user/my-site

# 4. Add custom domain (optional)
./scripts/azure-jekyll-deploy.sh domain-setup \
  --app-name my-site \
  --custom-domain www.mysite.com
```

### Example 5: Non-Interactive Mode
```bash
# Run without prompts (useful for CI/CD)
./scripts/azure-jekyll-deploy.sh --yes deploy \
  --app-name production-site \
  --github-repo https://github.com/org/production-site
```

### Example 6: Cleanup Resources
```bash
# Remove all Azure resources (destructive!)
./scripts/azure-jekyll-deploy.sh cleanup \
  --resource-group jekyll-citadel-rg \
  --force
```

## Integration

### Cron Job for Automated Backups
```bash
# Add to crontab for daily resource checks
0 2 * * * /path/to/it-journey/scripts/azure-jekyll-deploy.sh --quiet azure-create --app-name daily-check
```

### Systemd Service
Create `/etc/systemd/system/azure-jekyll-deploy.service`:

```ini
[Unit]
Description=Azure Jekyll Deploy Service
After=network.target

[Service]
Type=oneshot
ExecStart=/path/to/it-journey/scripts/azure-jekyll-deploy.sh --yes deploy --config /etc/azure-jekyll-deploy.conf
StandardOutput=journal
StandardError=journal
Environment=AZURE_SUBSCRIPTION=your-subscription-id

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable azure-jekyll-deploy.service
sudo systemctl start azure-jekyll-deploy.service
```

### GitHub Actions Integration
```yaml
# .github/workflows/deploy.yml
name: Deploy to Azure
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy Jekyll to Azure
        run: |
          chmod +x scripts/azure-jekyll-deploy.sh
          ./scripts/azure-jekyll-deploy.sh --yes deploy \
            --app-name ${{ secrets.AZURE_APP_NAME }} \
            --github-repo ${{ github.repositoryUrl }} \
            --github-token ${{ secrets.GITHUB_TOKEN }}
        env:
          AZURE_SUBSCRIPTION: ${{ secrets.AZURE_SUBSCRIPTION }}
```

### Docker Integration
```dockerfile
# Dockerfile for containerized deployment
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    ruby-full \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# Install Jekyll
RUN gem install bundler jekyll

# Copy deployment script
COPY scripts/azure-jekyll-deploy.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/azure-jekyll-deploy.sh

# Set working directory
WORKDIR /app

# Default command
CMD ["azure-jekyll-deploy.sh", "--help"]
```

## Maintenance & Updates

### Version Updates
When updating the script:
1. Increment `SCRIPT_VERSION` variable
2. Update `Last Modified` date in header
3. Document changes in CHANGELOG
4. Test all functionality
5. Update documentation if behavior changed

### Logging
- Logs are written to: `${LOG_DIR}/azure-jekyll-deploy_${TIMESTAMP}.log`
- Default location: `/var/log/azure-jekyll-deploy/`
- Log rotation: Configure logrotate for production use

```bash
# /etc/logrotate.d/azure-jekyll-deploy
/var/log/azure-jekyll-deploy/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 0644 root root
}
```

### Monitoring
Set up monitoring for deployment success:

```bash
# Check deployment status
#!/bin/bash
SCRIPT_DIR="/path/to/it-journey/scripts"
LOG_FILE="/var/log/azure-jekyll-deploy/azure-jekyll-deploy_$(date +%Y%m%d).log"

if [ -f "$LOG_FILE" ]; then
    if grep -q "Script completed successfully" "$LOG_FILE"; then
        echo "✅ Deployment successful"
        exit 0
    else
        echo "❌ Deployment failed"
        tail -20 "$LOG_FILE"
        exit 1
    fi
else
    echo "⚠️ No deployment log found for today"
    exit 1
fi
```

### Troubleshooting

#### Common Issues

**1. Azure CLI Login Issues**
```bash
# Force re-login
az logout
az login --use-device-code

# Check account
az account show
az account list
```

**2. GitHub Token Issues**
```bash
# Verify token permissions
gh auth status

# Test repository access
gh repo view yourusername/your-repo
```

**3. Jekyll Build Failures**
```bash
# Test build locally
cd your-jekyll-site
bundle install
bundle exec jekyll build

# Check for missing dependencies
bundle list
```

**4. DNS Propagation Delays**
```bash
# Check domain resolution
nslookup yourdomain.com

# Test Azure endpoint
curl -I https://your-app-name.azurestaticapps.net
```

**5. Permission Issues**
```bash
# Check Azure permissions
az role assignment list --assignee $(az account show --query user.name -o tsv)

# Verify GitHub permissions
gh repo view yourusername/your-repo --json permissions
```

#### Debug Mode
Enable debug logging: `bash -x scripts/azure-jekyll-deploy.sh --verbose [command]`

#### Recovery Procedures

**Failed Deployment Recovery:**
```bash
# Check logs
tail -f /var/log/azure-jekyll-deploy/azure-jekyll-deploy_*.log

# Manual cleanup if needed
az group delete --name jekyll-citadel-rg --yes

# Retry deployment
./scripts/azure-jekyll-deploy.sh deploy [options]
```

**GitHub Actions Issues:**
```bash
# Check workflow status
gh run list --repo yourusername/your-repo

# View workflow logs
gh run view <run-id> --log
```

## Security Considerations

### Credential Management
- Never hardcode credentials in scripts or config files
- Use Azure Key Vault for production secrets
- Rotate GitHub tokens regularly
- Implement least-privilege access

### Network Security
- Use HTTPS for all Azure endpoints
- Configure Azure Front Door WAF for production sites
- Implement proper CORS policies
- Enable Azure Monitor security alerts

### Compliance
- Review Azure compliance certifications
- Implement data residency requirements
- Configure audit logging
- Regular security assessments

## Performance Optimization

### Build Optimization
```yaml
# Add to Jekyll _config.yml
# Compress HTML output
compress_html:
  clippings: all
  comments: ["<!-- ", " -->"]
  endings: all
  startings: [html, head, body]

# Exclude unnecessary files
exclude:
  - .bundle/
  - .sass-cache/
  - .jekyll-cache/
  - vendor/
  - .github/
```

### Azure Optimization
```bash
# Enable CDN globally
az cdn profile create --name cdn-profile --resource-group rg --sku Standard_Akamai
az cdn endpoint create --name endpoint --profile-name cdn-profile --resource-group rg --origin yoursite.azurestaticapps.net
```

### Monitoring Performance
```bash
# Check Azure metrics
az monitor metrics list --resource /subscriptions/.../Microsoft.Web/staticSites/your-site --metric "Requests"
```

## Contributing
Follow standard bash style guide and submit pull requests with tests.

### Development Setup
```bash
# Clone repository
git clone https://github.com/bamr87/it-journey.git
cd it-journey

# Install development dependencies
gem install bundler
bundle install

# Run tests
bash scripts/azure-jekyll-deploy-TESTING.md  # Follow testing checklist
```

### Code Style
- Use ShellCheck for linting
- Follow Google Shell Style Guide
- Add comprehensive error handling
- Include detailed logging
- Write self-documenting code

## Changelog

### Version 1.0.0 (2025-11-17)
- Initial release
- Complete Azure Static Web Apps deployment automation
- GitHub Actions CI/CD pipeline setup
- Custom domain configuration
- Comprehensive error handling and logging
- Cross-platform compatibility (macOS, Linux, WSL2)
- Dry-run mode for safe testing
- Interactive and non-interactive modes

## Support & Community

**Getting Help:**
- 📖 Check the [Azure Ascension Quest](https://it-journey.dev/quests/level-0082-azure-ascension-jekyll-deployment/)
- 🐛 Report issues via [GitHub Issues](https://github.com/bamr87/it-journey/issues)
- 💬 Join community discussions
- 📧 Contact maintainers

**Related Resources:**
- [Azure Static Web Apps Documentation](https://docs.microsoft.com/azure/static-web-apps/)
- [Jekyll Deployment Guide](https://jekyllrb.com/docs/deployment/)
- [GitHub Actions for Azure](https://github.com/Azure/actions)
- [Azure CLI Documentation](https://docs.microsoft.com/cli/azure/)

---

*This script embodies the Azure Ascension quest, transforming complex cloud deployment into an automated ritual. May your deployments be swift and your sites ever-available!* ⚔️☁️💎