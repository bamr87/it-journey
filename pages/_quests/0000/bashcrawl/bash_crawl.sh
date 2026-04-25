#!/usr/bin/env bash
#
# Script: bash_crawl.sh
# Description: Guided Bashcrawl launcher for online play or local setup.
# Author: IT-Journey Team
# Version: 2.0.0
# Last Modified: 2026-04-25
# Dependencies: bash, git, optional browser opener (open/xdg-open)
# Tested On: macOS, Linux, WSL
#
# Usage: bash_crawl.sh [online|local|classic|native|help]

set -euo pipefail

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly BASHCRAWL_WEB_URL="https://bamr87.github.io/bashcrawl/"
readonly BASHCRAWL_REPO_URL="https://github.com/bamr87/bashcrawl.git"
readonly BASHCRAWL_DIR="${BASHCRAWL_DIR:-bashcrawl}"

show_help() {
    cat <<EOF
Bashcrawl Quest Launcher

Usage:
  $SCRIPT_NAME [online|local|classic|native|help]

Modes:
  online   Open the no-install browser version
  local    Clone/update the repo and launch Textual TUI mode
  classic  Clone/update the repo and launch the pure Bash emulator
  native   Clone/update the repo and show native terminal instructions
  help     Show this help text

Environment:
  BASHCRAWL_DIR  Local clone directory (default: ./bashcrawl)
EOF
}

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
