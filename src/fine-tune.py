import openai
import argparse
import yaml
import os
import sys
from types import SimpleNamespace


def fine_tune():
    pass


def main(args):
    pass



if __name__ == '__main__':
    if os.environ.get('OPENAI_API_KEY') is None:
        print("OPENAI_API_KEY is not set.")
        sys.exit(1)
    
    parser = argparse.ArgumentParser("Fine-tune GPT-3 on a dataset.")
    parser.add_argument("--config_file", type=str, default="configure/openai.yaml", help="The model ID to use for fine-tuning.")
    parser.add_argument("--training_file", type=str, default="data/fine-tune.jsonl", help="The path to the data directory.")
    args = parser.parse_args()

    config = yaml.safe_load(open(args.config_file, 'r'))
    args.__dict__.update(config)    

    main(args)
