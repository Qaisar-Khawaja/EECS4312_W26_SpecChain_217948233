"""cleans raw data & make clean dataset"""
import json
import re
import string
from pathlib import Path
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt_tab', quiet=True)

class ReviewCleaner:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def remove_duplicates(self, reviews):
        """Remove duplicate reviews based on review text"""
        seen = set()
        unique_reviews = []
        
        for review in reviews:
            review_text = review.get('content', '') or review.get('text', '') or review.get('review', '')
            if review_text and review_text not in seen:
                seen.add(review_text)
                unique_reviews.append(review)
        
        return unique_reviews
    
    def remove_empty_and_short(self, reviews, min_length=3):
        """Remove empty entries and extremely short reviews"""
        filtered = []
        
        for review in reviews:
            review_text = review.get('content', '') or review.get('text', '') or review.get('review', '')
            if review_text and len(review_text.strip()) >= min_length:
                filtered.append(review)
        
        return filtered
    
    def remove_emojis(self, text):
        """Remove emojis and special characters"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        return emoji_pattern.sub(r'', text)
    
    def convert_numbers_to_text(self, text):
        """Convert numbers to text representation"""
        number_map = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
            '10': 'ten'
        }
        
        for num, word in number_map.items():
            text = re.sub(r'\b' + num + r'\b', word, text)
        
        text = re.sub(r'\d+', '', text)
        
        return text
    
    def clean_text(self, text):
        """Apply all text cleaning steps"""
        if not text:
            return ""
        
        text = self.remove_emojis(text)
        text = re.sub(r'http\S+|www.\S+', '', text)
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = self.convert_numbers_to_text(text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def remove_stopwords_and_lemmatize(self, text):
        """Remove stop words and lemmatize tokens"""
        if not text:
            return ""
        
        tokens = word_tokenize(text)
        
        cleaned_tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words and len(token) > 1
        ]
        
        return ' '.join(cleaned_tokens)
    
    def clean_review(self, review):
        """Clean a single review and keep only the final version"""
        review_text = review.get('content', '') or review.get('text', '') or review.get('review', '')
        
        # 1. Run the cleaning logic
        cleaned_text = self.clean_text(review_text)
        cleaned_text = self.remove_stopwords_and_lemmatize(cleaned_text)
        
        # 2. Create the clean object
        cleaned_review = review.copy()
        
        # CRITICAL: Replace 'content' with the cleaned version
        # This ensures the 'content' field IS the clean data
        cleaned_review['content'] = cleaned_text
        
        # Remove the extra fields to keep the file strictly "Clean"
        if 'original_text' in cleaned_review: del cleaned_review['original_text']
        if 'cleaned_text' in cleaned_review: del cleaned_review['cleaned_text']
        
        return cleaned_review


def main():
    print("Starting review cleaning process...")
    
    input_path = Path('data/reviews_raw.jsonl')
    output_path = Path('data/reviews_clean.jsonl')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not input_path.exists():
        print(f"Error: {input_path} not found!")
        return
    
    print(f"Loading reviews from {input_path}...")
    reviews = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                reviews.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    
    original_count = len(reviews)
    print(f"Loaded {original_count} raw reviews")
    
    cleaner = ReviewCleaner()
    
    print("Removing duplicates...")
    reviews = cleaner.remove_duplicates(reviews)
    after_dedup = len(reviews)
    print(f"After removing duplicates: {after_dedup} reviews")
    
    print("Removing empty and extremely short reviews...")
    reviews = cleaner.remove_empty_and_short(reviews, min_length=10)
    print(f"After removing empty/short reviews: {len(reviews)} reviews")
    
    print("Cleaning review texts...")
    cleaned_reviews = []
    for i, review in enumerate(reviews):
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(reviews)} reviews...")
        
        cleaned_review = cleaner.clean_review(review)
        
        if cleaned_review['content'] and len(cleaned_review['content'].split()) >= 3:
            cleaned_reviews.append(cleaned_review)
    
    final_count = len(cleaned_reviews)
    print(f"After final cleaning: {final_count} reviews")
    
    print(f"Saving cleaned reviews to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        for review in cleaned_reviews:
            f.write(json.dumps(review, ensure_ascii=False) + '\n')
    
    # Create metadata automatically
    # print("Creating metadata file...")
    # metadata = {
    #     "app_information": {
    #         "app_name": "",
    #         "package_name": "",
    #         "platform": "Google Play Store"
    #     },
    #     "dataset_information": {
    #         "raw_dataset_size": original_count,
    #         "cleaned_dataset_size": final_count,
    #         "collection_method": "UPDATE_THIS",
    #         "data_format": "JSONL (JSON Lines)"
    #     },
    #     "cleaning_decisions": {
    #         "duplicate_removal": "Removed exact duplicate reviews based on text content",
    #         "empty_removal": "Removed reviews with empty or null text",
    #         "short_review_threshold": "Removed reviews shorter than 10 characters",
    #         "emoji_removal": "Removed all Unicode emojis",
    #         "special_characters": "Removed all non-alphanumeric characters except spaces",
    #         "number_handling": "Converted common numbers (0-10) to text, removed others",
    #         "case_normalization": "Converted all text to lowercase",
    #         "whitespace": "Normalized multiple spaces to single space",
    #         "stopwords": "Removed English stop words using NLTK stopwords corpus",
    #         "lemmatization": "Applied WordNet lemmatization to all tokens",
    #         "minimum_cleaned_length": "Required at least 3 words after cleaning"
    #     },
    #     "statistics": {
    #         "original_reviews": original_count,
    #         "after_deduplication": after_dedup,
    #         "final_cleaned_reviews": final_count,
    #         "removal_rate_percent": round((1 - final_count/original_count) * 100, 2) if original_count > 0 else 0
    #     }
    # }
    
    # metadata_path = Path('data/dataset_metadata.json')
    # with open(metadata_path, 'w', encoding='utf-8') as f:
    #     json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"CLEANING COMPLETE!")
    print(f"{'='*60}")
    print(f"Original reviews: {original_count}")
    print(f"After deduplication: {after_dedup}")
    print(f"Final cleaned reviews: {final_count}")
    print(f"\n⚠️  IMPORTANT: Edit data/dataset_metadata.json to add:")
    print(f"   - app_name")
    print(f"   - package_name")
    print(f"   - collection_method")


if __name__ == "__main__":
    main()