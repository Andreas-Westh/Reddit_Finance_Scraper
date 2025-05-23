import praw # https://praw.readthedocs.io/en/latest/
import os
from dotenv import load_dotenv
import nltk
import re
from sentida import Sentida
import pandas as pd

#grab .env
load_dotenv()

# load in praw through .env
reddit = praw.Reddit(
    client_id    = os.getenv("CLIENT_ID"),
    client_secret= os.getenv("CLIENT_SECRET"),
    username     = os.getenv("USERNAME"),
    password     = os.getenv("PASSWORD"),
    user_agent   = os.getenv("USER_AGENT"),
    check_for_async=False
)

# check for success
print(reddit.user.me())


# load subreddit instances
subreddit = reddit.subreddit('Wallstreetbetsnew')

# sorting the posts / how many amounts to scrape
# check submissions class in documentation for more info
submissions = list(subreddit.hot(limit=100)) # must be a list so we can iterate through it multiple times
for submission in submissions:
    print(f"submission.title: {submission.title}")

# tokenize the words in the title
word_collection=[]
for submission in submissions:
    title_words = nltk.word_tokenize(submission.title,language="english")
    word_collection.extend(title_words)
    
# find out if a token is a ticker
ticker_pattern = re.compile(r'^[A-Z]{4}$')
potential_tickers = []
for word in word_collection:
    if ticker_pattern.match(word):
        potential_tickers.append(word)

# get titles that include the ticker
ticker_titles_rows = []

for submission in submissions:
    for ticker in potential_tickers:
        if ticker in submission.title:
            ticker_titles_rows.append({
                    "ticker": ticker,
                    "title": submission.title
                 })
           # break # doesnt match same submission more than once, could be removed
            
# create a df for above loop hell
ticker_titles = pd.DataFrame(ticker_titles_rows, columns=["ticker","title"])

# get sentiment
ticker_titles["sentiment"] = ticker_titles["title"].apply(lambda x: Sentida().sentida(x,output="mean",normal=False))



# TO DO 
# With potential_tickers, get a sentiment score for sentences that include them