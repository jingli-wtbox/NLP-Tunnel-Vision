import json
import tiktoken # for token counting
import numpy as np
from collections import defaultdict
import argparse


def data_validation(args):
    with open(args.data_path, "r") as f:
        data_openai = [json.loads(line) for line in f.readlines()]
    
    print(f"Total number of examples: {len(data_openai)}")

    # Openai data format error checks
    format_errors = defaultdict(int)

    for ex in data_openai:
        if not isinstance(ex, dict):
            format_errors["data_type"] += 1
            continue
            
        messages = ex.get("messages", None)
        if not messages:
            format_errors["missing_messages_list"] += 1
            continue
            
        for message in messages:
            if "role" not in message or "content" not in message:
                format_errors["message_missing_key"] += 1
            
            if any(k not in ("role", "content", "name", "function_call") for k in message):
                format_errors["message_unrecognized_key"] += 1
            
            if message.get("role", None) not in ("system", "user", "assistant", "function"):
                format_errors["unrecognized_role"] += 1
                
            content = message.get("content", None)
            function_call = message.get("function_call", None)
            
            if (not content and not function_call) or not isinstance(content, str):
                format_errors["missing_content"] += 1
        
        if not any(message.get("role", None) == "assistant" for message in messages):
            format_errors["example_missing_assistant_message"] += 1

    if format_errors:
        print("Found errors:")
        for k, v in format_errors.items():
            print(f"{k}: {v}")
    else:
        print("No errors found")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Training Data Validation for OpenAI Fine-Tuning")
    parser.add_argument("--data_path", type=str, default="data/processed/nyt-2020-openai.jsonl", help="Path to the openai data formating file")

    args = parser.parse_args()
    data_validation(args)