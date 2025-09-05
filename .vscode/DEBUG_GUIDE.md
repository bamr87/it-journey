# IT-Journey Debug Configuration Guide

This guide explains how to use the VS Code debug and task configurations for the IT-Journey Jekyll application.

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed and running
- VS Code with recommended extensions installed
- Basic familiarity with Jekyll

### Starting Development Server

#### Option 1: Using Docker (Recommended)

1. Open VS Code in the IT-Journey project
2. Press `Ctrl/Cmd + Shift + P` and run "Tasks: Run Task"
3. Select "Jekyll: Serve with Docker"
4. Visit `http://localhost:4002` to view your site

#### Option 2: Using Local Ruby/Bundle

1. Ensure Ruby and Bundle are installed locally
2. Run "Bundle: Install Dependencies" task first
3. Run "Jekyll: Serve Local (No Docker)" task
4. Visit `http://localhost:4002` to view your site

## 🛠️ Available Tasks

### Jekyll Development Tasks

- **Jekyll: Serve with Docker** - Start development server in foreground
- **Jekyll: Serve with Docker (Detached)** - Start development server in background
- **Jekyll: Serve Local (No Docker)** - Start without Docker (requires local Ruby)
- **Jekyll: Build Only (Docker)** - Build site without serving (development config)
- **Jekyll: Production Build (Docker)** - Build site for production
- **Jekyll: Clean and Rebuild (Docker)** - Clean and rebuild from scratch

### Docker Management Tasks

- **Jekyll: Stop Docker** - Stop Jekyll containers
- **Docker: View Logs** - View real-time container logs
- **Docker: Rebuild Container** - Force rebuild of Docker container

### Dependency Management Tasks

- **Bundle: Install Dependencies** - Install Ruby gem dependencies
- **Bundle: Update Dependencies** - Update Ruby gem dependencies

## 🐛 Debug Configurations (VS Code Run and Debug Panel)

The following debug configurations are available in the VS Code Run and Debug panel (`Cmd+Shift+D`):

### Available Configurations

1. **Jekyll: Serve with Docker** - Primary development configuration
   - **Type**: node-terminal
   - **Command**: `docker-compose up`
   - **Description**: Starts the Jekyll site using Docker container (Recommended)
   - **Access**: Site will be available at <http://localhost:4002>

2. **Jekyll: Serve Local (Bundle)** - Local Ruby environment
   - **Type**: node-terminal
   - **Command**: `bundle exec jekyll serve --config _config.yml,_config_dev.yml --port 4002 --host 0.0.0.0`
   - **Description**: Runs Jekyll directly using local bundle (requires Ruby setup)
   - **Access**: Site will be available at <http://localhost:4002>

3. **Jekyll: Build Site** - Build only configuration
   - **Type**: node-terminal
   - **Command**: `bundle exec jekyll build --config _config.yml,_config_dev.yml`
   - **Description**: Builds the site without serving (outputs to _site/)

4. **Docker: Stop All Services** - Cleanup configuration
   - **Type**: node-terminal
   - **Command**: `docker-compose down`
   - **Description**: Stops all Docker containers and cleans up

### How to Use Debug Configurations

1. **Open the Run and Debug Panel**: Press `Cmd+Shift+D` or click the debug icon
2. **Select Configuration**: Use the dropdown to choose a configuration
3. **Start**: Click the green play button (▷) or press `F5`
4. **Monitor**: Watch the integrated terminal for progress
5. **Stop**: Use `Ctrl+C` in the terminal or run the stop configuration

## 🐛 Debug Configurations

### Available Launch Configurations

- **Jekyll: Serve with Docker** - Launch Jekyll via Docker Compose
- **Jekyll: Serve Local** - Launch Jekyll locally without Docker
- **Jekyll: Build Site** - Build the Jekyll site
- **Docker: Stop Services** - Stop all Docker services

### Using Debug Configurations

1. Go to the Run and Debug panel (`Ctrl/Cmd + Shift + D`)
2. Select your desired configuration from the dropdown
3. Click the play button or press `F5`

## 📁 File Structure & Settings

### VS Code Configuration Files

- `.vscode/launch.json` - Debug configurations
- `.vscode/tasks.json` - Task definitions
- `.vscode/settings.json` - Jekyll-specific editor settings

### Jekyll Configuration

- `_config.yml` - Main Jekyll configuration
- `_config_dev.yml` - Development overrides
- `docker-compose.yml` - Docker development environment

## 🔧 Configuration Details

### Docker Setup

The Docker configuration:

- Uses `jekyll/jekyll:latest` image
- Serves on port 4002
- Mounts current directory to `/app`
- Uses both config files for development

### Port Configuration

- **Development**: Port 4002 (configured in `_config.yml`)
- **Alternative**: Port 4001 (dg_port for parallel deployments)

### File Watching

VS Code is configured to:

- Exclude Jekyll build directories from file watching
- Auto-save files for live reload
- Format YAML and Liquid templates appropriately

## 🚨 Troubleshooting

### Common Issues

#### Docker Not Starting

1. Check Docker Desktop is running
2. Try "Docker: Rebuild Container" task
3. Check port 4002 isn't already in use

#### Bundle Issues (Local Development)

1. Run "Bundle: Install Dependencies" task
2. Ensure Ruby version matches Gemfile requirements
3. Check for platform-specific gem issues

#### Port Conflicts

1. Check if port 4002 is in use: `lsof -i :4002`
2. Kill existing processes or change port in `_config.yml`
3. Restart development server

#### File Changes Not Reflecting

1. Check Jekyll logs for errors
2. Try "Jekyll: Clean and Rebuild (Docker)" task
3. Verify file watching is working (check VS Code settings)

### Logs and Debugging

- Use "Docker: View Logs" task to see Jekyll output
- Check VS Code integrated terminal for task output
- Look for build errors in Jekyll logs

## 🔍 Development Workflow

### Recommended Workflow

1. Start with "Jekyll: Serve with Docker (Detached)"
2. Make changes to files
3. View changes at `http://localhost:4002`
4. Use "Docker: View Logs" if issues occur
5. Stop with "Jekyll: Stop Docker" when done

### File Editing

- Markdown files: Auto-formatted with appropriate line heights
- YAML files: 2-space indentation, auto-completion
- Liquid templates: HTML syntax highlighting with Liquid support
- Auto-save enabled for live reload

### Testing Changes

- Local changes reflect immediately with live reload
- Configuration changes require server restart
- Use "Jekyll: Clean and Rebuild" for major changes

## 📚 Additional Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [IT-Journey Project Structure](../README.md)
- [Contributing Guidelines](../CONTRIBUTING.md)

## 🤝 Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Review Jekyll and Docker logs
3. Check GitHub Issues for similar problems
4. Create a new issue with detailed error information

---

*This configuration enables efficient Jekyll development with both Docker and local environments, providing flexibility for different development preferences and setups.*
