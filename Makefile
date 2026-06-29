# Makefile for IT-Journey Content Statistics and Quest Tooling
# Provides convenient commands for managing content statistics and quest validation

.PHONY: help stats stats-update stats-show stats-clean stats-config test \
        serve build build-prod build-ci clean \
        quest-validate quest-network quest-network-strict quest-build-network \
        quest-audit quest-audit-strict quest-audit-report quest-levels-data quest-nav quest-data quest-normalize \
        docker-validate docker-validate-strict docker-build-ci docker-audit-tier2 \
        quest-execute quest-execute-host \
        content-validate content-normalize content-normalize-apply content-audit \
        mermaid-check mermaid-fix \
        cms-index cms-analyze cms-plan cms-status cms-all \
        issue-triage issue-status issue-plan \
        theme-crawl theme-triage

JEKYLL_CONFIG_DEV := _config.yml,_config_dev.yml
JEKYLL_CONFIG_CI  := _config.yml,_config_dev.yml,_config_ci.yml
JEKYLL_PORT       := 4002

# Default target
help:
	@echo "📊 IT-Journey Content Statistics"
	@echo "================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make stats              - Generate content statistics"
	@echo "  make stats-update       - Update statistics and show summary"
	@echo "  make stats-show         - Display current statistics"
	@echo "  make stats-clean        - Remove generated statistics file"
	@echo "  make stats-config       - Show current configuration"
	@echo "  make test               - Test the statistics generator"
	@echo ""
	@echo "🏗️  Jekyll Build"
	@echo "  make serve              - Dev server (local theme, incremental)"
	@echo "  make build              - Dev build (_config.yml + _config_dev.yml)"
	@echo "  make build-ci           - CI smoke build (matches PR workflow)"
	@echo "  make build-prod         - Production build (remote theme)"
	@echo "  make clean              - Remove _site and Jekyll caches"
	@echo ""
	@echo "🎯 Quest Tooling"
	@echo "  make quest-validate         - Run quest_validator.py across pages/_quests"
	@echo "  make quest-network          - Validate quest dependency network (errors only)"
	@echo "  make quest-network-strict   - Network validation including orphan warnings (CI parity)"
	@echo "  make quest-build-network    - Rebuild quest-network.json / network.yml"
	@echo "  make quest-levels-data      - Emit _data/quests/levels.yml from registry"
	@echo "  make quest-nav              - Regenerate _data/navigation/quests.yml from collection"
	@echo "  make quest-audit            - Unified audit: content + network + data freshness (one report)"
	@echo "  make quest-audit-strict     - Unified audit with warnings escalated to failures"
	@echo "  make quest-audit-report     - Unified audit + JSON report (quest-audit-report.json)"
	@echo ""
	@echo "🐳 Dockerized Validation (CI-parity, no host Ruby/Python)"
	@echo "  make docker-validate        - Run the unified quest audit in Docker (python:3.12-slim)"
	@echo "  make docker-validate-strict - Dockerized audit with warnings as failures"
	@echo "  make docker-build-ci        - CI-parity Jekyll build in Docker (ruby:3.2.3 + github-pages)"
	@echo "  make docker-audit-tier2     - Dockerized audit + Claude tier-2 (needs CLAUDE_CODE_OAUTH_TOKEN)"
	@echo "  make quest-execute QUEST=<path> - Claude RUNS a quest's code snippets, isolated in Docker"
	@echo "  make quest-execute SAMPLE=N     - same, across a spread of N quests"
	@echo ""
	@echo "📝 Content Tooling"
	@echo "  make content-validate          - Frontmatter validator across pages/"
	@echo "  make content-normalize         - Dry-run frontmatter normalizer across pages/"
	@echo "  make content-normalize-apply   - Apply frontmatter normalization across pages/"
	@echo "  make content-audit             - Full content audit (frontmatter + quests + network)"
	@echo ""
	@echo "🧭 AI-Augmented CMS"
	@echo "  make cms-status         - Terminal content dashboard (health by collection)"
	@echo "  make cms-index          - Build .cms/index (content-index + summary + schema)"
	@echo "  make cms-analyze        - Write the daily .cms/reports analysis"
	@echo "  make cms-plan           - Write the daily .cms/worklists (mechanical/substantive)"
	@echo "  make cms-all            - Index + analyze + plan"
	@echo ""
	@echo "🧭 Issue Autopilot"
	@echo "  make issue-triage       - Classify open issues -> .issues/worklists/<date>.md"
	@echo "  make issue-status       - Issue triage dashboard (counts by disposition)"
	@echo "  make issue-plan         - Show what the resolve lane would dispatch (dry-run)"
	@echo ""
	@echo "🔭 Theme Scout (frontend canary)"
	@echo "  make theme-crawl        - Test it-journey.dev -> .frontend/findings.jsonl"
	@echo "  make theme-triage       - Classify theme-vs-content + dedup -> candidates"
	@echo ""

