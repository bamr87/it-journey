#!/bin/bash
# guardian.sh - Hyperlink Guardian Main Testing Engine
# Comprehensive link detection and testing for Jekyll sites
# Part of the IT-Journey Testing Framework

set -euo pipefail

# Script metadata
SCRIPT_VERSION="2.0.0"
SCRIPT_NAME="Hyperlink Guardian"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Default configuration
SITE_URL="${SITE_URL:-https://bamr87.github.io/it-journey}"
OUTPUT_DIR="${OUTPUT_DIR:-$PROJECT_ROOT/test-results}"
MAX_PARALLEL="${MAX_PARALLEL:-10}"
TIMEOUT="${TIMEOUT:-30}"
USER_AGENT="${USER_AGENT:-IT-Journey-Hyperlink-Guardian/2.0}"

# Advanced configuration
RETRY_COUNT="${RETRY_COUNT:-2}"
RETRY_DELAY="${RETRY_DELAY:-5}"
EXCLUDE_PATTERNS="${EXCLUDE_PATTERNS:-}"
INTERNAL_ONLY="${INTERNAL_ONLY:-false}"
VERBOSE="${VERBOSE:-false}"
CONFIG_FILE="${CONFIG_FILE:-}"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_debug() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${PURPLE}🔍 DEBUG: $1${NC}"
    fi
}

# Load configuration from file
load_config() {
    local config_file="$1"
    
    if [[ -f "$config_file" ]]; then
        log_info "Loading configuration from: $config_file"
        
        # Check if it's YAML or JSON
        if [[ "$config_file" =~ \.ya?ml$ ]]; then
            # Simple YAML parsing for basic values
            while IFS=': ' read -r key value; do
                case "$key" in
                    "url") SITE_URL="$value" ;;
                    "timeout") TIMEOUT="$value" ;;
                    "retry_count") RETRY_COUNT="$value" ;;
                    "max_parallel") MAX_PARALLEL="$value" ;;
                esac
            done < <(grep -E "^\s*(url|timeout|retry_count|max_parallel):" "$config_file" | sed 's/^[[:space:]]*//')
        elif [[ "$config_file" =~ \.json$ ]]; then
            # JSON parsing with jq if available
            if command -v jq >/dev/null 2>&1; then
                SITE_URL=$(jq -r '.site.url // empty' "$config_file" 2>/dev/null || echo "$SITE_URL")
                TIMEOUT=$(jq -r '.testing.timeout // empty' "$config_file" 2>/dev/null || echo "$TIMEOUT")
                RETRY_COUNT=$(jq -r '.testing.retry_count // empty' "$config_file" 2>/dev/null || echo "$RETRY_COUNT")
                MAX_PARALLEL=$(jq -r '.testing.max_parallel // empty' "$config_file" 2>/dev/null || echo "$MAX_PARALLEL")
            fi
        fi
        log_success "Configuration loaded successfully"
    else
        log_warning "Configuration file not found: $config_file"
    fi
}

# Initialize guardian with improved configuration loading
initialize_guardian() {
    log_info "Initializing ${SCRIPT_NAME} v${SCRIPT_VERSION}"
    
    # Load configuration file if specified or found
    if [[ -n "$CONFIG_FILE" ]]; then
        load_config "$CONFIG_FILE"
    elif [[ -f "$SCRIPT_DIR/../config/guardian-config.yml" ]]; then
        load_config "$SCRIPT_DIR/../config/guardian-config.yml"
    elif [[ -f "$SCRIPT_DIR/../config/test-config.json" ]]; then
        load_config "$SCRIPT_DIR/../config/test-config.json"
    fi
    
    # Load exclusions file if it exists
    local exclusions_file="$SCRIPT_DIR/../config/exclusions.txt"
    if [[ -f "$exclusions_file" && -z "$EXCLUDE_PATTERNS" ]]; then
        EXCLUDE_PATTERNS=$(grep -v '^#' "$exclusions_file" | grep -v '^$' | tr '\n' '|' | sed 's/|$//')
        log_debug "Loaded exclusion patterns from file: $EXCLUDE_PATTERNS"
    fi
    
    log_info "Configuration:"
    log_info "  Target domain: ${SITE_URL}"
    log_info "  Output directory: ${OUTPUT_DIR}"
    log_info "  Max parallel tests: ${MAX_PARALLEL}"
    log_info "  Request timeout: ${TIMEOUT}s"
    log_info "  Retry count: ${RETRY_COUNT}"
    
    # Create output directory structure
    mkdir -p "$OUTPUT_DIR"/{artifacts,reports}
    
    # Initialize log files with headers
    echo "timestamp|url|status_code|response_time|status|error_message|file_source|category" > "$OUTPUT_DIR/detailed-results.csv"
    echo "$(date -u +"%Y-%m-%d %H:%M:%S UTC") - Guardian v${SCRIPT_VERSION} initialization complete" > "$OUTPUT_DIR/artifacts/guardian.log"
}

