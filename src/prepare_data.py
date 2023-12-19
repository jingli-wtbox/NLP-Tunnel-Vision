import pandas as pd
import json
from tqdm.auto import tqdm
from threading import Thread

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
                            "newsdesk": df_articles[df_articles['uniqueID'] == article_id]['newsdesk'], 
                            "section": df_articles[df_articles['uniqueID'] == article_id]['section'], 
                            "subsection": df_articles[df_articles['uniqueID'] == article_id]['subsection'], 
                            "headline": df_articles[df_articles['uniqueID'] == article_id]['headline'], 
                            "keywords": df_articles[df_articles['uniqueID'] == article_id]['keywords'],
                            "abstract": df_articles[df_articles['uniqueID'] == article_id]['abstract']
                            })
                    print(f"newsdesk: {df_articles[df_articles['uniqueID'] == article_id]['newsdesk'].to_list()[0].strip()}")
                    print(f"line: {line}")
                    break
                f_writer.write(json.dumps(line) + '\n')
    print(f"Finish writing user reading historys in window {window_size}")


def main():
    print("Step 1: start to read data from csv files")
    df_raw_articles = pd.read_csv('data/raw/nyt-articles-2020.csv')
    df_articles = df_raw_articles[['uniqueID', 'newsdesk', 'section', 'subsection',  'headline', 'abstract', 'keywords' ]]
    df_raw_comments = pd.read_csv('data/raw/nyt-comments-2020.csv')
    df_comments = df_raw_comments[['commentBody', 'userID', 'articleID']]

    pairs_window_size = [(5, 'data/processed/nyt-2020-ws5.jsonl'), 
                         (10, 'data/processed/nyt-2020-ws10.jsonl'), 
                         (15, 'data/processed/nyt-2020-ws15.jsonl'), 
                         (20, 'data/processed/nyt-2020-ws20.jsonl'), 
                         (25, 'data/processed/nyt-2020-ws25.jsonl')]


    print("Step 2: start to convert data to jsonl files") 
    # create five threads to convert data
    # for window_size, output_path in pairs_window_size:
    #     Thread(target=convert_to_jsonl, name=f"Convertor-{window_size}", args=(window_size, df_articles, df_comments, output_path)).start()
    #     break
    convert_to_jsonl(5, df_articles, df_comments, 'data/processed/nyt-2020-ws5.jsonl')

    print("Done!")

    

if __name__ == '__main__':
    main()