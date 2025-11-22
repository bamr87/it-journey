#!/usr/bin/env bash
# Crush Workflow State Manager v1.0.0
# Manages workflow execution state, checkpoints, and context persistence

# State initialization
state_init() {
    local execution_dir="$1"
    local workflow_file="$2"
    local input_data="$3"
    
    local state_file="$execution_dir/state.json"
    local inputs_file="$execution_dir/inputs.json"
    
    # Extract workflow metadata
    local workflow_name=$(yq eval '.workflow.name' "$workflow_file")
    local workflow_version=$(yq eval '.workflow.version' "$workflow_file")
    local execution_id=$(basename "$execution_dir")
    
    # Create initial state
    cat > "$state_file" << EOF
{
  "workflow": {
    "name": "$workflow_name",
    "version": "$workflow_version",
    "file": "$workflow_file",
    "execution_id": "$execution_id",
    "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "status": "running",
    "current_step": null
  },
  "inputs": $input_data,
  "steps": {},
  "context": {},
  "metrics": {
    "total_duration": null,
    "step_count": 0,
    "iterations": 0,
    "checkpoints_saved": 0
  }
}
EOF
    
    # Save inputs separately
    echo "$input_data" > "$inputs_file"
    
    # Return silently to prevent stdout pollution
    return 0
}

# Update workflow status
state_update_workflow() {
    local execution_dir="$1"
    local status="$2"
    
    local state_file="$execution_dir/state.json"
    
    # Update status and completion time if finished
    if [[ "$status" == "completed" || "$status" == "failed" ]]; then
        jq --arg status "$status" \
           --arg completed "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
           '.workflow.status = $status | .workflow.completed_at = $completed' \
           "$state_file" > "$state_file.tmp" && mv "$state_file.tmp" "$state_file"
        
        # Calculate duration
        local started=$(jq -r '.workflow.started_at' "$state_file")
        local completed=$(jq -r '.workflow.completed_at' "$state_file")
        
        # TODO: Calculate actual duration
        jq '.metrics.total_duration = "calculated"' "$state_file" > "$state_file.tmp" && mv "$state_file.tmp" "$state_file"
    else
        jq --arg status "$status" '.workflow.status = $status' "$state_file" > "$state_file.tmp" && mv "$state_file.tmp" "$state_file"
    fi
}

# Update step status
state_update_step() {
    local execution_dir="$1"
    local step_id="$2"
    local status="$3"
    
    local state_file="$execution_dir/state.json"
    
    # Initialize step if not exists
    if ! jq -e ".steps.\"$step_id\"" "$state_file" &> /dev/null; then
        jq --arg step "$step_id" \
           --arg status "$status" \
           --arg started "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
           '.steps[$step] = {status: $status, started_at: $started}' \
           "$state_file" > "$state_file.tmp" && mv "$state_file.tmp" "$state_file"
    else
        # Update existing step
        jq --arg step "$step_id" \
           --arg status "$status" \
           '.steps[$step].status = $status' \
           "$state_file" > "$state_file.tmp" && mv "$state_file.tmp" "$state_file"
        
        # Add completion time if completed or failed
        if [[ "$status" == "completed" || "$status" == "failed" ]]; then
            jq --arg step "$step_id" \
               --arg completed "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
               '.steps[$step].completed_at = $completed' \
               "$state_file" > "$state_file.tmp" && mv "$state_file.tmp" "$state_file"
        fi
    fi
    
    # Update current step
    jq --arg step "$step_id" '.workflow.current_step = $step' "$state_file" > "$state_file.tmp" && mv "$state_file.tmp" "$state_file"
}

# Save step outputs to state
state_save_outputs() {
    local execution_dir="$1"
    local step_id="$2"
    local output_dir="$3"
    
    local state_file="$execution_dir/state.json"
    
    # Build outputs object from files in output_dir
    local outputs="{}"
    
    if [[ -d "$output_dir" ]]; then
        while IFS= read -r -d '' file; do
            local output_name=$(basename "$file" | sed 's/\.[^.]*$//')
            local relative_path="${file#$execution_dir/}"
            
            outputs=$(echo "$outputs" | jq --arg key "$output_name" --arg path "$relative_path" '. + {($key): $path}')
        done < <(find "$output_dir" -type f -print0)
    fi
    
    # Update state with outputs
    jq --arg step "$step_id" \
       --argjson outputs "$outputs" \
       '.steps[$step].outputs = $outputs' \
       "$state_file" > "$state_file.tmp" && mv "$state_file.tmp" "$state_file"
}

# Save checkpoint
state_save_checkpoint() {
    local execution_dir="$1"
    
    local state_file="$execution_dir/state.json"
    local checkpoint_file="$execution_dir/checkpoints/checkpoint-$(date +%Y%m%d-%H%M%S).json"
    
    # Copy current state as checkpoint
    cp "$state_file" "$checkpoint_file"
    
    # Update checkpoint count
    jq '.metrics.checkpoints_saved += 1' "$state_file" > "$state_file.tmp" && mv "$state_file.tmp" "$state_file"
    
    echo "Checkpoint saved: $checkpoint_file"
}

# Restore from checkpoint
state_restore_checkpoint() {
    local execution_dir="$1"
    local checkpoint_name="${2:-latest}"
    
    local checkpoints_dir="$execution_dir/checkpoints"
    
    if [[ ! -d "$checkpoints_dir" ]]; then
        echo "No checkpoints found" >&2
        return 1
    fi
    
    local checkpoint_file
    if [[ "$checkpoint_name" == "latest" ]]; then
        checkpoint_file=$(find "$checkpoints_dir" -name "checkpoint-*.json" -type f | sort -r | head -1)
    else
        checkpoint_file="$checkpoints_dir/$checkpoint_name.json"
    fi
    
    if [[ ! -f "$checkpoint_file" ]]; then
        echo "Checkpoint not found: $checkpoint_name" >&2
        return 1
    fi
    
    # Restore state
    cp "$checkpoint_file" "$execution_dir/state.json"
    
    echo "State restored from: $checkpoint_file"
}

# Get step output value
state_get_output() {
    local execution_dir="$1"
    local step_id="$2"
    local output_name="$3"
    
    local state_file="$execution_dir/state.json"
    
    local output_path=$(jq -r ".steps.\"$step_id\".outputs.\"$output_name\"" "$state_file")
    
    if [[ "$output_path" == "null" || -z "$output_path" ]]; then
        echo "Output not found: $step_id.$output_name" >&2
        return 1
    fi
    
    local full_path="$execution_dir/$output_path"
    
    if [[ -f "$full_path" ]]; then
        cat "$full_path"
    else
        echo "Output file not found: $full_path" >&2
        return 1
    fi
}

# Validate state file
state_validate() {
    local state_file="$1"
    
    if [[ ! -f "$state_file" ]]; then
        echo "State file not found: $state_file" >&2
        return 1
    fi
    
    if ! jq empty "$state_file" &> /dev/null; then
        echo "Invalid JSON in state file" >&2
        return 1
    fi
    
    # Check required fields
    local required_fields=(".workflow.name" ".workflow.status" ".inputs" ".steps")
    
    for field in "${required_fields[@]}"; do
        if ! jq -e "$field" "$state_file" &> /dev/null; then
            echo "Missing required field: $field" >&2
            return 1
        fi
    done
    
    echo "State file is valid"
    return 0
}

# Export for use in engine.sh
export -f state_init
export -f state_update_workflow
export -f state_update_step
export -f state_save_outputs
export -f state_save_checkpoint
export -f state_restore_checkpoint
export -f state_get_output
export -f state_validate
