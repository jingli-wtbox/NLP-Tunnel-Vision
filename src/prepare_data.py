import pandas as pd
import json
from tqdm.auto import tqdm
from threading import Thread
import argparse

def convert_to_jsonl(window_size, df_articles, df_comments, output_path):
    with open(output_path, 'w') as f_writer:
        list_user = df_comments['userID'].unique().tolist()
        for user in tqdm(list_user, total=len(list_user), desc=f"write user reading historys in window {window_size}" ): 
            df_user = df_comments[df_comments['userID'] == user]
            if df_user.shape[0] >= window_size:     
                line = {"userID": user, "window_size": window_size, "records_article_comment": []}           
                for i in range(window_size):
                    article_id = df_user.iloc[i]['articleID']
                    line['records_article_comment'].append({
                            "commentBody": df_user.iloc[i]['commentBody'],
                            "newsdesk": str(df_articles[df_articles['uniqueID'] == article_id]['newsdesk'].values[0]).strip(), 
                            "section": str(df_articles[df_articles['uniqueID'] == article_id]['section'].values[0]).strip(), 
                            "subsection": str(df_articles[df_articles['uniqueID'] == article_id]['subsection'].values[0]).strip(), 
                            "headline": str(df_articles[df_articles['uniqueID'] == article_id]['headline'].values[0]).strip(), 
                            "keywords": str(df_articles[df_articles['uniqueID'] == article_id]['keywords'].values[0]).strip(),
                            "abstract": str(df_articles[df_articles['uniqueID'] == article_id]['abstract'].values[0]).strip()
                            })
                f_writer.write(json.dumps(line) + '\n')
    print(f"Finish writing user reading historys in window {window_size}")


def main(args):
    print("Step 1: start to read data from csv files")

    df_articles = pd.read_csv(args.raw_articles_path)[args.columns_article]
    df_comments = pd.read_csv(args.raw_comments_path)[args.columns_comment]

    # remove rows that commentBody less than 10 words
    df_comments = df_comments[df_comments['commentBody'].str.split().str.len() >= args.num_words_threshold]


    pairs_window_size = []
    for window_size in args.window_sizes:
        output_path = args.output_prefix + str(window_size) + '.jsonl'
        pairs_window_size.append((window_size, output_path))
    

    print("Step 2: start to convert data to jsonl files") 
    # create five threads to convert data
    list_threads = []
    for window_size, output_path in pairs_window_size:
        list_threads.append(
            Thread(target=convert_to_jsonl, name=f"Convertor-{window_size}", args=(window_size, df_articles, df_comments, output_path)).start()
        )
    
    for thread in list_threads:
        thread.join()

    print("Done!")


    

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Prepare data for NLP-Tunnel-Vision")
    parser.add_argument('--window_sizes', type=list, default=[5, 10, 15, 20, 25], help='window size of articles read by user')
    parser.add_argument('--raw_articles_path', type=str, default='data/raw/nyt-articles-2020.csv', help='path of raw articles csv file')
    parser.add_argument('--raw_comments_path', type=str, default='data/raw/nyt-comments-2020.csv', help='path of raw comments csv file')
    parser.add_argument('--columns_article', type=list, default=['uniqueID', 'newsdesk', 'section', 'subsection',  'headline', 'abstract', 'keywords' ], help='columns of articles')
    parser.add_argument('--columns_comment', type=list, default=['commentBody', 'userID', 'articleID'], help='columns of comments')
    parser.add_argument('--output_prefix', type=str, default='data/processed/nyt-2020-ws', help='prefix of output jsonl files')
    parser.add_argument('--num_words_threshold', type=int, default=10, help='threshold of commentBody length')
    args = parser.parse_args()

    main(args)