# Enhanced file finding with better organization
find_content_files() {
    local file_type="$1"
    log_debug "Searching for ${file_type} files..."
    
    case "$file_type" in
        "markdown")
            find "$PROJECT_ROOT" -type f \( -name "*.md" -o -name "*.markdown" \) \
                ! -path "*/node_modules/*" \
                ! -path "*/.git/*" \
                ! -path "*/vendor/*" \
                ! -path "*/_site/*" \
                ! -path "*/test-results/*" \
                ! -path "*/test/hyperlink-guardian/*"
            ;;
        "html")
            find "$PROJECT_ROOT" -type f -name "*.html" \
                ! -path "*/node_modules/*" \
                ! -path "*/.git/*" \
                ! -path "*/vendor/*" \
                ! -path "*/_site/*" \
                ! -path "*/test-results/*"
            ;;
    esac
}

# Enhanced link extraction with categorization
extract_links_from_file() {
    local file="$1"
    local file_type="$2"
    local relative_file="${file#$PROJECT_ROOT/}"
    
    log_debug "Extracting links from ${file_type}: $relative_file"
    
    case "$file_type" in
        "markdown")
            # Standard markdown links [text](url)
            grep -oE '\[([^\]]*)\]\(([^)]+)\)' "$file" 2>/dev/null | sed "s/.*(\([^)]*\)).*/\1|$relative_file|markdown_link/" || true
            
            # Reference-style links [text]: url  
            grep -oE '^\[([^\]]*)\]:\s*(.+)$' "$file" 2>/dev/null | sed "s/.*:\s*\(.*\)/\1|$relative_file|reference_link/" || true
            
            # Bare URLs in text
            grep -oE 'https?://[^[:space:]<>"\)]+' "$file" 2>/dev/null | sed "s/$/|$relative_file|bare_url/" || true
            ;;
        "html")
            # href attributes
            grep -oE 'href="([^"]*)"' "$file" 2>/dev/null | sed "s/href=\"//;s/\"//" | sed "s/$/|$relative_file|html_href/" || true
            
            # src attributes (images, scripts)
            grep -oE 'src="([^"]*)"' "$file" 2>/dev/null | sed "s/src=\"//;s/\"//" | sed "s/$/|$relative_file|html_src/" || true
            
            # action attributes (forms)
            grep -oE 'action="([^"]*)"' "$file" 2>/dev/null | sed "s/action=\"//;s/\"//" | sed "s/$/|$relative_file|html_action/" || true
            ;;
    esac
}

