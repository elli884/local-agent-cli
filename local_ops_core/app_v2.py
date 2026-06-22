import argparse
import sys
from local_ops_core.structured_parser import extract_structured_data, LogAnalysis
from local_ops_core.model_fallback import route_and_execute

def main():
    parser = argparse.ArgumentParser(description="LocalOps Core Pipeline v2.0 - JSON Engine")
    parser.add_argument('--analyze_log', type=str, required=True, help='The log string to analyze')
    args = parser.parse_args()
    
    print("Starting intelligent analysis pipeline...")
    try:
        # Run dynamic routing to process the log text through the optimal model
        print("Running model routing and execution...")
        routing_result = route_and_execute(f"Provide a quick breakdown of this log: {args.analyze_log}")
        print(f"Routing Output: {routing_result}\n")
        
        # Run structured JSON extraction and validation
        print("Running structured data extraction...")
        parsed_data: LogAnalysis = extract_structured_data(args.analyze_log)
        print(parsed_data.model_dump_json(indent=4))
        
    except Exception as e:
        print(f"Critical pipeline error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
# Execution in terminal: uv run python -m local_ops_core.app_v2 --analyze_log "CRITICAL: Database connection lost on port 5432 - Code 1012"