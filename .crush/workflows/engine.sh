#!/usr/bin/env bash
# Crush Workflow Execution Engine v1.0.0
# Orchestrates sequential AI prompt execution with state management

set -euo pipefail

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Source dependencies
source "$SCRIPT_DIR/state-manager.sh"
source "$SCRIPT_DIR/prompt-runner.sh"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}✓${NC} $1" >&2
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1" >&2
}

log_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

log_step() {
    echo -e "${MAGENTA}▶${NC} ${BOLD}$1${NC}" >&2
}

# Check dependencies
check_dependencies() {
    local missing_deps=()
    
    # Required tools
    local required_tools=(yq jq crush gum)
    
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            missing_deps+=("$tool")
        fi
    done
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Install with: brew install yq jq charm/tap/crush charm/tap/gum"
        return 1
    fi
    
    return 0
}

# Parse workflow YAML
parse_workflow() {
    local workflow_file="$1"
    
    if [[ ! -f "$workflow_file" ]]; then
        log_error "Workflow file not found: $workflow_file"
        return 1
    fi
    
    # Validate YAML syntax
    if ! yq eval '.' "$workflow_file" &> /dev/null; then
        log_error "Invalid YAML syntax in workflow file"
        return 1
    fi
    
    log_success "Workflow file parsed: $workflow_file"
    return 0
}

# Validate workflow schema
validate_workflow() {
    local workflow_file="$1"
    local schema_file="$SCRIPT_DIR/schemas/workflow.schema.json"
    
    log_step "Validating workflow schema..."
    
    # Check required fields
    local required_fields=(
        ".workflow.name"
        ".workflow.version"
        ".steps"
    )
    
    for field in "${required_fields[@]}"; do
        if ! yq eval "$field" "$workflow_file" &> /dev/null; then
            log_error "Missing required field: $field"
            return 1
        fi
    done
    
    # Validate step structure
    local step_count=$(yq eval '.steps | length' "$workflow_file")
    if [[ $step_count -eq 0 ]]; then
        log_error "Workflow must have at least one step"
        return 1
    fi
    
    log_success "Workflow schema is valid"
    return 0
}

# Initialize workflow execution
init_workflow() {
    local workflow_file="$1"
    local input_data="$2"
    
    # Generate execution ID
    local execution_id="execution-$(date +%Y%m%d-%H%M%S)"
    
    # Get workflow name
    local workflow_name=$(yq eval '.workflow.name' "$workflow_file" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    
    # Create execution directory
    local execution_dir="$REPO_ROOT/work/workflows/$workflow_name/$execution_id"
    mkdir -p "$execution_dir"/{outputs,checkpoints,logs/steps}
    
    log_success "Initialized execution: $execution_id"
    
    # Initialize state
    state_init "$execution_dir" "$workflow_file" "$input_data"
    
    echo "$execution_dir"
}

# Execute workflow step
execute_step() {
    local execution_dir="$1"
    local step_id="$2"
    local workflow_file="$3"
    
    log_step "Executing step: $step_id"
    
    # Get step definition
    local step_def=$(yq eval ".steps[] | select(.id == \"$step_id\")" "$workflow_file")
    local step_name=$(echo "$step_def" | yq eval '.name' -)
    local step_type=$(echo "$step_def" | yq eval '.type // "prompt"' -)
    
    log_info "Step: $step_name"
    
    # Update state - mark step as running
    state_update_step "$execution_dir" "$step_id" "running"
    
    # Execute based on step type
    case "$step_type" in
        "prompt")
            execute_prompt_step "$execution_dir" "$step_id" "$workflow_file"
            ;;
        "loop")
            execute_loop_step "$execution_dir" "$step_id" "$workflow_file"
            ;;
        "parallel")
            execute_parallel_step "$execution_dir" "$step_id" "$workflow_file"
            ;;
        "human_review")
            execute_human_review_step "$execution_dir" "$step_id" "$workflow_file"
            ;;
        *)
            log_error "Unknown step type: $step_type"
            return 1
            ;;
    esac
    
    local step_result=$?
    
    if [[ $step_result -eq 0 ]]; then
        state_update_step "$execution_dir" "$step_id" "completed"
        log_success "Step completed: $step_id"
    else
        state_update_step "$execution_dir" "$step_id" "failed"
        log_error "Step failed: $step_id"
        return 1
    fi
    
    return 0
}

