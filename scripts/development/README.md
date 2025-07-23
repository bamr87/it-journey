# Development Scripts

Scripts specifically for development workflows, content creation, and testing.

## Directory Structure

- `build/` - Build automation and compilation scripts
- `content/` - Content processing and transformation tools  
- `testing/` - Testing utilities and CI/CD scripts

## Build Scripts (`build/`)

### `build-site.sh`
Unified build script supporting multiple project types with intelligent detection.

**Features:**
- Auto-detection of Jekyll, Node.js, and Docker projects
- Environment-specific builds (development/production)
- Clean build capabilities
- Development server integration
- Build validation and reporting

**Usage:**
```bash
# Auto-detect and build for development
./build-site.sh

# Production Jekyll build
./build-site.sh --type jekyll --env production

# Clean build with development server
./build-site.sh --clean --serve
```

### `create-dockerfile.sh`
Generates Docker configuration files for different project types.

### `create-gemfile.sh`
Creates Ruby Gemfile with IT-Journey standard dependencies.

## Content Scripts (`content/`)

### `jupyter-to-markdown.sh`
Converts Jupyter notebooks to Jekyll-compatible markdown files.

**Features:**
- Preserves code cells and output
- Generates frontmatter headers
- Handles image attachments
- Maintains notebook structure

### `append_feature.py`
Python script for adding features and content to markdown files.

## Testing Scripts (`testing/`)

### `cibuild`
Continuous integration build script for automated testing.

**Features:**
- Jekyll build validation
- Link checking
- Performance testing
- Error reporting

## Integration

Development scripts work together to provide a complete development workflow:

1. **Setup** → Use core environment setup
2. **Build** → Use build-site.sh for compilation  
3. **Test** → Use testing scripts for validation
4. **Content** → Use content tools for processing

## Configuration

Scripts respect standard project configurations:

- `_config.yml` / `_config_dev.yml` for Jekyll
- `package.json` for Node.js projects
- `Gemfile` for Ruby projects
- `Dockerfile` for containerized builds
