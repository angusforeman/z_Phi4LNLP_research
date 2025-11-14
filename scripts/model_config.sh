#!/bin/bash
# Model configuration utility for testing different quantization levels

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$PROJECT_DIR/.env"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

function print_usage() {
    echo "Model Configuration Utility"
    echo ""
    echo "Usage: $0 [command] [model_name]"
    echo ""
    echo "Commands:"
    echo "  list              List available models"
    echo "  current           Show current configuration"
    echo "  set <model>       Set the model (e.g., phi4:latest, mistral:7b)"
    echo "  info <model>      Show model information"
    echo "  test <query>      Test current model with a query"
    echo "  benchmark         Run quick benchmark (5 queries)"
    echo ""
    echo "Examples:"
    echo "  $0 list"
    echo "  $0 set phi4:latest"
    echo "  $0 info phi4:latest"
    echo "  $0 test 'count all customers'"
    echo "  $0 benchmark"
}

function list_models() {
    echo -e "${BLUE}Available Ollama models:${NC}"
    ollama list
}

function show_current() {
    if [ -f "$ENV_FILE" ]; then
        current=$(grep "^MODEL_NAME=" "$ENV_FILE" | cut -d'=' -f2)
        echo -e "${GREEN}Current model:${NC} $current"
        
        # Show model info if it exists
        if ollama list | grep -q "$(echo $current | cut -d':' -f1)"; then
            echo ""
            ollama show "$current" 2>&1 | head -15
        fi
    else
        echo -e "${RED}Error: .env file not found${NC}"
        exit 1
    fi
}

function set_model() {
    local model=$1
    if [ -z "$model" ]; then
        echo -e "${RED}Error: Model name required${NC}"
        echo "Usage: $0 set <model_name>"
        exit 1
    fi
    
    # Check if model exists
    if ! ollama list | grep -q "$(echo $model | cut -d':' -f1)"; then
        echo -e "${YELLOW}Warning: Model '$model' not found locally${NC}"
        echo "Pull it with: ollama pull $model"
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Update .env file
    if [ -f "$ENV_FILE" ]; then
        # Use sed to replace the MODEL_NAME line
        if grep -q "^MODEL_NAME=" "$ENV_FILE"; then
            sed -i "s|^MODEL_NAME=.*|MODEL_NAME=$model|" "$ENV_FILE"
        else
            echo "MODEL_NAME=$model" >> "$ENV_FILE"
        fi
        echo -e "${GREEN}✓ Model set to:${NC} $model"
    else
        echo -e "${RED}Error: .env file not found${NC}"
        exit 1
    fi
}

function show_model_info() {
    local model=${1:-$(grep "^MODEL_NAME=" "$ENV_FILE" | cut -d'=' -f2)}
    
    if ollama list | grep -q "$(echo $model | cut -d':' -f1)"; then
        echo -e "${BLUE}Model information for: $model${NC}"
        ollama show "$model"
    else
        echo -e "${RED}Model '$model' not found${NC}"
        echo "Available models:"
        ollama list
        exit 1
    fi
}

function test_query() {
    local query=$1
    if [ -z "$query" ]; then
        echo -e "${RED}Error: Query required${NC}"
        echo "Usage: $0 test '<natural language query>'"
        exit 1
    fi
    
    current=$(grep "^MODEL_NAME=" "$ENV_FILE" | cut -d'=' -f2)
    echo -e "${BLUE}Testing with model:${NC} $current"
    echo -e "${BLUE}Query:${NC} $query"
    echo ""
    
    cd "$PROJECT_DIR"
    time ./venv/bin/python src/cli.py "$query"
}

function run_quick_benchmark() {
    current=$(grep "^MODEL_NAME=" "$ENV_FILE" | cut -d'=' -f2)
    echo -e "${BLUE}Running quick benchmark with model:${NC} $current"
    echo ""
    
    cd "$PROJECT_DIR"
    
    queries=(
        "show all customers"
        "count all products"
        "list all orders"
        "show customers with their orders"
        "count orders per customer"
    )
    
    total_time=0
    success_count=0
    
    for i in "${!queries[@]}"; do
        query="${queries[$i]}"
        echo -e "${YELLOW}[$((i+1))/${#queries[@]}]${NC} Testing: $query"
        
        start=$(date +%s.%N)
        if ./venv/bin/python src/cli.py "$query" > /tmp/test_output.sql 2>&1; then
            end=$(date +%s.%N)
            duration=$(echo "$end - $start" | bc)
            total_time=$(echo "$total_time + $duration" | bc)
            success_count=$((success_count + 1))
            echo -e "  ${GREEN}✓ Success${NC} (${duration}s)"
            cat /tmp/test_output.sql | grep "SELECT\|INSERT\|UPDATE\|DELETE" | head -1
        else
            end=$(date +%s.%N)
            duration=$(echo "$end - $start" | bc)
            echo -e "  ${RED}✗ Failed${NC} (${duration}s)"
        fi
        echo ""
    done
    
    avg_time=$(echo "scale=3; $total_time / ${#queries[@]}" | bc)
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Benchmark Summary${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "Model:        $current"
    echo -e "Queries:      ${#queries[@]}"
    echo -e "Successful:   $success_count"
    echo -e "Total time:   ${total_time}s"
    echo -e "Average time: ${avg_time}s"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Main script logic
case "${1:-}" in
    list)
        list_models
        ;;
    current)
        show_current
        ;;
    set)
        set_model "$2"
        ;;
    info)
        show_model_info "$2"
        ;;
    test)
        test_query "$2"
        ;;
    benchmark)
        run_quick_benchmark
        ;;
    -h|--help|"")
        print_usage
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        print_usage
        exit 1
        ;;
esac
