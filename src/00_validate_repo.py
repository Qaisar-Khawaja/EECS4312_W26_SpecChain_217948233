"""checks required files/folders exist"""
import os

def validate():
    required_files = [
        # Data
        "data/reviews_raw.jsonl",
        "data/reviews_clean.jsonl",
        "data/review_groups_manual.json",
        "data/review_groups_auto.json",
        "data/review_groups_hybrid.json",
        
        # Personas
        "personas/personas_manual.json",
        "personas/personas_auto.json",
        "personas/personas_hybrid.json",
        
        # Specs
        "spec/spec_manual.md",
        "spec/spec_auto.md",
        "spec/spec_hybrid.md",
        
        # Tests
        "tests/tests_manual.json",
        "tests/tests_auto.json",
        "tests/tests_hybrid.json",
        
        # Metrics
        "metrics/metrics_manual.json",
        "metrics/metrics_auto.json",
        "metrics/metrics_hybrid.json",
        "metrics/metrics_summary.json"
    ]

    print("Checking repository structure")
    missing = 0
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"{file_path} found")
        else:
            print(f"!! MISSING: {file_path}")
            missing += 1

    print("-" * 30)
    if missing == 0:
        print("Repository validation complete: ALL FILES PRESENT")
    else:
        print(f"Repository validation complete: {missing} FILES MISSING")

if __name__ == "__main__":
    validate()