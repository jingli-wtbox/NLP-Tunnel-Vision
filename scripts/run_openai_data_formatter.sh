#!/bin/bash

python src/openai_data_formatter.py --input_file_prefix data/processed/nyt-2020-ws --output_file data/processed/nyt-2020-openai.jsonl  --limit_rows 10