# Enhanced URL normalization with better categorization
normalize_and_categorize_url() {
    local url="$1"
    local source_file="$2"
    local link_category="$3"
    
    log_debug "Processing URL: $url from $source_file ($link_category)"
    
    # Skip problematic URLs
    if [[ -z "$url" ]] || \
       [[ "$url" =~ ^#.*$ ]] || \
       [[ "$url" =~ ^(mailto:|tel:|javascript:|data:) ]] || \
       [[ "$url" =~ \{\{.*\}\} ]]; then
        return 1
    fi
    
    # Apply exclusion patterns
    if [[ -n "$EXCLUDE_PATTERNS" ]] && echo "$url" | grep -qE "$EXCLUDE_PATTERNS"; then
        log_debug "URL excluded by pattern: $url"
        return 1
    fi
    
    # Normalize URL and determine type
    local normalized_url
    local url_type
    
    if [[ "$url" =~ ^/ ]]; then
        normalized_url="${SITE_URL}${url}"
        url_type="internal_absolute"
    elif [[ "$url" =~ ^\./ ]]; then
        normalized_url="${SITE_URL}/${url#./}"
        url_type="internal_relative"
    elif [[ "$url" =~ ^https?:// ]]; then
        normalized_url="$url"
        if [[ "$url" =~ $SITE_URL ]]; then
            url_type="internal_full"
        else
            url_type="external"
        fi
    else
        if [[ "$INTERNAL_ONLY" == "true" ]]; then
            log_debug "Skipping external relative URL in internal-only mode: $url"
            return 1
        fi
        normalized_url="$url"
        url_type="external_relative"
    fi
    
    echo "$normalized_url|$source_file|$link_category|$url_type"
}

# Enhanced URL testing with better error categorization
test_url_with_retry() {
    local url="$1"
    local source_file="$2"
    local link_category="$3"
    local url_type="$4"
    local output_file="$5"
    
    local attempt=1
    local status_code
    local response_time
    local error_message=""
    local final_status="FAIL"
    local error_category="unknown"
    
    log_debug "Testing URL: $url (Type: $url_type, Category: $link_category)"
    
    while [[ $attempt -le $((RETRY_COUNT + 1)) ]]; do
        log_debug "Attempt $attempt/$((RETRY_COUNT + 1)) for $url"
        
        # Use curl with comprehensive options
        local curl_output
        if curl_output=$(curl -s -o /dev/null \
                              -w "%{http_code}|%{time_total}|%{url_effective}" \
                              --max-time "$TIMEOUT" \
                              --user-agent "$USER_AGENT" \
                              --location \
                              --fail-early \
                              --connect-timeout 10 \
                              "$url" 2>&1); then
            
            status_code=$(echo "$curl_output" | cut -d'|' -f1)
            response_time=$(echo "$curl_output" | cut -d'|' -f2)
            
            # Categorize response
            if [[ "$status_code" -ge 200 && "$status_code" -lt 300 ]]; then
                final_status="PASS"
                error_category="none"
                break
            elif [[ "$status_code" -ge 300 && "$status_code" -lt 400 ]]; then
                final_status="REDIRECT"
                error_category="redirect"
                break
            elif [[ "$status_code" == "404" ]]; then
                error_category="not_found"
                error_message="Page not found"
            elif [[ "$status_code" -ge 400 && "$status_code" -lt 500 ]]; then
                error_category="client_error"
                error_message="HTTP $status_code client error"
            elif [[ "$status_code" -ge 500 ]]; then
                error_category="server_error"
                error_message="HTTP $status_code server error"
                # Retry server errors
                if [[ $attempt -lt $((RETRY_COUNT + 1)) ]]; then
                    log_debug "Server error $status_code for $url, retrying in ${RETRY_DELAY}s..."
                    sleep "$RETRY_DELAY"
                fi
            fi
        else
            status_code="ERROR"
            response_time="0"
            error_message="$curl_output"
            
            # Categorize connection errors
            if echo "$error_message" | grep -qi "timeout"; then
                error_category="timeout"
            elif echo "$error_message" | grep -qi "connection.*refused"; then
                error_category="connection_refused"
            elif echo "$error_message" | grep -qi "ssl\|certificate"; then
                error_category="ssl_error"
            elif echo "$error_message" | grep -qi "dns\|resolve"; then
                error_category="dns_error"
            else
                error_category="connection_error"
            fi
            
            # Retry connection errors
            if [[ $attempt -lt $((RETRY_COUNT + 1)) ]]; then
                log_debug "Connection error for $url, retrying in ${RETRY_DELAY}s..."
                sleep "$RETRY_DELAY"
            fi
        fi
        
        ((attempt++))
    done
    
    # Clean up error message for CSV
    error_message=$(echo "$error_message" | tr '|' ';' | tr '\n' ' ' | head -c 150)
    
    # Output result with enhanced categorization
    printf "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" \
        "$(date -u +"%Y-%m-%d %H:%M:%S")" \
        "$url" \
        "$status_code" \
        "$response_time" \
        "$final_status" \
        "$error_message" \
        "$source_file" \
        "$link_category" \
        "$url_type" \
        "$error_category" >> "$output_file"
    
    # Log result with appropriate level
    if [[ "$final_status" == "PASS" ]]; then
        log_success "OK: $url (${status_code}, ${response_time}s)"
    elif [[ "$final_status" == "REDIRECT" ]]; then
        log_warning "REDIRECT: $url (${status_code})"
    else
        log_error "BROKEN: $url (${status_code}, ${error_category}) from $source_file"
    fi
}

# Main link collection and testing function
execute_comprehensive_scan() {
    local results_file="$OUTPUT_DIR/detailed-results.csv"
    local raw_links_file="$OUTPUT_DIR/artifacts/raw-links.txt"
    local processed_links_file="$OUTPUT_DIR/artifacts/processed-links.txt"
    
    log_info "Starting comprehensive link health scan..."
    
    # Clear working files
    > "$raw_links_file"
    > "$processed_links_file"
    
    local total_files=0
    local total_raw_links=0
    
    # Process markdown files
    log_info "Scanning markdown files..."
    while IFS= read -r file; do
        ((total_files++))
        log_debug "Processing markdown file: ${file#$PROJECT_ROOT/}"
        
        while IFS='|' read -r url source_file category; do
            if [[ -n "$url" ]]; then
                echo "$url|$source_file|$category" >> "$raw_links_file"
                ((total_raw_links++))
            fi
        done < <(extract_links_from_file "$file" "markdown")
    done < <(find_content_files "markdown")
    
    # Process HTML files
    log_info "Scanning HTML files..."
    while IFS= read -r file; do
        ((total_files++))
        log_debug "Processing HTML file: ${file#$PROJECT_ROOT/}"
        
        while IFS='|' read -r url source_file category; do
            if [[ -n "$url" ]]; then
                echo "$url|$source_file|$category" >> "$raw_links_file"
                ((total_raw_links++))
            fi
        done < <(extract_links_from_file "$file" "html")
    done < <(find_content_files "html")
    
    log_info "Processed $total_files files and found $total_raw_links raw links"
    
    # Normalize and deduplicate links
    log_info "Normalizing and categorizing links..."
    declare -A tested_urls
    local processed_count=0
    local valid_count=0
    
    while IFS='|' read -r url source_file category; do
        ((processed_count++))
        
        if normalized_data=$(normalize_and_categorize_url "$url" "$source_file" "$category"); then
            echo "$normalized_data" >> "$processed_links_file"
            ((valid_count++))
        fi
    done < "$raw_links_file"
    
    # Count unique URLs
    local unique_count
    unique_count=$(cut -d'|' -f1 "$processed_links_file" | sort | uniq | wc -l)
    
    log_info "Processed $processed_count raw links"
    log_info "Found $valid_count valid links"
    log_info "Identified $unique_count unique URLs to test"
    
    if [[ "$unique_count" -eq 0 ]]; then
        log_warning "No valid links found to test"
        return 0
    fi
    
    # Test URLs with parallel processing
    log_info "Beginning link testing with max $MAX_PARALLEL parallel processes..."
    
    local count=0
    local total_tested=0
    
    # Sort and process unique URLs
    sort "$processed_links_file" | while IFS='|' read -r url source_file category url_type; do
        # Skip if we've already tested this URL (simple deduplication)
        if [[ -n "${tested_urls[$url]:-}" ]]; then
            continue
        fi
        tested_urls["$url"]=1
        
        ((count++))
        ((total_tested++))
        
        log_info "[$total_tested/$unique_count] Testing: $url"
        
        # Run in background for parallel processing
        test_url_with_retry "$url" "$source_file" "$category" "$url_type" "$results_file" &
        
        # Limit parallel processes
        if (( count % MAX_PARALLEL == 0 )); then
            log_debug "Waiting for batch of $MAX_PARALLEL tests to complete..."
            wait
        fi
    done
    
    # Wait for final batch
    wait
    
    log_success "Link testing complete! Results saved to $results_file"
    echo "$total_tested"
}

# Enhanced summary generation with detailed categorization
generate_comprehensive_summary() {
    local results_file="$OUTPUT_DIR/detailed-results.csv"
    local summary_file="$OUTPUT_DIR/summary.json"
    local broken_links_file="$OUTPUT_DIR/broken-links.json"
    
    log_info "Generating comprehensive analysis summary..."
    
    if [[ ! -f "$results_file" ]] || [[ ! -s "$results_file" ]]; then
        log_error "Results file not found or empty: $results_file"
        return 1
    fi
    
    # Calculate comprehensive statistics
    local total_links
    local broken_links
    local working_links
    local redirects
    local success_rate
    
    # Skip header and count results
    total_links=$(tail -n +2 "$results_file" | wc -l)
    broken_links=$(tail -n +2 "$results_file" | grep -c "|FAIL|" || echo "0")
    working_links=$(tail -n +2 "$results_file" | grep -c "|PASS|" || echo "0")
    redirects=$(tail -n +2 "$results_file" | grep -c "|REDIRECT|" || echo "0")
    
    if [[ "$total_links" -gt 0 ]]; then
        success_rate=$(echo "scale=2; $working_links * 100 / $total_links" | bc -l 2>/dev/null || echo "0")
    else
        success_rate="0"
    fi
    
    # Generate categorized broken links analysis
    local broken_links_json="[]"
    if [[ "$broken_links" -gt 0 ]]; then
        broken_links_json="["
        local first=true
        
        while IFS='|' read -r timestamp url status_code response_time status error_message source_file category url_type error_category; do
            if [[ "$status" == "FAIL" ]]; then
                if [[ "$first" == "true" ]]; then
                    first=false
                else
                    broken_links_json+=","
                fi
                
                # Escape JSON strings properly
                url=$(printf '%s' "$url" | sed 's/"/\\"/g')
                error_message=$(printf '%s' "$error_message" | sed 's/"/\\"/g')
                source_file=$(printf '%s' "$source_file" | sed 's/"/\\"/g')
                
                broken_links_json+="
    {
      \"url\": \"$url\",
      \"status_code\": \"$status_code\",
      \"error_message\": \"$error_message\",
      \"source_file\": \"$source_file\",
      \"link_category\": \"$category\",
      \"url_type\": \"$url_type\",
      \"error_category\": \"$error_category\",
      \"timestamp\": \"$timestamp\"
    }"
            fi
        done < <(tail -n +2 "$results_file")
        
        broken_links_json+="
  ]"
    fi
    
    # Save broken links to separate file for AI analysis
    echo "$broken_links_json" > "$broken_links_file"
    
    # Generate performance metrics
    local avg_response_time
    avg_response_time=$(tail -n +2 "$results_file" | awk -F'|' '$4 > 0 {sum+=$4; count++} END {if(count>0) print sum/count; else print 0}')
    
    # Create comprehensive summary
    cat > "$summary_file" << EOF
{
  "scan_metadata": {
    "scan_timestamp": "$(date -u +"%Y-%m-%d %H:%M:%S UTC")",
    "guardian_version": "$SCRIPT_VERSION",
    "site_url": "$SITE_URL",
    "project_root": "$PROJECT_ROOT",
    "scan_parameters": {
      "max_parallel": $MAX_PARALLEL,
      "timeout": $TIMEOUT,
      "retry_count": $RETRY_COUNT,
      "internal_only": $INTERNAL_ONLY,
      "exclude_patterns": "$EXCLUDE_PATTERNS"
    }
  },
  "summary_statistics": {
    "total_links": $total_links,
    "working_links": $working_links,
    "broken_links": $broken_links,
    "redirects": $redirects,
    "success_rate": $success_rate,
    "average_response_time": $avg_response_time
  },
  "categorized_results": {
    "by_status": {
      "pass": $working_links,
      "fail": $broken_links,
      "redirect": $redirects
    },
    "by_type": $(tail -n +2 "$results_file" | cut -d'|' -f9 | sort | uniq -c | awk 'BEGIN{printf "{"} {printf "%s\"%s\": %d", (NR>1?", ":""), $2, $1} END{printf "}"}'),
    "by_error_category": $(tail -n +2 "$results_file" | grep "|FAIL|" | cut -d'|' -f10 | sort | uniq -c | awk 'BEGIN{printf "{"} {printf "%s\"%s\": %d", (NR>1?", ":""), $2, $1} END{printf "}"}')
  },
  "broken_link_details": $broken_links_json,
  "files": {
    "detailed_results": "detailed-results.csv",
    "broken_links": "broken-links.json",
    "raw_links": "artifacts/raw-links.txt",
    "processed_links": "artifacts/processed-links.txt",
    "guardian_log": "artifacts/guardian.log"
  }
}
EOF
    
    log_success "Comprehensive summary generated: $summary_file"
    log_info "📈 Final Statistics:"
    log_info "   Total Links Tested: $total_links"
    log_info "   Working Links: $working_links"
    log_info "   Broken Links: $broken_links"
    log_info "   Redirects: $redirects"
    log_info "   Success Rate: ${success_rate}%"
    log_info "   Average Response Time: ${avg_response_time}s"
    
    return 0
}

# Enhanced help display
show_help() {
    cat << EOF
${CYAN}${SCRIPT_NAME} v${SCRIPT_VERSION}${NC}
Comprehensive hyperlink testing for Jekyll sites

${YELLOW}Usage:${NC} $0 [OPTIONS]

${YELLOW}Options:${NC}
    -h, --help              Show this help message
    -v, --verbose           Enable verbose debugging output
    -u, --url URL           Set target site URL (default: $SITE_URL)
    -o, --output DIR        Set output directory (default: $OUTPUT_DIR)
    -p, --parallel NUM      Set max parallel tests (default: $MAX_PARALLEL)
    -t, --timeout SEC       Set request timeout (default: $TIMEOUT)
    -r, --retry NUM         Set retry count (default: $RETRY_COUNT)
    -c, --config FILE       Load configuration from file
    --internal-only         Test only internal links
    --exclude PATTERN       Exclude URLs matching regex pattern

${YELLOW}Environment Variables:${NC}
    SITE_URL                Target site URL
    OUTPUT_DIR              Output directory for results
    MAX_PARALLEL            Maximum parallel tests
    TIMEOUT                 Request timeout in seconds
    RETRY_COUNT             Number of retries for failed requests
    VERBOSE                 Enable verbose output (true/false)
    EXCLUDE_PATTERNS        Regex pattern for URLs to exclude
    CONFIG_FILE             Configuration file path

${YELLOW}Configuration Files:${NC}
    Default locations (in order of precedence):
    1. File specified by --config or CONFIG_FILE
    2. $SCRIPT_DIR/../config/guardian-config.yml
    3. $SCRIPT_DIR/../config/test-config.json

${YELLOW}Examples:${NC}
    $0                                    # Run with default settings
    $0 --verbose                          # Run with verbose output
    $0 --config custom-config.yml         # Use custom configuration
    $0 --url https://example.com --parallel 20
    $0 --exclude "github\\.com|localhost"  # Exclude specific domains

${YELLOW}Output Files:${NC}
    summary.json              # Comprehensive analysis summary
    detailed-results.csv      # Complete test results
    broken-links.json        # Categorized broken link data
    artifacts/raw-links.txt   # All discovered links
    artifacts/guardian.log    # Execution log

For more information, visit: ${CYAN}https://github.com/bamr87/it-journey${NC}
EOF
}

# Enhanced argument parsing
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                VERBOSE="true"
                shift
                ;;
            -u|--url)
                SITE_URL="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            -p|--parallel)
                MAX_PARALLEL="$2"
                shift 2
                ;;
            -t|--timeout)
                TIMEOUT="$2"
                shift 2
                ;;
            -r|--retry)
                RETRY_COUNT="$2"
                shift 2
                ;;
            -c|--config)
                CONFIG_FILE="$2"
                shift 2
                ;;
            --internal-only)
                INTERNAL_ONLY="true"
                shift
                ;;
            --exclude)
                EXCLUDE_PATTERNS="$2"
                shift 2
                ;;
            *)
                log_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
}

