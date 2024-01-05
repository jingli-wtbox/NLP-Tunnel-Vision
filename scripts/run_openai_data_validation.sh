#!/bin/bash

# This script checks the format of the training data for OpenAI model fine-tuning.

python src/openai_data_validation.py --data_path data/processed/nyt-2020-openai.jsonl