# Makefile for IT-Journey Content Statistics
# Provides convenient commands for managing content statistics

.PHONY: help stats stats-update stats-show stats-clean stats-config test

# Default target
help:
	@echo "📊 IT-Journey Content Statistics"
	@echo "================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make stats        - Generate content statistics"
	@echo "  make stats-update - Update statistics and show summary"
	@echo "  make stats-show   - Display current statistics"
	@echo "  make stats-clean  - Remove generated statistics file"
	@echo "  make stats-config - Show current configuration"
	@echo "  make test         - Test the statistics generator"
	@echo ""

# Generate statistics
stats:
	@echo "🔄 Generating content statistics..."
	@bash _data/generate_statistics.sh

# Update and show summary
stats-update:
	@bash _data/update_statistics.sh

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
	@ruby -c _data/generate_statistics.rb && echo "✅ Ruby syntax check passed"
	@if [ -d "pages/_posts" ]; then \
		echo "✅ Posts directory found"; \
	else \
		echo "❌ Posts directory not found"; \
		exit 1; \
	fi
	@bash -n _data/generate_statistics.sh && echo "✅ Bash script syntax check passed"
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
