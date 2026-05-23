#!/usr/bin/env bash
#
# Script: bash_crawl.sh
# Description: Bashcrawl quest launcher for IT-Journey — web, local, and agent modes.
# Author: IT-Journey Team
# Version: 3.0.0
# Last Modified: 2026-05-22
# Dependencies: bash, git, optional browser opener (open/xdg-open), optional python3+textual
# Tested On: macOS, Linux, WSL
#
# Usage: bash_crawl.sh [online|local|classic|native|tutorial|agent|help|menu]
#        bash_crawl.sh --quest <chamber>   Print walkthrough URL and launch

set -euo pipefail

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly SCRIPT_VERSION="3.0.0"
readonly BASHCRAWL_WEB_URL="https://bamr87.github.io/bashcrawl/"
readonly BASHCRAWL_REPO_URL="https://github.com/bamr87/bashcrawl.git"
readonly BASHCRAWL_DIR="${BASHCRAWL_DIR:-bashcrawl}"
readonly BASE_URL="https://it-journey.dev"

# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------
log_info()  { echo "[INFO]  $*"; }
log_warn()  { echo "[WARN]  $*" >&2; }
log_error() { echo "[ERROR] $*" >&2; }

# ---------------------------------------------------------------------------
# Walkthrough URL lookup
# ---------------------------------------------------------------------------

# Map of chamber aliases → walkthrough side-quest paths
declare -A QUEST_MAP=(
    [entrance]="/quests/0000/side-quests/entrance/"
    [workshop]="/quests/0000/side-quests/workshop/"
    [cellar]="/quests/0000/side-quests/cellar/"
    [armoury]="/quests/0000/side-quests/armoury/"
    [armory]="/quests/0000/side-quests/armoury/"
    [chamber]="/quests/0000/side-quests/chamber/"
    [chapel]="/quests/0000/side-quests/hidden-chapel/"
    [vault]="/quests/0000/side-quests/vault/"
    [scrap]="/quests/0000/side-quests/scrap/"
    [rift]="/quests/0000/side-quests/rift/"
    [agent]="/quests/0000/side-quests/agent-mode/"
)

show_quest_url() {
    local chamber="${1:-}"
    if [[ -z "$chamber" ]]; then
        log_error "Usage: $SCRIPT_NAME --quest <chamber>"
        echo "Chambers: entrance, workshop, cellar, armoury, chamber, chapel, vault, scrap, rift, agent"
        exit 2
    fi
    local path="${QUEST_MAP[$chamber]:-}"
    if [[ -z "$path" ]]; then
        log_error "Unknown chamber: $chamber"
        echo "Available: ${!QUEST_MAP[*]}"
        exit 2
    fi
    echo "Walkthrough: ${BASE_URL}${path}"
}

# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------

show_help() {
    cat <<EOF
Bashcrawl Quest Launcher v${SCRIPT_VERSION}

Usage:
  $SCRIPT_NAME [MODE]
  $SCRIPT_NAME --quest <chamber>

Modes:
  online    Open the no-install browser version
  local     Clone/update the repo and launch Textual TUI (--interactive)
  classic   Clone/update the repo and launch the pure Bash emulator (--classic)
  native    Clone/update the repo and show native terminal instructions
  tutorial  Clone/update the repo and launch tutorial mode (--tutorial)
  agent     Clone/update the repo and launch agent mode (--agent)
  help      Show this help text
  menu      Interactive mode-selection menu (default)

Options:
  --quest <chamber>   Print the IT-Journey walkthrough URL for a chamber,
                      then launch the appropriate local mode. Chambers:
                      entrance, workshop, cellar, armoury, chamber, chapel,
                      vault, scrap, rift, agent

Environment:
  BASHCRAWL_DIR   Local clone directory (default: ./bashcrawl)

Examples:
  $SCRIPT_NAME online
  $SCRIPT_NAME local
  $SCRIPT_NAME --quest cellar
EOF
}

# ---------------------------------------------------------------------------
# Browser opener
# ---------------------------------------------------------------------------

open_online_game() {
    log_info "Opening Bashcrawl Web: $BASHCRAWL_WEB_URL"
    if command -v open >/dev/null 2>&1; then
        open "$BASHCRAWL_WEB_URL"
    elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$BASHCRAWL_WEB_URL"
    else
        echo "Open this URL in your browser:"
        echo "  $BASHCRAWL_WEB_URL"
    fi
}

# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

ensure_git() {
    if ! command -v git >/dev/null 2>&1; then
        log_error "git is required for local Bashcrawl setup."
        echo "Use online mode instead: $BASHCRAWL_WEB_URL"
        exit 3
    fi
}

clone_or_update_repo() {
    ensure_git

    if [[ -d "$BASHCRAWL_DIR/.git" ]]; then
        log_info "Updating existing Bashcrawl clone in $BASHCRAWL_DIR..."
        git -C "$BASHCRAWL_DIR" pull --ff-only
    elif [[ -e "$BASHCRAWL_DIR" ]]; then
        log_error "$BASHCRAWL_DIR exists but is not a Git repository."
        echo "Set BASHCRAWL_DIR to another path or move the existing directory."
        exit 5
    else
        log_info "Cloning Bashcrawl into $BASHCRAWL_DIR..."
        git clone "$BASHCRAWL_REPO_URL" "$BASHCRAWL_DIR"
    fi
}

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

run_setup() {
    local setup_script="$BASHCRAWL_DIR/setup.sh"
    if [[ ! -x "$setup_script" ]]; then
        chmod +x "$setup_script"
    fi
    "$setup_script" --quick
    "$setup_script" --verify
}

# ---------------------------------------------------------------------------
# Local modes
# ---------------------------------------------------------------------------

