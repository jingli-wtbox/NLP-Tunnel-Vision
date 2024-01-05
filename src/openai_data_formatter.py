import pandas as pd
import argparse
import sys
import json
import copy
from tqdm import tqdm
from utils import (
    SYSTEM_PROMPT,
    USER_PROMPT
)

def convert_to_openai_data(df_all, output_file):
    with open(output_file, 'w') as f_writer:
        for _, row in tqdm(df_all.iterrows(), total=df_all.shape[0], desc="Convert data to OpenAI format"): 
            user_prompt = copy.deepcopy(USER_PROMPT)
            for ws in range(row['window_size']-1):
                user_prompt +=  f"\n##\nArticle {ws} Headline: " + row['records_article_comment'][ws]['headline']    + \
                                f"\nArticle {ws} Abstract: " + row['records_article_comment'][ws]['abstract']        + \
                                f"\nArticle {ws} Keywords: " + row['records_article_comment'][ws]['keywords']        + \
                                f"\nArticle {ws} Newsdesk: " + row['records_article_comment'][ws]['newsdesk']        + \
                                f"\nArticle {ws} Comment: " + row['records_article_comment'][ws]['commentBody'] 
            user_prompt += "\n##\nNew Article Headline: " + row['records_article_comment'][row['window_size']-1]['headline'] + \
                            "\nNew Article Abstract: " + row['records_article_comment'][row['window_size']-1]['abstract']    + \
                            "\nNew Article Comment:"
       
            messages = {
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    },
                    {
                        "role": "assistant",
                        "content": row['records_article_comment'][row['window_size']-1]['commentBody']
                    }
                ]
            }
            f_writer.write(json.dumps(messages) + '\n')


def main(args):
    df_all = pd.DataFrame()
    for sz in args.window_sizes:
        df  = pd.read_json(args.input_file_prefix + str(sz) + '.jsonl', lines=True)
        df_all = pd.concat([df_all, df], ignore_index=True)

    if df_all.shape[0] == 0:
        print("No data is read.")
        sys.exit(1)

    if args.shuffle:
        print("Data is randomly shuffled.")
        df_all = df_all.sample(frac=1, random_state=42)
    
    df_all = df_all.sample(n=args.limit_rows, random_state=42)

    convert_to_openai_data(df_all, args.output_file)

    print("Done!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Convert data into OpenAI format.")
    parser.add_argument("--input_file_prefix", type=str, default="data/processed/nyt-2020-ws", help="The path to the input file.")
    parser.add_argument("--output_file", type=str, default="data/processed/nyt-2020-openai.jsonl", help="The path to the output file.")
    parser.add_argument("--window_sizes", type=list, default=[5, 10, 15, 20, 25], help="The window sizes of articles read by user.")
    parser.add_argument("--shuffle", type=bool, default=True, help="Whether to shuffle the data.")
    parser.add_argument("--limit_rows", type=int, default=20, help="Limit the number of rows in training file.")

    args = parser.parse_args()
    main(args)

