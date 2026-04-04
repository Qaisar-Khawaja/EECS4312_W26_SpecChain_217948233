"""imports or reads your raw dataset; if you scraped, include scraper here"""
# Step 1: Import required packages (As per Prof's instructions)
from google_play_scraper import app
import pandas as pd
import numpy as np
from google_play_scraper import Sort, reviews_all
import json
import os

# Step 2: Set the App Id (Fixed for Headspace)
APP_ID = 'com.getsomeheadspace.android' 

# Step 3: Scrape the Reviews (As per Prof's instructions)
print(f"Scraping reviews for {APP_ID}...")
us_reviews = reviews_all(
    APP_ID,
    sleep_milliseconds=0, 
    lang='en', 
    country='us', 
    sort=Sort.NEWEST, 
)

# Step 4: Put the Reviews into Pandas DataFrame (As per Prof's instructions)
df_busu = pd.DataFrame(np.array(us_reviews), columns=['review'])
df_busu = df_busu.join(pd.DataFrame(df_busu.pop('review').tolist()))

# --- PROJECT REQUIREMENT: SAVE THE DATA ---
# We must save this DataFrame to data/reviews_raw.jsonl
if not os.path.exists('data'):
    os.makedirs('data')

# Save to JSONL format (orient='records', lines=True makes it .jsonl)
# We take the first 5000 if the app has more, as per Task 2 instructions
df_busu.head(5000).to_json('data/reviews_raw.jsonl', orient='records', lines=True)

print(f"Success! {len(df_busu.head(5000))} reviews saved to data/reviews_raw.jsonl")