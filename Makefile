# Makefile for IT-Journey Content Statistics and Quest Tooling
# Provides convenient commands for managing content statistics and quest validation

.PHONY: help stats stats-update stats-show stats-clean stats-config test \
        serve build build-prod build-ci clean \
        quest-validate quest-network quest-network-strict quest-build-network \
        quest-audit quest-audit-strict quest-levels-data quest-nav \
        content-validate content-normalize content-normalize-apply content-audit

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
	@echo "  make quest-audit            - Full quest audit (validate + network + build)"
	@echo "  make quest-audit-strict     - Full audit + strict network (matches CI behaviour)"
	@echo ""
	@echo "📝 Content Tooling"
	@echo "  make content-validate          - Frontmatter validator across pages/"
	@echo "  make content-normalize         - Dry-run frontmatter normalizer across pages/"
	@echo "  make content-normalize-apply   - Apply frontmatter normalization across pages/"
	@echo "  make content-audit             - Full content audit (frontmatter + quests + network)"
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

quest-audit: quest-build-network quest-validate quest-network
	@echo "✅ Quest audit complete — content, dependencies, and network artifacts validated."

quest-audit-strict: quest-build-network quest-validate quest-network-strict
	@echo "✅ Strict quest audit complete (orphan warnings escalated)."

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

content-audit: content-validate quest-validate quest-network
	@echo "✅ Content audit complete — frontmatter, quests, and network validated."

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
