# IT-Journey

[![pages-build-deployment](https://github.com/bamr87/it-journey/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/bamr87/it-journey/actions/workflows/pages/pages-build-deployment)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Your comprehensive learning platform for mastering IT skills through gamified quests, hands-on tutorials, and interactive notebooks.

**🌐 Live Site:** [https://it-journey.dev](https://it-journey.dev)

## 📖 Overview

IT-Journey is an open-source educational platform that transforms technical learning into an engaging adventure. Built on Jekyll and GitHub Pages, it combines:

- **53+ Gamified Quests** with binary-level progression
- **84+ Tutorial Posts** covering practical IT skills  
- **6+ Interactive Notebooks** for hands-on experimentation
- **Automated Quality Assurance** with AI-powered link monitoring
- **Multi-platform Support** (macOS, Windows, Linux)

Whether you're starting from zero or advancing your expertise, IT-Journey provides structured learning paths with real-world applications.

## ⚡ Quick Start

### Prerequisites

- **Git** - Version control system
- **Ruby 2.6+** - Jekyll runtime environment
- **Bundler** - Ruby gem manager
- **Docker** (optional) - For containerized development

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bamr87/it-journey.git
   cd it-journey
   ```

2. **Install dependencies:**
   ```bash
   bundle install
   ```

3. **Run locally:**
   ```bash
   bundle exec jekyll serve
   ```

4. **Access the site:**
   Open [http://localhost:4000](http://localhost:4000) in your browser

### Docker Setup (Alternative)

```bash
docker-compose up
```

## 📚 Learning Paths

### 🌱 Beginner Path
Start your IT journey from scratch:
- **[Zero to Hero Guide](zer0.md)** - Complete setup from scratch
- **Foundation Quests** - Binary levels 0000-0111
- **Basic Tutorials** - Command-line and development basics

### 🚀 Intermediate Path
Build practical skills:
- **Automation Projects** - GitHub Actions, scripting
- **Web Development** - Jekyll, frontend/backend basics
- **DevOps Fundamentals** - CI/CD, containerization

### 🏆 Advanced Path
Master professional practices:
- **Create Content** - Write quests and tutorials
- **Contribute Code** - Improve platform features
- **Mentor Others** - Support the learning community

## 📂 Project Structure

```
it-journey/
├── pages/
│   ├── _quests/          # 53+ gamified learning quests
│   ├── _posts/           # 84+ tutorial articles
│   ├── _notebooks/       # 6+ Jupyter notebooks
│   └── _about/           # Platform documentation
├── scripts/              # Automation tools
│   ├── link-checker.py   # AI-powered link validation
│   └── zer0-to-hero-complete.sh
├── test/                 # Testing frameworks
│   ├── hyperlink-guardian/  # Link health monitoring
│   └── quest-validator/     # Quest quality validation
├── .github/
│   ├── workflows/        # GitHub Actions CI/CD
│   └── instructions/     # AI Copilot guidelines
├── _config.yml           # Jekyll configuration
├── Gemfile               # Ruby dependencies
└── docker-compose.yml    # Container setup
```

## 🎯 Key Features

### Educational Content
- **Binary-Coded Quest Levels** - Technical progression system (0000-1111+)
- **Fantasy-Themed Learning** - RPG narratives make concepts memorable
- **Multi-Platform Guides** - Instructions for macOS, Windows, Linux
- **Real-World Projects** - Portfolio-worthy applications

### Platform Capabilities
- **Static Site Generation** - Fast, secure Jekyll-based platform
- **GitHub Pages Hosting** - Free, reliable deployment
- **Automated Testing** - Link validation and content quality checks
- **AI Integration** - GPT-4 powered analysis and recommendations
- **Docker Support** - Consistent development environments

## 🛠️ Tech Stack

### Core Technologies
- **[Jekyll 3.9+](https://jekyllrb.com/)** - Static site generator
- **[Ruby 2.6+](https://www.ruby-lang.org/)** - Programming language
- **[Bootstrap 5](https://getbootstrap.com/)** - CSS framework
- **[GitHub Pages](https://pages.github.com/)** - Hosting platform
- **[GitHub Actions](https://github.com/features/actions)** - CI/CD automation

### Development Tools
- **Docker** - Containerized environments
- **Bundler** - Ruby dependency management
- **Make** - Build automation
- **Python 3.8+** - Testing and validation scripts

### AI Integration
- **OpenAI GPT-4** - Intelligent analysis and recommendations
- **Custom automation** - Link validation and content quality

## 🤝 Contributing

Contributions are welcome! Whether you're fixing typos, adding content, or building features:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-contribution`)
3. **Make your changes**
4. **Test thoroughly** (run `bundle exec jekyll serve` locally)
5. **Commit with clear messages** (`git commit -m 'Add amazing feature'`)
6. **Push to your fork** (`git push origin feature/amazing-contribution`)
7. **Open a Pull Request**

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines and development standards.

### Ways to Contribute
- 📝 Write tutorials, quests, or documentation
- 🐛 Report bugs or suggest improvements
- 🔧 Improve automation and testing tools
- 🎨 Enhance design and user experience
- 💬 Help others in discussions and issues

## 📞 Support & Community

- **Issues:** [GitHub Issues](https://github.com/bamr87/it-journey/issues) for bug reports and feature requests
- **Discussions:** [GitHub Discussions](https://github.com/bamr87/it-journey/discussions) for questions and community chat
- **Documentation:** Browse [the live site](https://it-journey.dev) for comprehensive guides

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Jekyll](https://jekyllrb.com/) and hosted on [GitHub Pages](https://pages.github.com/)
- Uses the [zer0-mistakes](https://github.com/bamr87/zer0-mistakes) theme
- Powered by the open-source community

---

**Ready to start?** Check out the [Zero to Hero Guide](zer0.md) or browse [Learning Quests](pages/_quests/) to begin your IT journey! 🚀