# Execute prompt-based step
execute_prompt_step() {
    local execution_dir="$1"
    local step_id="$2"
    local workflow_file="$3"
    
    # Get prompt path and inputs
    local prompt_path=$(yq eval ".steps[] | select(.id == \"$step_id\") | .prompt" "$workflow_file")
    local step_inputs=$(yq eval ".steps[] | select(.id == \"$step_id\") | .inputs" "$workflow_file" -o=json)
    
    # Resolve input template variables
    step_inputs=$(resolve_template_vars "$execution_dir" "$step_inputs")
    
    # Create step output directory
    local step_output_dir="$execution_dir/outputs/$step_id"
    mkdir -p "$step_output_dir"
    
    # Execute prompt
    log_info "Running prompt: $prompt_path"
    
    # Use prompt-runner to execute
    if prompt_run "$REPO_ROOT/$prompt_path" "$step_inputs" "$step_output_dir"; then
        # Store outputs in state
        state_save_outputs "$execution_dir" "$step_id" "$step_output_dir"
        return 0
    else
        log_error "Prompt execution failed"
        return 1
    fi
}

# Execute loop step
execute_loop_step() {
    local execution_dir="$1"
    local step_id="$2"
    local workflow_file="$3"
    
    local max_iterations=$(yq eval ".steps[] | select(.id == \"$step_id\") | .max_iterations" "$workflow_file")
    local continue_condition=$(yq eval ".steps[] | select(.id == \"$step_id\") | .continue_if" "$workflow_file")
    
    log_info "Loop step: max $max_iterations iterations"
    
    local iteration=1
    while [[ $iteration -le $max_iterations ]]; do
        log_info "Iteration $iteration of $max_iterations"
        
        # Execute loop body (treat as prompt step)
        if ! execute_prompt_step "$execution_dir" "$step_id" "$workflow_file"; then
            log_error "Loop iteration $iteration failed"
            return 1
        fi
        
        # Check continue condition
        if [[ -n "$continue_condition" ]]; then
            local should_continue=$(eval_condition "$execution_dir" "$continue_condition" "$iteration")
            if [[ "$should_continue" != "true" ]]; then
                log_info "Loop condition not met, stopping"
                break
            fi
        fi
        
        ((iteration++))
    done
    
    log_success "Loop completed after $((iteration - 1)) iterations"
    return 0
}

# Execute parallel step
execute_parallel_step() {
    local execution_dir="$1"
    local step_id="$2"
    local workflow_file="$3"
    
    log_info "Parallel step execution (sequential for now)"
    
    # Get tasks
    local task_count=$(yq eval ".steps[] | select(.id == \"$step_id\") | .tasks | length" "$workflow_file")
    
    for ((i=0; i<task_count; i++)); do
        local task_id=$(yq eval ".steps[] | select(.id == \"$step_id\") | .tasks[$i].id" "$workflow_file")
        log_info "Executing parallel task: $task_id"
        
        # Execute task as sub-step
        if ! execute_prompt_step "$execution_dir" "$task_id" "$workflow_file"; then
            log_error "Parallel task $task_id failed"
            return 1
        fi
    done
    
    return 0
}