# Generate statistics
stats:
	@echo "🔄 Generating content statistics..."
	@bash scripts/generation/generate_statistics.sh

# Update and show summary
stats-update:
	@bash scripts/generation/update_statistics.sh

# Show current statistics
stats-show:
	@if [ -f "_data/content_statistics.yml" ]; then \
		echo "📊 Current Content Statistics:"; \
		echo "============================"; \
		if command -v yq >/dev/null 2>&1; then \
			echo "Total Posts: $$(yq '.total_posts' _data/content_statistics.yml)"; \
			echo "Published: $$(yq '.published' _data/content_statistics.yml)"; \
			echo "Drafts: $$(yq '.drafts' _data/content_statistics.yml)"; \
			echo "Categories: $$(yq '.category_count' _data/content_statistics.yml)"; \
			echo "Tags: $$(yq '.tag_count' _data/content_statistics.yml)"; \
			echo "Date Range: $$(yq '.date_range.earliest' _data/content_statistics.yml)-$$(yq '.date_range.latest' _data/content_statistics.yml)"; \
			echo ""; \
			echo "🎯 Top Focus Areas:"; \
			yq '.focus_areas | to_entries | sort_by(.value) | reverse | .[0:5] | .[] | "  " + .key + ": " + (.value | tostring)' _data/content_statistics.yml; \
		else \
			echo "Generated: $$(grep 'generated_at:' _data/content_statistics.yml | cut -d' ' -f2-)"; \
			echo "Install 'yq' for detailed statistics display"; \
			echo "  brew install yq  # macOS"; \
			echo "  sudo apt install yq  # Ubuntu"; \
		fi; \
	else \
		echo "❌ No statistics file found. Run 'make stats' first."; \
	fi

# Clean generated files
stats-clean:
	@echo "🧹 Cleaning generated statistics..."
	@rm -f _data/content_statistics.yml
	@echo "✅ Statistics file removed"

# Show configuration
stats-config:
	@echo "⚙️ Current Statistics Configuration:"
	@echo "==================================="
	@if [ -f "_data/statistics_config.yml" ]; then \
		cat _data/statistics_config.yml; \
	else \
		echo "❌ Configuration file not found"; \
	fi

# Test the generator
test:
	@echo "🧪 Testing statistics generator..."
	@ruby -c scripts/generation/generate_statistics.rb && echo "✅ Ruby syntax check passed"
	@if [ -d "pages/_posts" ]; then \
		echo "✅ Posts directory found"; \
	else \
		echo "❌ Posts directory not found"; \
		exit 1; \
	fi
	@bash -n scripts/generation/generate_statistics.sh && echo "✅ Bash script syntax check passed"
	@echo "🎉 All tests passed!"

# Contributor stats targets
contributor-stats:
	@echo "🧙 Generating contributor stats for $(USERNAME)..."
	@bash scripts/generation/generate_contributor_stats.sh $(USERNAME)

contributor-stats-all:
	@echo "🧙 Generating stats for all contributors..."
	@bash scripts/generation/generate_contributor_stats.sh --all

