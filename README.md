# EECS4312_W26_SpecChain

## Application: Headspace Meditation App
A requirements engineering pipeline comparing manual, automated, and hybrid approaches to extracting user requirements from app store reviews.

## Dataset 
- reviews_raw.jsonl contains the collected 5000 reviews from Google Play Store
- reviews_clean.jsonl contains the cleaned dataset 
- The cleaned dataset contains 4,526 reviews

## Data Collection Method
- Google Play Scraper (`google-play-scraper` Python library) - scraped reviews for Headspace app (`com.getsomeheadspace.android`) from Google Play Store, sorted by newest, English language, US country, maximum 5,000 reviews


## Repository Structure
- data/ contains datasets and review groups (manual, automated, hybrid)
- personas/ contains persona files (manual, automated, hybrid)
- spec/ contains specifications (manual, automated, hybrid)
- tests/ contains validation tests (manual, automated, hybrid)
- metrics/ contains all metric files (manual, automated, hybrid, summary)
- src/ contains executable Python scripts
- reflection/ contains the final reflection
- prompts/ conatains Groq prompts used
- venv/ it is used for eneviornment setup

## How to Run:
When running files individually follow the steps:

Step 1: python3 src/ 01_collect_or_import.py
Step 2: python3 src/ 02_clean.py
Step 3: python3 src/ 05_personas_auto.py
Step 4: python3 src/ 06_spec_generate.py
Step 5: python3 src/ 07_tests_generate.py
Step 6: python3 src/ 08_metrics.py for comparison results which gives a table on terminal

To run all:
python3 src/00_validate_repo.py
python3 src/run_all.py

