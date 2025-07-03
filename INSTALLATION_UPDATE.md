# zer0-mistakes Theme Installation Update

## Summary of Changes

I've successfully updated both the `zer0.md` build instructions and the `install.sh` script to provide a simplified, streamlined installation process that's optimized for Azure Static Web Apps deployment.

## Key Improvements

### 1. Simplified Installation in zer0.md

**Before**: Complex manual setup with multiple shell commands creating directories, configuration files, and Azure workflows.

**After**: Single command installation that handles everything automatically:

```bash
# Navigate to your repository directory
cd $ZREPO

# Download and run the zer0-mistakes theme installer directly from GitHub
curl -fsSL https://raw.githubusercontent.com/bamr87/zer0-mistakes/main/install.sh | bash
```

### 2. Enhanced install.sh Script Features

- **Remote Installation**: Can be downloaded and executed directly from GitHub
- **Azure Static Web Apps Ready**: Automatically creates Azure deployment workflow
- **Comprehensive Error Handling**: Color-coded output with detailed error messages
- **Build Directory**: Creates `build/` directory for logs and temporary files
- **Automatic Cleanup**: Cleans up temporary files after remote installation

### 3. Azure Static Web Apps Optimization

The installation now creates the optimal directory structure for Azure Static Web Apps:

- **App Location**: Root directory (`.`) - Contains Jekyll source files
- **API Location**: `api/` directory - For Azure Functions (optional)
- **Output Location**: `_site/` directory - Jekyll build output

### 4. Pre-configured GitHub Actions

Automatically creates `.github/workflows/azure-static-web-apps.yml` with:

- Ruby setup and Jekyll build process
- Azure Static Web Apps deployment configuration
- Pull request preview deployments
- Automated cleanup on PR close

## Installation Options

### Option 1: Direct Remote Installation (Recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/bamr87/zer0-mistakes/main/install.sh | bash
```

### Option 2: Clone and Install
```bash
git clone https://github.com/bamr87/zer0-mistakes.git temp-theme
./temp-theme/install.sh .
rm -rf temp-theme
```

### Option 3: Local Installation (if you have the repo locally)
```bash
./install.sh /path/to/target/directory
```

## What Gets Installed

- **Configuration**: `_config.yml`, `_config_dev.yml`, `frontmatter.json`
- **Dependencies**: `Gemfile`, `Rakefile`, `package.json`
- **Docker**: `docker-compose.yml`, `Dockerfile`
- **Theme Structure**: `_data/`, `_sass/`, `_includes/`, `_layouts/`, `assets/`
- **Static Files**: `404.html`, `favicon.ico`, `index.md` (if not exists)
- **Development Tools**: `.gitignore`, `INSTALLATION.md`
- **Azure Integration**: `.github/workflows/azure-static-web-apps.yml`
- **Build System**: `build/` directory with logs

## Next Steps After Installation

1. **Start Development**:
   ```bash
   docker-compose up
   # OR
   bundle install && bundle exec jekyll serve --config _config_dev.yml
   ```

2. **Azure Deployment**:
   - Create Azure Static Web App in Azure portal
   - Add `AZURE_STATIC_WEB_APPS_API_TOKEN` to GitHub repository secrets
   - Push to `main` branch to trigger deployment

3. **Customization**:
   - Edit `_config.yml` for site settings
   - Update `index.md` for homepage content
   - Add content to `pages/` directory
   - Customize styles in `_sass/custom.scss`

## Benefits

- **Faster Setup**: From complex multi-step process to single command
- **Azure Ready**: Pre-configured for Azure Static Web Apps deployment
- **Error Resilient**: Comprehensive error handling and validation
- **Documentation**: Automatic creation of setup and usage documentation
- **Flexible**: Works with both local and remote installation scenarios

This update follows all the IT-Journey principles:
- **Keep It Simple (KIS)**: Single command replaces complex setup
- **Don't Repeat Yourself (DRY)**: Reusable script for all installations
- **Design for Failure (DFF)**: Comprehensive error handling and validation
- **Collaboration (COLAB)**: Clear documentation and consistent standards
