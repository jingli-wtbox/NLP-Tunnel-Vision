from openai import OpenAI
import argparse
import os
import sys
from dotenv import load_dotenv

def check_job(args):
    job_info = args.openai_client.fine_tuning.jobs.retrieve(args.job_id)
    print(job_info)

def main(args):
    load_dotenv()
    if os.getenv('OPENAI_API_KEY', None) is None:
        print("OPENAI_API_KEY is not set.")
        sys.exit(1)
    
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    args.openai_client = client
    check_job(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Check the status of OpenAI Fine-Tuning Job")
    parser.add_argument("--job_id", type=str, default="ftjob-XaSDpsnnON1MuHYk9RJKe4BM", help="OpenAI Fine-Tuning Job ID")
    args = parser.parse_args()

    main(args)