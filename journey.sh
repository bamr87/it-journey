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
