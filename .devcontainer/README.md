# IT-Journey DevContainer Setup

This DevContainer configuration provides a complete Jekyll development environment for the IT-Journey project, optimized for educational content creation and AI-assisted development.

## 🚀 Features

- **Ruby 3.2** - Matches production CI/CD environment
- **Node.js 20** - For modern JavaScript tooling
- **Jekyll & Bundle** - Pre-installed with optimized caching
- **VS Code Extensions** - Essential extensions for Jekyll, Markdown, and AI-assisted development
- **Port Forwarding** - Automatic forwarding for Jekyll servers (4000, 4002) and LiveReload (35729)
- **Front Matter CMS** - Integrated content management for educational posts
- **Docker Integration** - Can run alongside existing docker-compose setup

## 🛠️ VS Code Extensions Included

### Core Development

- **Ruby LSP** - Ruby language server for syntax highlighting and IntelliSense
- **YAML Support** - For Jekyll configuration files
- **JSON Support** - For configuration and data files

### Content Creation

- **Markdown All in One** - Enhanced Markdown editing with ToC, preview, and shortcuts
- **Markdown Lint** - Consistent Markdown formatting
- **Markdown Table** - Easy table creation and formatting
- **Front Matter CMS** - Visual content management for Jekyll posts

### AI & Productivity

- **GitHub Copilot** - AI-powered code completion
- **GitHub Copilot Chat** - AI assistance for development questions
- **Todo Tree** - Track TODOs and FIXMEs in code
- **Docker** - Docker container management

## 🔧 Environment Configuration

The devcontainer includes optimized settings for Jekyll development:

- **Liquid Template Support** - HTML files are treated as Liquid templates
- **Jekyll File Associations** - Proper syntax highlighting for Jekyll files
- **Optimized File Watching** - Excludes Jekyll build directories for better performance
- **Markdown Settings** - Configured for educational content writing

## 📚 Getting Started

1. **Open in DevContainer**
   - Open VS Code in the IT-Journey repository
   - Command Palette: "Dev Containers: Reopen in Container"
   - Wait for container build and setup

2. **Start Jekyll Development**

   ```bash
   # Using the existing docker-compose tasks (recommended)
   # Use VS Code Task: "Jekyll: Serve with Docker"
   
   # Or start Jekyll directly in the devcontainer
   bundle exec jekyll serve --config "_config.yml,_config_dev.yml" --host 0.0.0.0 --port 4000
   ```

3. **Create Educational Content**

   - Use Front Matter CMS dashboard (opens automatically)
   - Create new posts in `pages/_posts/`
   - Follow IT-Journey front matter standards for educational content

## 🔀 Integration with Existing Docker Setup

This devcontainer works alongside the existing `docker-compose.yml`:

- **DevContainer**: Provides full development environment with VS Code integration
- **Docker Compose**: Runs Jekyll server with hot reload for testing
- **Ports**: Both setups use the same port configuration (4000, 4002, 35729)

You can use both simultaneously:

- DevContainer for code editing, debugging, and AI assistance
- Docker Compose for serving the Jekyll site during development

## 🚀 Performance Optimizations

- **Bundle Caching** - Gems are cached in a Docker volume for faster rebuilds
- **File Watching** - Optimized exclusions for Jekyll build directories
- **Network Mode** - Uses host networking for seamless port access
- **Lazy Loading** - Extensions load on-demand for faster startup

## 🔍 Troubleshooting

### Container Won't Start

```bash
# Rebuild the devcontainer
# Command Palette: "Dev Containers: Rebuild Container"
```

### Gem Installation Issues

```bash
# Clear bundle cache and reinstall
rm -rf .bundle
bundle install
```

### Port Conflicts

```bash
# Check if ports are already in use
netstat -tlnp | grep -E ':(4000|4002|35729)'

# Stop existing Jekyll processes
docker-compose down
pkill -f jekyll
```

### Performance Issues

```bash
# Clear Jekyll caches
bundle exec jekyll clean

# Clear all caches and rebuild
rm -rf _site .jekyll-cache .sass-cache
bundle exec jekyll build
```

## 📖 Educational Content Guidelines

When creating content in this environment:

1. **Use Front Matter Standards** - Include comprehensive metadata for AI assistance
2. **Follow IT-Journey Principles** - Design for Failure, Keep It Simple, AI-Powered Development
3. **Test Cross-Platform** - Use both devcontainer and docker-compose for validation
4. **Document Learning Paths** - Connect new content to existing educational journeys

## 🤖 AI Integration

This devcontainer is optimized for AI-assisted development:

- **Copilot Integration** - Enhanced code completion for Jekyll and Liquid templates
- **Front Matter Support** - Structured metadata for AI content understanding
- **Educational Context** - AI agents understand learning objectives and technical requirements
- **Workflow Automation** - AI can assist with content creation, validation, and deployment

For more information about AI-assisted development practices, see the [Copilot Instructions](.github/copilot-instructions.md).
