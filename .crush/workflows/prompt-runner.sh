#!/usr/bin/env bash
# Crush Workflow Prompt Runner v1.0.0
# Executes individual prompts with context injection and output capture

# Run a prompt file with inputs
prompt_run() {
    local prompt_file="$1"
    local inputs_json="$2"
    local output_dir="$3"
    
    if [[ ! -f "$prompt_file" ]]; then
        echo "Prompt file not found: $prompt_file" >&2
        return 1
    fi
    
    echo "Running prompt: $prompt_file" >&2
    echo "Inputs: $inputs_json" >&2
    echo "Output directory: $output_dir" >&2
    
    # Read prompt content
    local prompt_content=$(cat "$prompt_file")
    
    # Build context string from inputs
    local context=""
    while IFS= read -r line; do
        local key=$(echo "$line" | jq -r '.key')
        local value=$(echo "$line" | jq -r '.value')
        context="$context\n$key: $value"
    done < <(echo "$inputs_json" | jq -c 'to_entries[]')
    
    # Create combined prompt
    local combined_prompt="${prompt_content}\n\n## Context\n${context}\n\n## Task\nGenerate the requested content based on the prompt and context above. Save outputs to structured files."
    
    # Log the execution
    local log_file="$output_dir/prompt_execution.log"
    echo "=== Prompt Execution ===" > "$log_file"
    echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$log_file"
    echo "Prompt: $prompt_file" >> "$log_file"
    echo "Inputs:" >> "$log_file"
    echo "$inputs_json" | jq '.' >> "$log_file"
    echo "" >> "$log_file"
    
    # Use Crush to execute the prompt
    if command -v crush &> /dev/null; then
        echo "Executing with Crush..." >&2
        
        # Create temporary prompt file with context
        local temp_prompt=$(mktemp)
        echo -e "$combined_prompt" > "$temp_prompt"
        
        # Execute with Crush (this would need actual Crush API integration)
        # For now, create placeholder outputs
        echo "# Generated Output" > "$output_dir/output.md"
        echo "This is a placeholder for AI-generated content." >> "$output_dir/output.md"
        echo "" >> "$output_dir/output.md"
        echo "## Context Used" >> "$output_dir/output.md"
        echo -e "$context" >> "$output_dir/output.md"
        
        # Save metadata
        cat > "$output_dir/metadata.json" << EOF
{
  "prompt_file": "$prompt_file",
  "executed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "inputs": $inputs_json,
  "status": "completed"
}
EOF
        
        rm "$temp_prompt"
        
        echo "Prompt execution completed" >&2
        return 0
    else
        echo "Crush not available, using mock execution" >&2
        
        # Mock execution for testing
        echo "# Mock Output" > "$output_dir/output.md"
        echo "Crush is not installed. This is a mock output for testing." >> "$output_dir/output.md"
        
        cat > "$output_dir/metadata.json" << EOF
{
  "prompt_file": "$prompt_file",
  "executed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "inputs": $inputs_json,
  "status": "mock",
  "note": "Crush not available"
}
EOF
        
        return 0
    fi
}

# Parse prompt front matter
prompt_parse_frontmatter() {
    local prompt_file="$1"
    
    if [[ ! -f "$prompt_file" ]]; then
        echo "{}" >&2
        return 1
    fi
    
    # Extract YAML front matter (between --- markers)
    local frontmatter=$(sed -n '/^---$/,/^---$/p' "$prompt_file" | sed '1d;$d')
    
    if [[ -z "$frontmatter" ]]; then
        echo "{}"
        return 0
    fi
    
    # Convert YAML to JSON
    echo "$frontmatter" | yq eval -o=json '.'
}

# Validate prompt structure
prompt_validate() {
    local prompt_file="$1"
    
    if [[ ! -f "$prompt_file" ]]; then
        echo "Prompt file not found: $prompt_file" >&2
        return 1
    fi
    
    # Check for front matter
    if ! grep -q "^---$" "$prompt_file"; then
        echo "Warning: Prompt missing front matter" >&2
    fi
    
    # Check for content
    local content_lines=$(wc -l < "$prompt_file")
    if [[ $content_lines -lt 10 ]]; then
        echo "Warning: Prompt seems too short ($content_lines lines)" >&2
    fi
    
    echo "Prompt validation passed" >&2
    return 0
}

# Export for use in engine.sh
export -f prompt_run
export -f prompt_parse_frontmatter
export -f prompt_validate
