from twscrape import API, gather
from twscrape.logger import set_log_level
import json
import os

def clean_mentioned_users(mentioned_users):
    return [
        {"displayname": user["displayname"], "username": user["username"]}
        for user in mentioned_users
    ]

async def searchTweets(keyword="", folder=""):
    api = API()
    
    # q = "DeFi since:2023-01-01 until:2023-08-31"
    # q = keyword.lower()
    q = f"{keyword.lower()} since:2023-01-01 until:2023-12-31"
    
    tweets = []
    async for rep in api.search(q, 1000):
        data = rep.json()
        data = json.loads(rep.json())
        tweets.append(data)
    
    for tweet in tweets:
        if "mentionedUsers" in tweet:
            tweet["mentionedUsers"] = clean_mentioned_users(tweet["mentionedUsers"])

    file_path = os.path.join(folder, 'tweets.json')
    
    with open(file_path, 'a', encoding='utf-8') as json_file:
        json.dump(tweets, json_file, ensure_ascii=False, indent=4)