launch_local_mode() {
    local mode="$1"

    clone_or_update_repo
    run_setup

    local main_script="$BASHCRAWL_DIR/main.sh"
    if [[ ! -x "$main_script" ]]; then
        chmod +x "$main_script"
    fi

    case "$mode" in
        local)     exec "$main_script" --interactive ;;
        classic)   exec "$main_script" --classic ;;
        tutorial)  exec "$main_script" --tutorial ;;
        agent)     exec "$main_script" --agent ;;
        native)
            echo "Native mode uses your real terminal environment."
            echo "Run when ready:"
            echo "  cd $BASHCRAWL_DIR"
            echo "  ./main.sh --native"
            ;;
        *)
            log_error "Unknown local mode: $mode"
            exit 2
            ;;
    esac
}

# ---------------------------------------------------------------------------
# Interactive menu
# ---------------------------------------------------------------------------

prompt_for_mode() {
    cat <<EOF

Choose your Bashcrawl path:

  1) Play online now        (no install — opens browser)
  2) Textual TUI (local)    (install + rich interface)
  3) Classic Bash (local)   (install + pure bash emulator)
  4) Tutorial mode (local)  (install + step-by-step guidance)
  5) Agent mode (local)     (install + AI/automation mode)
  6) Native terminal        (install + show manual instructions)
  7) Show help

EOF
    printf "Selection [1-7]: "
    read -r selection

    case "$selection" in
        1) open_online_game ;;
        2) launch_local_mode local ;;
        3) launch_local_mode classic ;;
        4) launch_local_mode tutorial ;;
        5) launch_local_mode agent ;;
        6) launch_local_mode native ;;
        7) show_help ;;
        *)
            log_error "Choose a number from 1 to 7."
            exit 2
            ;;
    esac
}

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

main() {
    # Handle --quest flag (may appear anywhere)
    if [[ "${1:-}" == "--quest" ]]; then
        show_quest_url "${2:-}"
        # After printing the URL, launch local mode by default
        log_info "Launching local mode..."
        launch_local_mode local
        return
    fi

    local mode="${1:-menu}"

    case "$mode" in
        online)                  open_online_game ;;
        local|classic|native|\
        tutorial|agent)          launch_local_mode "$mode" ;;
        help|--help|-h)          show_help ;;
        menu)                    prompt_for_mode ;;
        *)
            log_error "Unknown mode: $mode"
            show_help
            exit 2
            ;;
    esac
}

main "$@"


open_online_game() {
    echo "Opening Bashcrawl Web: $BASHCRAWL_WEB_URL"

    if command -v open >/dev/null 2>&1; then
        open "$BASHCRAWL_WEB_URL"
    elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$BASHCRAWL_WEB_URL"
    else
        echo "Open this URL in your browser: $BASHCRAWL_WEB_URL"
    fi
}

ensure_git() {
    if ! command -v git >/dev/null 2>&1; then
        echo "Error: git is required for local Bashcrawl setup." >&2
        echo "Use online mode instead: $BASHCRAWL_WEB_URL" >&2
        exit 3
    fi
}

clone_or_update_repo() {
    ensure_git

    if [[ -d "$BASHCRAWL_DIR/.git" ]]; then
        echo "Updating existing Bashcrawl clone in $BASHCRAWL_DIR..."
        git -C "$BASHCRAWL_DIR" pull --ff-only
    elif [[ -e "$BASHCRAWL_DIR" ]]; then
        echo "Error: $BASHCRAWL_DIR exists but is not a Git repository." >&2
        echo "Set BASHCRAWL_DIR to another path or move the existing directory." >&2
        exit 5
    else
        echo "Cloning Bashcrawl into $BASHCRAWL_DIR..."
        git clone "$BASHCRAWL_REPO_URL" "$BASHCRAWL_DIR"
    fi
}

run_setup() {
    if [[ ! -x "$BASHCRAWL_DIR/setup.sh" ]]; then
        chmod +x "$BASHCRAWL_DIR/setup.sh"
    fi

    "$BASHCRAWL_DIR/setup.sh" --quick
    "$BASHCRAWL_DIR/setup.sh" --verify
}

launch_local_mode() {
    local mode="$1"

    clone_or_update_repo
    run_setup

    case "$mode" in
        local)
            exec "$BASHCRAWL_DIR/main.sh" --interactive
            ;;
        classic)
            exec "$BASHCRAWL_DIR/main.sh" --classic
            ;;
        native)
            echo "Native mode uses your real terminal environment."
            echo "Run this when you are ready:"
            echo "  cd $BASHCRAWL_DIR"
            echo "  ./main.sh --native"
            ;;
        *)
            echo "Error: unknown local mode: $mode" >&2
            exit 2
            ;;
    esac
}

prompt_for_mode() {
    cat <<EOF
Choose your Bashcrawl path:

1) Play online now (recommended first run)
2) Install/update locally and launch Textual TUI
3) Install/update locally and launch classic Bash emulator
4) Prepare native terminal mode
5) Show help
EOF
    printf "\nSelection [1-5]: "
    read -r selection

    case "$selection" in
        1) open_online_game ;;
        2) launch_local_mode local ;;
        3) launch_local_mode classic ;;
        4) launch_local_mode native ;;
        5) show_help ;;
        *)
            echo "Error: choose a number from 1 to 5." >&2
            exit 2
            ;;
    esac
}

main() {
    local mode="${1:-menu}"

    case "$mode" in
        online) open_online_game ;;
        local|classic|native) launch_local_mode "$mode" ;;
        help|--help|-h) show_help ;;
        menu) prompt_for_mode ;;
        *)
            echo "Error: unknown mode: $mode" >&2
            show_help
            exit 2
            ;;
    esac
}

main "$@"