# Execute human review step
execute_human_review_step() {
    local execution_dir="$1"
    local step_id="$2"
    local workflow_file="$3"
    
    local review_prompt=$(yq eval ".steps[] | select(.id == \"$step_id\") | .prompt" "$workflow_file")
    
    log_step "Human Review Required"
    echo -e "${CYAN}$review_prompt${NC}"
    
    # Show relevant content for review
    local inputs=$(yq eval ".steps[] | select(.id == \"$step_id\") | .inputs" "$workflow_file" -o=json)
    inputs=$(resolve_template_vars "$execution_dir" "$inputs")
    
    echo "$inputs" | jq -r 'to_entries[] | "\(.key): \(.value)"'
    
    # Use gum to get approval
    if gum confirm "Approve and continue?"; then
        state_update_step "$execution_dir" "$step_id" "approved"
        return 0
    else
        local feedback=$(gum input --placeholder "Provide feedback for revision...")
        echo "$feedback" > "$execution_dir/outputs/$step_id/feedback.txt"
        state_update_step "$execution_dir" "$step_id" "rejected"
        return 1
    fi
}

# Resolve template variables in JSON
resolve_template_vars() {
    local execution_dir="$1"
    local json_data="$2"
    
    # Load state
    local state_file="$execution_dir/state.json"
    
    if [[ ! -f "$state_file" ]]; then
        echo "$json_data"
        return 0
    fi
    
    # Use jq to do the replacement properly
    local resolved=$(echo "$json_data" | jq -c '
        . as $data |
        ($inputs // {}) as $workflow_inputs |
        $data | walk(
            if type == "string" then
                gsub("\\{\\{ inputs\\.topic \\}\\}"; $workflow_inputs.topic // "") |
                gsub("\\{\\{ inputs\\.level \\}\\}"; $workflow_inputs.level // "") |
                gsub("\\{\\{ inputs\\.difficulty \\}\\}"; $workflow_inputs.difficulty // "") |
                gsub("\\{\\{ inputs\\.estimated_time \\}\\}"; $workflow_inputs.estimated_time // "") |
                gsub("\\{\\{ inputs\\.prerequisites \\}\\}"; $workflow_inputs.prerequisites // "") |
                gsub("\\{\\{ steps\\.[^}]* \\}\\}"; "")
            else
                .
            end
        )
    ' --argjson inputs "$(jq -c '.inputs' "$state_file")" 2>/dev/null)
    
    echo "$resolved"
}

# Evaluate condition
eval_condition() {
    local execution_dir="$1"
    local condition="$2"
    local iteration="$3"
    
    # Simple condition evaluation (loop.iteration < max)
    condition="${condition//\{\{ loop.iteration \}\}/$iteration}"
    
    # Evaluate with bc or test
    if [[ "$condition" =~ \< ]]; then
        local left=$(echo "$condition" | cut -d'<' -f1 | xargs)
        local right=$(echo "$condition" | cut -d'<' -f2 | xargs)
        if [[ $left -lt $right ]]; then
            echo "true"
        else
            echo "false"
        fi
    else
        echo "true"
    fi
}

# Run complete workflow
run_workflow() {
    local workflow_file="$1"
    local input_data="${2:-{}}"
    local interactive="${3:-false}"
    
    log_step "Starting workflow execution"
    
    # Validate workflow
    if ! validate_workflow "$workflow_file"; then
        log_error "Workflow validation failed"
        return 1
    fi
    
    # Get inputs interactively if requested
    if [[ "$interactive" == "true" ]]; then
        input_data=$(collect_inputs_interactive "$workflow_file")
    fi
    
    # Initialize execution
    local execution_dir=$(init_workflow "$workflow_file" "$input_data")
    
    log_info "Execution directory: $execution_dir"
    
    # Get workflow steps
    local step_count=$(yq eval '.steps | length' "$workflow_file")
    
    log_info "Workflow has $step_count steps"
    
    # Execute steps sequentially
    for ((i=0; i<step_count; i++)); do
        local step_id=$(yq eval ".steps[$i].id" "$workflow_file")
        
        if ! execute_step "$execution_dir" "$step_id" "$workflow_file"; then
            log_error "Workflow failed at step: $step_id"
            
            # Handle failure
            local on_failure=$(yq eval ".steps[$i].on_failure // \"abort\"" "$workflow_file")
            
            if [[ "$on_failure" == "abort" ]]; then
                state_update_workflow "$execution_dir" "failed"
                return 1
            fi
            
            # TODO: Handle retry, skip, or alternate path
        fi
        
        # Check for checkpoint
        if should_save_checkpoint "$workflow_file" "$step_id"; then
            state_save_checkpoint "$execution_dir"
            log_success "Checkpoint saved after $step_id"
        fi
    done
    
    # Workflow completed
    state_update_workflow "$execution_dir" "completed"
    log_success "Workflow completed successfully!"
    log_info "Execution directory: $execution_dir"
    
    return 0
}

# Collect inputs interactively
collect_inputs_interactive() {
    local workflow_file="$1"
    
    log_step "Collecting workflow inputs"
    
    local inputs_json="{}"
    
    # Get required inputs
    local required_count=$(yq eval '.inputs.required | length' "$workflow_file")
    
    for ((i=0; i<required_count; i++)); do
        local input_name=$(yq eval ".inputs.required[$i].name" "$workflow_file")
        local input_desc=$(yq eval ".inputs.required[$i].description" "$workflow_file")
        local input_example=$(yq eval ".inputs.required[$i].example" "$workflow_file")
        
        local value=$(gum input --placeholder "$input_desc (e.g., $input_example)")
        
        inputs_json=$(echo "$inputs_json" | jq --arg key "$input_name" --arg val "$value" '. + {($key): $val}')
    done
    
    echo "$inputs_json"
}

# Check if checkpoint should be saved
should_save_checkpoint() {
    local workflow_file="$1"
    local step_id="$2"
    
    # Check if step is in checkpoint list
    local checkpoint_steps=$(yq eval '.state.checkpoints[] | .after' "$workflow_file" 2>/dev/null)
    
    if echo "$checkpoint_steps" | grep -q "$step_id"; then
        return 0
    fi
    
    return 1
}

# Resume workflow from checkpoint
resume_workflow() {
    local execution_dir="$1"
    
    log_step "Resuming workflow from checkpoint"
    
    if [[ ! -d "$execution_dir" ]]; then
        log_error "Execution directory not found: $execution_dir"
        return 1
    fi
    
    # Load state
    local state_file="$execution_dir/state.json"
    if [[ ! -f "$state_file" ]]; then
        log_error "State file not found"
        return 1
    fi
    
    local workflow_file=$(jq -r '.workflow.file' "$state_file")
    local current_step=$(jq -r '.workflow.current_step' "$state_file")
    
    log_info "Resuming from step: $current_step"
    
    # TODO: Continue execution from current step
    log_warning "Resume functionality not yet fully implemented"
    
    return 0
}

# List available workflows
list_workflows() {
    log_step "Available Workflows"
    
    local templates_dir="$SCRIPT_DIR/templates"
    
    if [[ ! -d "$templates_dir" ]]; then
        log_warning "No workflow templates found"
        return 0
    fi
    
    find "$templates_dir" -name "*.yml" -o -name "*.yaml" | while read -r workflow_file; do
        local name=$(yq eval '.workflow.name' "$workflow_file")
        local desc=$(yq eval '.workflow.description' "$workflow_file")
        local version=$(yq eval '.workflow.version' "$workflow_file")
        
        echo -e "${GREEN}•${NC} ${BOLD}$name${NC} (v$version)"
        echo "  $desc"
        echo "  File: $(basename "$workflow_file")"
        echo
    done
}

# List recent executions
list_executions() {
    local count="${1:-10}"
    
    log_step "Recent Workflow Executions"
    
    local workflows_dir="$REPO_ROOT/work/workflows"
    
    if [[ ! -d "$workflows_dir" ]]; then
        log_warning "No workflow executions found"
        return 0
    fi
    
    find "$workflows_dir" -name "state.json" -type f | sort -r | head -n "$count" | while read -r state_file; do
        local workflow_name=$(jq -r '.workflow.name' "$state_file")
        local execution_id=$(jq -r '.workflow.execution_id' "$state_file")
        local status=$(jq -r '.workflow.status' "$state_file")
        local started=$(jq -r '.workflow.started_at' "$state_file")
        
        local status_icon="●"
        case "$status" in
            "completed") status_icon="${GREEN}✓${NC}" ;;
            "failed") status_icon="${RED}✗${NC}" ;;
            "running") status_icon="${YELLOW}▶${NC}" ;;
        esac
        
        echo -e "$status_icon ${BOLD}$workflow_name${NC} - $execution_id"
        echo "  Started: $started"
        echo "  Status: $status"
        echo "  Path: $(dirname "$state_file")"
        echo
    done
}

# Main command dispatcher
main() {
    local command="${1:-help}"
    shift || true
    
    # Check dependencies first
    if ! check_dependencies; then
        return 1
    fi
    
    case "$command" in
        run)
            local workflow_file="${1:-}"
            local input_data="${2:-{}}"
            local interactive=false
            
            # Parse flags
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --interactive|-i)
                        interactive=true
                        shift
                        ;;
                    --input|-n)
                        input_data="$2"
                        shift 2
                        ;;
                    --input-file|-f)
                        input_data=$(cat "$2")
                        shift 2
                        ;;
                    *)
                        workflow_file="$1"
                        shift
                        ;;
                esac
            done
            
            if [[ -z "$workflow_file" ]]; then
                log_error "Usage: engine.sh run <workflow.yml> [--interactive] [--input JSON]"
                return 1
            fi
            
            run_workflow "$workflow_file" "$input_data" "$interactive"
            ;;
        
        validate)
            local workflow_file="${1:-}"
            if [[ -z "$workflow_file" ]]; then
                log_error "Usage: engine.sh validate <workflow.yml>"
                return 1
            fi
            
            parse_workflow "$workflow_file" && validate_workflow "$workflow_file"
            ;;
        
        resume)
            local execution_dir="${1:-}"
            if [[ -z "$execution_dir" ]]; then
                log_error "Usage: engine.sh resume <execution_dir>"
                return 1
            fi
            
            resume_workflow "$execution_dir"
            ;;
        
        list)
            list_workflows
            ;;
        
        executions)
            local count=10
            if [[ "${1:-}" == "--recent" ]]; then
                count="${2:-10}"
            fi
            list_executions "$count"
            ;;
        
        info)
            local workflow_file="${1:-}"
            if [[ -z "$workflow_file" ]]; then
                log_error "Usage: engine.sh info <workflow.yml>"
                return 1
            fi
            
            log_step "Workflow Information"
            yq eval '.workflow' "$workflow_file"
            ;;
        
        help|--help|-h)
            cat << EOF
${BOLD}Crush Workflow Engine${NC}

${BOLD}USAGE:${NC}
  engine.sh <command> [options]

${BOLD}COMMANDS:${NC}
  run <workflow.yml>         Execute workflow
    --interactive, -i        Collect inputs interactively
    --input JSON, -n JSON    Provide inputs as JSON
    --input-file FILE, -f    Read inputs from file
  
  validate <workflow.yml>    Validate workflow definition
  resume <execution_dir>     Resume from checkpoint
  list                       List available workflows
  executions [--recent N]    List recent executions
  info <workflow.yml>        Show workflow details
  help                       Show this help

${BOLD}EXAMPLES:${NC}
  # Run workflow interactively
  engine.sh run templates/article-quest-creation.yml --interactive
  
  # Run with input JSON
  engine.sh run templates/quest-only.yml --input '{"topic": "Docker", "level": "0011"}'
  
  # Resume failed execution
  engine.sh resume work/workflows/article-quest/execution-20251120-143022
  
  # List available workflows
  engine.sh list

EOF
            ;;
        
        *)
            log_error "Unknown command: $command"
            log_info "Run 'engine.sh help' for usage"
            return 1
            ;;
    esac
}

# Execute if run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
