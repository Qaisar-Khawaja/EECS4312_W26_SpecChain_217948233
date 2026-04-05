"""cleans raw data & make clean dataset"""
import json
import re
from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# STEP 1: Download required language processing tools
print("Downloading language processing tools...")
nltk.download('punkt', quiet=True)     
nltk.download('stopwords', quiet=True)  
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True) 
nltk.download('punkt_tab', quiet=True)


class ReviewCleaner:
    
    def __init__(self):
        # This tool converts words to their base form 
        self.lemmatizer = WordNetLemmatizer()
        # These are common English words we'll remove 
        self.stop_words = set(stopwords.words('english'))
    
    # DUPLICATE REMOVAL
    def remove_duplicates(self, reviews):
        """
        Remove duplicate reviews based on the review text.
        - We keep a set of all review texts we've seen
        - If we see the same text again, we skip it
        """
        seen = set()  # Track what we've already seen
        unique_reviews = []  # Store only unique ones
        
        for review in reviews:
            # Get the review text
            review_text = review.get('content', '') or review.get('text', '') or review.get('review', '')
            # If we haven't seen this exact text before, keep it
            if review_text and review_text not in seen:
                seen.add(review_text)
                unique_reviews.append(review)
        
        return unique_reviews
    
    # SHORT/EMPTY REVIEW REMOVAL
    def remove_empty_and_short(self, reviews, min_length=10):
        """
        Remove reviews that are empty or too short to be useful.
        We want reviews with at least 10 characters.
        """
        filtered = []
        
        for review in reviews:
            review_text = review.get('content', '') or review.get('text', '') or review.get('review', '')
            if review_text and len(review_text.strip()) >= min_length:
                filtered.append(review)
        
        return filtered
    
    # EMOJI REMOVAL
    def remove_emojis(self, text):
        """
        Remove all emojis and special Unicode characters.
        """
        # This pattern matches all common emoji ranges
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F300-\U0001F5FF"  # Symbols & pictographs
            "\U0001F680-\U0001F6FF"  # Transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # Flags
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251"  # Enclosed characters
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.sub(r'', text)
    

    # NUMBER TO TEXT CONVERSION
    def convert_numbers_to_text(self, text):
        # Map of numbers to words
        number_map = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
            '10': 'ten'
        }
        # Replace each number with its word
        for num, word in number_map.items():
            text = re.sub(r'\b' + num + r'\b', word, text)
        # Remove any remaining numbers
        text = re.sub(r'\d+', '', text)
        return text
    
    # MAIN TEXT CLEANING
    def clean_text(self, text):
        if not text:
            return ""
        
        # Step 1: Remove emojis
        text = self.remove_emojis(text)
    
        # Step 2: Remove URLs 
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Step 3: Keep only letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Step 4: Convert numbers to words
        text = self.convert_numbers_to_text(text)
        
        # Step 5: Convert to lowercase
        text = text.lower()
        
        # Step 6: Replace multiple spaces with a single space and trim
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    # STOPWORD REMOVAL & LEMMATIZATION
    def remove_stopwords_and_lemmatize(self, text):
        if not text:
            return ""
        
        # Split the text into individual words (tokens)
        tokens = word_tokenize(text)
        
        # Process each word:
        # 1. Convert to base form (lemmatize)
        # 2. Keep only if it's not a stopword and has more than 1 character
        cleaned_tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words and len(token) > 1
        ]
        
        # Put the cleaned words back into a sentence
        return ' '.join(cleaned_tokens)
    
    # COMPLETE REVIEW CLEANING
    def clean_review(self, review):

        # Step 1: Get the review text
        review_text = review.get('content', '') or review.get('text', '') or review.get('review', '')
        
        # Step 2: Apply all cleaning operations
        cleaned_text = self.clean_text(review_text)
        cleaned_text = self.remove_stopwords_and_lemmatize(cleaned_text)
        
        # Step 3: Create a new review object with the cleaned text
        cleaned_review = review.copy()
        cleaned_review['content'] = cleaned_text
        
        # Step 4: Remove any temporary fields we don't need
        if 'original_text' in cleaned_review:
            del cleaned_review['original_text']
        if 'cleaned_text' in cleaned_review:
            del cleaned_review['cleaned_text']
        
        return cleaned_review

# MAIN EXECUTION
def main():
    print("\n" + "="*70)
    print("REVIEW CLEANING PROCESS STARTED")
    print("="*70 + "\n")
    

    # STEP 1: Set up file paths
    input_path = Path('data/reviews_raw.jsonl')
    output_path = Path('data/reviews_clean.jsonl')
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Create directory if needed
    
    # Check if input file exists
    if not input_path.exists():
        print(f"Error: {input_path} not found!")
        print("Please make sure your raw reviews file exists.")
        return
    
    # STEP 2: Load all reviews from the input file
    print(f"Loading reviews from {input_path}...")
    reviews = []
    
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                reviews.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    
    original_count = len(reviews)
    print(f"Loaded {original_count} raw reviews\n")
    
    cleaner = ReviewCleaner()
    
  
    # STEP 3: Remove duplicate reviews
    print("Removing duplicate reviews...")
    reviews = cleaner.remove_duplicates(reviews)
    after_dedup = len(reviews)
    removed_dupes = original_count - after_dedup
    print(f"Removed {removed_dupes} duplicates")
    print(f"Remaining: {after_dedup} reviews\n")
    
    # STEP 4: Remove empty and very short reviews
    print("Removing empty and extremely short reviews (< 10 characters)")
    reviews = cleaner.remove_empty_and_short(reviews, min_length=10)
    after_short_removal = len(reviews)
    removed_short = after_dedup - after_short_removal
    print(f"Removed {removed_short} short/empty reviews")
    print(f"Remaining: {after_short_removal} reviews\n")
    
    # STEP 5: Clean each review's text
    print("Cleaning review texts")
    cleaned_reviews = []
    
    for i, review in enumerate(reviews):
        # Show progress every 100 reviews
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{len(reviews)} reviews processed")
        
        # Clean the review
        cleaned_review = cleaner.clean_review(review)
        
        # Only keep if the cleaned text has at least 3 words
        if cleaned_review['content'] and len(cleaned_review['content'].split()) >= 3:
            cleaned_reviews.append(cleaned_review)
    
    final_count = len(cleaned_reviews)
    removed_during_cleaning = after_short_removal - final_count
    print(f"Removed {removed_during_cleaning} reviews that became too short after cleaning")
    print(f"  Final count: {final_count} clean reviews\n")
    
    # STEP 6: Save cleaned reviews to output file
    print(f"Saving cleaned reviews to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        for review in cleaned_reviews:
            f.write(json.dumps(review, ensure_ascii=False) + '\n')
    
    print(f"Successfully saved!\n")
    
    # FINAL SUMMARY
    print("="*70)
    print("CLEANING COMPLETE!")
    print("="*70)
    print(f"\nSUMMARY:")
    print(f" Started with:           {original_count:,} reviews")
    print(f" Removed duplicates:     -{removed_dupes:,} reviews")
    print(f" Removed short/empty:    -{removed_short:,} reviews")
    print(f" Removed after cleaning: -{removed_during_cleaning:,} reviews")
    print(f" Final clean dataset:    {final_count:,} reviews")
    print(f"\n  Data quality: {(final_count/original_count*100):.1f}% of original data retained")
    print(f"\n  Output file: {output_path}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()