contributor-stats-clean:
	@echo "🧹 Cleaning auto-generated contributor stats..."
	@for f in _data/contributors/*.yml; do \
		[ "$$(basename "$$f")" = "_template.yml" ] && continue; \
		echo "  Resetting: $$f"; \
	done
	@echo "✅ Use git checkout to restore original files"

# Development targets
dev-install:
	@echo "🔧 Setting up development environment..."
	@if ! command -v ruby >/dev/null 2>&1; then \
		echo "❌ Ruby not found. Please install Ruby 2.6+"; \
		exit 1; \
	fi
	@if ! command -v yq >/dev/null 2>&1; then \
		echo "⚠️  yq not found. Install for better statistics display:"; \
		echo "  brew install yq  # macOS"; \
		echo "  sudo apt install yq  # Ubuntu"; \
	fi
	@echo "✅ Development environment ready"

# Jekyll build and serve targets
serve:
	bundle exec jekyll serve --config $(JEKYLL_CONFIG_DEV) --livereload --port $(JEKYLL_PORT)

build:
	bundle exec jekyll build --config $(JEKYLL_CONFIG_DEV)

build-ci:
	bundle exec jekyll build --config $(JEKYLL_CONFIG_CI)

build-prod:
	JEKYLL_ENV=production bundle exec jekyll build --config _config.yml

clean:
	bundle exec jekyll clean

# Quest validation and tooling targets
quest-validate:
	@echo "🎯 Validating quest content..."
	@python3 test/quest-validator/quest_validator.py -d pages/_quests/ --summary

quest-network:
	@echo "🕸️  Validating quest dependency network..."
	@python3 scripts/quest/validate-quest-network.py

quest-network-strict:
	@echo "🕸️  Validating quest dependency network (strict — orphans become errors)..."
	@python3 scripts/quest/validate-quest-network.py --strict

quest-build-network:
	@echo "🔨 Rebuilding quest network artifacts..."
	@python3 scripts/quest/build-quest-network.py

quest-levels-data:
	@echo "📚 Generating _data/quests/levels.yml from quest_registry..."
	@python3 scripts/quest/generate-quest-levels-data.py

quest-nav:
	@echo "🧭 Regenerating quest sidebar navigation..."
	@python3 scripts/quest/generate-quest-navigation.py

quest-normalize:
	@echo "🧹 Normalizing quest frontmatter (relationships, retired fields)..."
	@python3 scripts/quest/normalize-quest-frontmatter.py --apply

quest-data: quest-levels-data quest-nav quest-build-network
	@echo "✅ All registry-derived quest data regenerated (levels, tiers, order, navigation, network)."

quest-audit:
	@echo "🎯 Unified quest audit (content + network + data freshness)..."
	@python3 scripts/quest/quest_audit.py $(EXTRA)

quest-audit-strict:
	@echo "🎯 Strict quest audit (warnings escalated to failures)..."
	@python3 scripts/quest/quest_audit.py --strict $(EXTRA)

# Run the audit the way CI / the daily loop should: deterministic layers only,
# JSON report written for tooling to pick up.
quest-audit-report:
	@python3 scripts/quest/quest_audit.py --json quest-audit-report.json $(EXTRA)

# ── Dockerized validation (CI-parity, no host Ruby/Python needed) ───────────
# docker-validate : full deterministic audit in python:3.12-slim (fast).
# docker-build-ci : real Jekyll build in the ruby:3.2.3 + github-pages image.
# docker-audit-tier2 : audit + Claude review (needs CLAUDE_CODE_OAUTH_TOKEN).
# Override args with EXTRA=..., e.g.  make docker-validate EXTRA=--strict
docker-validate:
	@echo "🐳 Quest audit in Docker (python:3.12-slim)..."
	@docker compose run --rm quest-audit audit $(EXTRA)

docker-validate-strict:
	@docker compose run --rm quest-audit strict $(EXTRA)

docker-build-ci:
	@echo "🐳 CI-parity Jekyll build in Docker (ruby:3.2.3 + github-pages)..."
	@docker compose run --rm quest-build

docker-audit-tier2:
	@echo "🐳 Quest audit + Claude tier-2 in Docker (needs CLAUDE_CODE_OAUTH_TOKEN)..."
	@docker compose run --rm -e CLAUDE_CODE_OAUTH_TOKEN -e ANTHROPIC_API_KEY \
		quest-audit tier2 $(MODE) $(EXTRA)

# ── Execute a quest's code snippets with a Claude agent (isolated) ──────────
# A Claude Code agent walks a quest and ACTUALLY RUNS its runnable code snippets
# in a disposable Docker container (real isolation), reporting which work.
#   make quest-execute QUEST=pages/_quests/0001/terminal-mastery.md
#   make quest-execute SAMPLE=3            # a spread of quests across levels
#   make quest-execute-host QUEST=...      # run on the HOST (no container) — riskier
# Needs CLAUDE_CODE_OAUTH_TOKEN (or ANTHROPIC_API_KEY); without it, runs --mock.
quest-execute:
	@echo "🤖🐳 Claude executing quest code snippets in an isolated container..."
	@if [ -n "$(QUEST)" ]; then TARGET="--changed $(QUEST)"; else TARGET="--tier2-sample $(SAMPLE)"; fi; \
	docker compose run --rm -e CLAUDE_CODE_OAUTH_TOKEN -e ANTHROPIC_API_KEY \
		quest-audit execute $$TARGET $(EXTRA)

quest-execute-host:
	@echo "🤖 Claude executing quest snippets on the HOST sandbox (prefer 'make quest-execute' for isolation)..."
	@if [ -n "$(QUEST)" ]; then TARGET="$(QUEST)"; else TARGET="-d pages/_quests --sample $(SAMPLE)"; fi; \
	python3 test/quest-validator/agentic_validate.py $$TARGET --mode execute --max-turns 40 --summary $(EXTRA)

# Agentic validation (tier 2): drive Claude Code (OAuth) to play quests end-to-end.
# SAMPLE / MODE / EXTRA are overridable, e.g.  make quest-validate-agentic SAMPLE=5 MODE=execute
SAMPLE ?= 3
MODE   ?= review
quest-validate-agentic:
	@echo "🤖 Agentic quest validation ($(MODE) mode, sample $(SAMPLE)) — needs claude login / CLAUDE_CODE_OAUTH_TOKEN..."
	@python3 test/quest-validator/agentic_validate.py -d pages/_quests --sample $(SAMPLE) --mode $(MODE) $(EXTRA)

quest-validate-agentic-mock:
	@echo "🤖 Agentic validator — OFFLINE pipeline test (no auth, no cost)..."
	@python3 test/quest-validator/agentic_validate.py -d pages/_quests --sample $(SAMPLE) --mock --summary

quest-validate-agentic-selftest:
	@echo "🧪 Agentic validator offline self-test suite..."
	@bash test/quest-validator/test-agentic.sh

# Content frontmatter validation and normalization targets
content-validate:
	@echo "📝 Validating frontmatter across pages/ ..."
	@python3 scripts/validation/frontmatter-validator.py pages/ -o TODO/seo/data/frontmatter-report.json

content-normalize:
	@echo "🔧 Dry-run normalize across pages/ ..."
	@python3 scripts/content/normalize-frontmatter.py pages/ --quiet \
		--report TODO/seo/data/normalize-dry-run.json || true

content-normalize-apply:
	@echo "🔧 Applying normalize across pages/ ..."
	@python3 scripts/content/normalize-frontmatter.py pages/ --apply --quiet \
		--report TODO/seo/data/normalize-apply.json

mermaid-check:
	@echo "🧜 Checking Mermaid front-matter flags across pages/ ..."
	@python3 scripts/validation/check_mermaid_flags.py

mermaid-fix:
	@echo "🧜 Adding missing 'mermaid: true' flags across pages/ ..."
	@python3 scripts/validation/check_mermaid_flags.py --fix

content-audit: content-validate mermaid-check quest-validate quest-network
	@echo "✅ Content audit complete — frontmatter, mermaid, quests, and network validated."

# AI-augmented CMS engine (scripts/cms/cms.py -> .cms/)
cms-index:
	@python3 scripts/cms/cms.py index

cms-analyze:
	@python3 scripts/cms/cms.py analyze

cms-plan:
	@python3 scripts/cms/cms.py plan

cms-status:
	@python3 scripts/cms/cms.py status

cms-all:
	@echo "🧭 Building CMS index, analysis report, and daily worklist..."
	@python3 scripts/cms/cms.py all

# Issue Autopilot engine (scripts/issues/ -> .issues/) — classify open issues,
# group them into batches, and decide which to resolve. READ/PLAN ONLY.
issue-triage:
	@echo "🧭 Classifying open issues and writing today's .issues worklist..."
	@python3 scripts/issues/triage.py plan

issue-status:
	@python3 scripts/issues/triage.py status

issue-plan:
	@python3 scripts/issues/dispatch.py --dry-run

# Theme Scout — frontend canary for it-journey.dev (-> files theme bugs upstream)
theme-crawl:
	@echo "🔭 Crawling $${BASE_URL:-https://it-journey.dev} ..."
	@node scripts/frontend/crawl.mjs

theme-triage:
	@python3 scripts/frontend/triage_findings.py

# Watch for changes and auto-update (requires fswatch on macOS)
watch:
	@if command -v fswatch >/dev/null 2>&1; then \
		echo "👀 Watching for changes in posts directory..."; \
		echo "Press Ctrl+C to stop"; \
		fswatch -o pages/_posts/ | while read f; do \
			echo "📝 Changes detected, updating statistics..."; \
			make stats; \
		done; \
	else \
		echo "❌ fswatch not found. Install with:"; \
		echo "  brew install fswatch  # macOS"; \
		echo "  sudo apt install inotify-tools  # Ubuntu (use inotifywait)"; \
	fi
