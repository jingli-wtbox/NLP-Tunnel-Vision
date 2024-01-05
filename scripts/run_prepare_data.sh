#!/bin/bash

# This script is used to prepare the data for the NLP-Tunnel-Vision project.
python src/prepare_data.py --raw_articles_path data/raw/nyt-articles-2020.csv --raw_comments_path data/raw/nyt-comments-2020.csv --output_prefix data/processed/nyt-2020-ws --limit_rows 2000