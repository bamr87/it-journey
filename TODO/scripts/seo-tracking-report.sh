#!/usr/bin/env bash
# SEO Performance Tracking Helper Script
# Generates weekly tracking report template with dates
#
# Usage: ./seo-tracking-report.sh [week_number]
# Example: ./seo-tracking-report.sh 2

set -euo pipefail

# Configuration
TRACKING_DIR="${TRACKING_DIR:-$(dirname "$0")/../seo}"
WEEK_NUM="${1:-1}"

# Calculate dates
START_DATE=$(date -v-"$((7 * (WEEK_NUM - 1)))"d +%Y-%m-%d 2>/dev/null || date -d "-$((7 * (WEEK_NUM - 1))) days" +%Y-%m-%d)
END_DATE=$(date -v-"$((7 * (WEEK_NUM - 1) - 6))"d +%Y-%m-%d 2>/dev/null || date -d "-$((7 * (WEEK_NUM - 1) - 6)) days" +%Y-%m-%d)
REPORT_DATE=$(date +%Y-%m-%d)

cat << EOF
# 📊 SEO Weekly Report - Week $WEEK_NUM

**Report Date**: $REPORT_DATE
**Tracking Period**: $START_DATE to $END_DATE

---

## 📈 Google Search Console Data

### Instructions
1. Go to [Google Search Console](https://search.google.com/search-console)
2. Select date range: $START_DATE to $END_DATE
3. Export data for each optimized page
4. Fill in the metrics below

---

## 🎯 Optimized Pages Performance

| Page | CTR | Impressions | Clicks | Avg Position | vs Baseline |
|------|-----|-------------|--------|--------------|-------------|
| Nerd Font Quest | ___% | _____ | _____ | _____ | Baseline: 0.7% |
| Bootable macOS | ___% | _____ | _____ | _____ | Baseline: 0.5% |
| Jekyll Mermaid | ___% | _____ | _____ | _____ | Baseline: 0% |
| SEC Edgar | ___% | _____ | _____ | _____ | Baseline: 0.3% |
| Desktop Widgets | ___% | _____ | _____ | _____ | Baseline: 0% |
| Auto-increment | ___% | _____ | _____ | _____ | Baseline: 0% |

---

## 📊 Overall Site Metrics

| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Total Clicks | _____ | _____ | _____% |
| Total Impressions | _____ | _____ | _____% |
| Average CTR | _____% | _____% | _____ |
| Average Position | _____ | _____ | _____ |

---

## 🔝 Top Queries This Week

| Query | Clicks | Impressions | CTR | Position |
|-------|--------|-------------|-----|----------|
| 1. _____________ | _____ | _____ | ___% | _____ |
| 2. _____________ | _____ | _____ | ___% | _____ |
| 3. _____________ | _____ | _____ | ___% | _____ |
| 4. _____________ | _____ | _____ | ___% | _____ |
| 5. _____________ | _____ | _____ | ___% | _____ |

---

## 🚀 New Opportunities Identified

### High Impressions, Low CTR (Optimize)
- Query: _____________ (_____ impressions, ___% CTR)
- Query: _____________ (_____ impressions, ___% CTR)

### Rising Queries (Monitor)
- Query: _____________ (+_____ impressions)
- Query: _____________ (+_____ impressions)

---

## ✅ Actions Completed This Week
- [ ] Action 1
- [ ] Action 2
- [ ] Action 3

## 📋 Next Week Priorities
1. Priority 1
2. Priority 2
3. Priority 3

---

## 💡 Insights & Notes

_Add observations about what's working, what's not, and strategy adjustments_

---

**Report Prepared By**: _______________
**Status**: 🔄 Draft | ✅ Final
EOF

echo ""
echo "---"
echo "Report template generated. Copy above content to TRACKING.md or save to:"
echo "  $TRACKING_DIR/reports/week-${WEEK_NUM}-${REPORT_DATE}.md"