# Main execution function with enhanced error handling
main() {
    echo -e "${CYAN}"
    echo "🔗 ============================================ 🔗"
    echo "   ${SCRIPT_NAME} v${SCRIPT_VERSION}"
    echo "   Advanced Link Health Testing Framework"
    echo "🔗 ============================================ 🔗"
    echo -e "${NC}"
    
    # Parse command line arguments
    parse_arguments "$@"
    
    # Initialize the guardian system
    initialize_guardian
    
    # Execute comprehensive scan
    local tested_count
    tested_count=$(execute_comprehensive_scan)
    
    # Generate detailed summary and analysis
    generate_comprehensive_summary
    
    # Final status report
    echo -e "${CYAN}"
    echo "🎉 ========================================== 🎉"
    echo "   Hyperlink Guardian scan complete!"
    echo "   Tested ${tested_count:-0} unique URLs"
    echo "   Results available in: $OUTPUT_DIR"
    echo "🎉 ========================================== 🎉"
    echo -e "${NC}"
    
    # Exit with appropriate code based on results
    if [[ -f "$OUTPUT_DIR/summary.json" ]]; then
        local broken_count
        broken_count=$(jq -r '.summary_statistics.broken_links' "$OUTPUT_DIR/summary.json" 2>/dev/null || echo "0")
        
        if [[ "$broken_count" -gt 0 ]]; then
            log_warning "Found $broken_count broken links - review required"
            exit 1
        else
            log_success "All links are healthy! 🎊"
            exit 0
        fi
    else
        log_error "Summary file not generated - scan may have failed"
        exit 1
    fi
}

# Execute main function if script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi 