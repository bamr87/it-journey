---
title: "Setting Up Charm & Building a Terminal Interface"
description: "Quickstart guide for installing Charm tools (Gum, Glow) and building a custom terminal dashboard for the IT-Journey repository."
permalink: /quickstart/charm-setup/
tags: [charm, gum, glow, terminal, cli, quickstart]
lastmod: 2025-11-19
---

# Setting Up Charm & Building a Terminal Interface

[Charm](https://charm.sh/) provides a suite of powerful tools to make the command line glamorous. In this quickstart, we'll install the core tools and build a custom "Terminal Dashboard" (a mini-emulator of sorts) to navigate the IT-Journey repository.

## 1. Install the Artifacts

We need two primary tools:
*   **[Gum](https://github.com/charmbracelet/gum)**: For interactive menus and inputs.
*   **[Glow](https://github.com/charmbracelet/glow)**: For rendering Markdown in the terminal.

### macOS (Homebrew)
```bash
brew install gum glow
```

### Windows (Scoop/Winget)
```powershell
scoop install gum glow
# OR
winget install charmbracelet.gum charmbracelet.glow
```

### Linux (Debian/Ubuntu)
```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://repo.charm.sh/apt/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | sudo tee /etc/apt/sources.list.d/charm.list
sudo apt update && sudo apt install gum glow
```

## 2. Build the "IT-Journey" Terminal Interface

We will create a shell script that acts as an interactive dashboard for this repository. This script will allow you to browse quests, view documentation, check statistics, and control Docker containers without leaving your terminal.

The script includes:
- **Dependency checking**: Ensures gum and glow are installed
- **Directory validation**: Confirms you're running from the repository root
- **Error handling**: Graceful handling of missing files or failed operations
- **Interactive menus**: Beautiful TUI for navigation

Create a file named `journey.sh` in the root of your repository:

```bash
touch journey.sh
chmod +x journey.sh
```

Open `journey.sh` and add the following code:

```bash
#!/bin/bash

# IT-Journey Terminal Interface
# Built with Gum & Glow (Charm)

# Check dependencies
if ! command -v gum &> /dev/null; then
    echo "Error: 'gum' is not installed. Please run: brew install gum"
    exit 1
fi

if ! command -v glow &> /dev/null; then
    echo "Error: 'glow' is not installed. Please run: brew install glow"
    exit 1
fi

# Check if we're in the right directory
if [[ ! -f "pages/_quickstart/charm-setup.md" ]]; then
    echo "Error: Please run this script from the IT-Journey repository root directory."
    exit 1
fi

# Styles
HEADER_STYLE='foreground 212 border-foreground 212 border double margin 1 padding "1 2"'

# Main Loop
while true; do
    clear
    
    # Header
    gum style \
        --border double \
        --margin "1" \
        --padding "1 2" \
        --border-foreground 212 \
        "🚀 IT-Journey Terminal Interface" \
        "Browse quests, docs, and manage the repo."

    # Menu
    echo "Choose your destination:"
    CHOICE=$(gum choose \
        "📜 Browse Quests" \
        "📖 Read Quickstarts" \
        "📝 View Posts" \
        "📊 View Statistics" \
        "🐳 Docker Controls" \
        "🚪 Exit")

    case "$CHOICE" in
        "📜 Browse Quests")
            QUEST_FILES=$(find pages/_quests -name "*.md" 2>/dev/null)
            if [[ -z "$QUEST_FILES" ]]; then
                gum style --foreground red "No quest files found."
                gum confirm "Return to menu?" && continue || break
            fi
            QUEST=$(echo "$QUEST_FILES" | gum filter --placeholder "Search quests...")
            if [[ -n "$QUEST" && -f "$QUEST" ]]; then
                glow "$QUEST" -p
            fi
            ;;
            
        "📖 Read Quickstarts")
            DOC_FILES=$(find pages/_quickstart -name "*.md" 2>/dev/null)
            if [[ -z "$DOC_FILES" ]]; then
                gum style --foreground red "No quickstart files found."
                gum confirm "Return to menu?" && continue || break
            fi
            DOC=$(echo "$DOC_FILES" | gum filter --placeholder "Search guides...")
            if [[ -n "$DOC" && -f "$DOC" ]]; then
                glow "$DOC" -p
            fi
            ;;

        "📝 View Posts")
            POST_FILES=$(find pages/_posts -name "*.md" 2>/dev/null)
            if [[ -z "$POST_FILES" ]]; then
                gum style --foreground red "No post files found."
                gum confirm "Return to menu?" && continue || break
            fi
            POST=$(echo "$POST_FILES" | gum filter --placeholder "Search posts...")
            if [[ -n "$POST" && -f "$POST" ]]; then
                glow "$POST" -p
            fi
            ;;
            
        "📊 View Statistics")
            gum style --border rounded --padding "1 2" \
                "Quests: $(find pages/_quests -name "*.md" 2>/dev/null | wc -l | xargs)" \
                "Posts:  $(find pages/_posts -name "*.md" 2>/dev/null | wc -l | xargs)" \
                "Guides: $(find pages/_quickstart -name "*.md" 2>/dev/null | wc -l | xargs)"
            gum confirm "Return to menu?" && continue || break
            ;;

        "🐳 Docker Controls")
            if ! command -v docker-compose &> /dev/null; then
                gum style --foreground red "Docker Compose not found. Please install Docker."
                gum confirm "Return to menu?" && continue || break
            fi
            ACTION=$(gum choose "Up (Detached)" "Down" "Logs" "Back")
            case "$ACTION" in
                "Up (Detached)") 
                    gum style --foreground green "Starting containers..."
                    docker-compose up -d && gum style --foreground green "Containers started!" || gum style --foreground red "Failed to start containers."
                    ;;
                "Down") 
                    gum style --foreground yellow "Stopping containers..."
                    docker-compose down && gum style --foreground green "Containers stopped!" || gum style --foreground red "Failed to stop containers."
                    ;;
                "Logs") 
                    gum style --foreground blue "Showing logs (press Ctrl+C to exit)..."
                    docker-compose logs -f
                    ;;
                "Back") continue ;;
            esac
            [[ "$ACTION" != "Logs" ]] && gum confirm "Return to menu?" && continue || break
            ;;
            
        "🚪 Exit")
            gum style --foreground 212 "Safe travels, adventurer!"
            break
            ;;
    esac
done
```

## 3. Run Your Interface

Now you can launch your custom terminal environment:

```bash
./journey.sh
```

## 4. Advanced: The "Terminal Emulator" Experience

To make this feel like a true dedicated environment, you can configure your terminal emulator (like iTerm2, Alacritty, or Windows Terminal) to launch this script directly upon opening a specific profile.

**Example (iTerm2 / General Profiles):**
1.  Create a new Profile named "IT-Journey".
2.  Set the **Command** to `/path/to/it-journey/journey.sh` (instead of `/bin/zsh`).
3.  Now, when you open this profile, you are immediately dropped into your custom IT-Journey dashboard!

## 5. Next Steps

*   **Add more actions**: Add options to run `docker-compose up`, run tests, or generate new posts.
*   **Style it**: Use `gum style` to match your personal aesthetic.
*   **Automate**: Use `gum input` to create a wizard for generating new quest files.
*   **Customize**: Add your own menu options for repository-specific tasks.
*   **Terminal Integration**: Configure your terminal emulator to launch this script automatically.

## 6. Features Overview

The `journey.sh` script provides:

### 📜 Browse Quests
- Search and filter through all quest files
- Render markdown with syntax highlighting using Glow
- Navigate the educational content easily

### 📖 Read Quickstarts  
- Access all quickstart guides in the terminal
- Perfect for reference while working
- Beautiful markdown rendering

### 📝 View Posts
- Browse development chronicles and blog posts
- Stay updated with project progress
- Read documentation in a distraction-free environment

### 📊 View Statistics
- Quick overview of repository content
- Track growth and activity
- Useful for project management

### 🐳 Docker Controls
- Start/stop containers with visual feedback
- View logs in real-time
- Manage the development environment

### Error Handling
- Dependency checks on startup
- Directory validation
- Graceful handling of missing files
- User-friendly error messages
