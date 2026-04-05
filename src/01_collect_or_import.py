"""imports or reads your raw dataset; if you scraped, include scraper here"""
import pandas as pd
import numpy as np
from google_play_scraper import Sort, reviews_all
import json
import os

# Step 1: Set the App Id
APP_ID = 'com.getsomeheadspace.android' 

# Step 2: Scrape the Reviews
print(f"Scraping reviews for {APP_ID}:")
raw_reviews = reviews_all(
    APP_ID,
    sleep_milliseconds=0, 
    lang='en', 
    country='us', 
    sort=Sort.NEWEST, 
)

# How many reviews are there in total:
total_available = len(raw_reviews)
print(f"Total reviews scraped: {total_available}")

# Step 3: Put the Reviews into Pandas DataFrame
df_reviews = pd.DataFrame(np.array(raw_reviews), columns=['review'])
df_reviews = df_reviews.join(pd.DataFrame(df_reviews.pop('review').tolist()))

# Step 5: Ensure data/ directory exists
os.makedirs("data", exist_ok=True)

# Step 6: Save maximum 5000 reviews or fewer if not available
max_reviews = min(total_available, 5000)
df_reviews.iloc[:max_reviews].to_json(
    "data/reviews_raw.jsonl",
    orient="records",
    lines=True
)
print(f"Saved {max_reviews} reviews to data/reviews_raw.jsonl")