"""automated persona generation pipeline"""
import os
import json
from groq import Groq
import random

# Initialize the Groq client
client = Groq(api_key="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")

def run_pipeline():
    print("============================================================================")
    print("TASK 4.1: GROUPING REVIEWS INTO THEMES")
    print("============================================================================")
    
    reviews_all = []
    with open('data/reviews_clean.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            reviews_all.append(json.loads(line))
    
    # Process reviews I only used small chunks because tokens are limited
    BATCH_SIZE = 300
    NUM_BATCHES = 3 
    
    # Becuase of small batches I shuffled to remove bias of ordered
    random.seed()
    shuffled_reviews = random.sample(reviews_all, len(reviews_all))
    all_batch_results = []
    
    for batch_num in range(NUM_BATCHES):
        start_index = batch_num * BATCH_SIZE
        end_index = min(start_index + BATCH_SIZE, len(shuffled_reviews))
        batch_reviews = shuffled_reviews[start_index:end_index]
        
        formatted_data = "\n".join([f"ID: {r['reviewId']} | Content: {r['content']}" for r in batch_reviews])
        
        if batch_num == 0:
            with open('prompts/prompt_auto.json', 'r', encoding='utf-8') as f:
                prompt_config = json.load(f)
        
        grouping_completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": prompt_config["prompt"]},
                {"role": "user", "content": f"Review Data:\n{formatted_data}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.8
        )
        all_batch_results.append(json.loads(grouping_completion.choices[0].message.content))

    # MERGE & KEEP the TOP 5
    merged_themes = {}
    for batch_result in all_batch_results:
        for theme in batch_result.get('themes', []):
            theme_name = theme['name']
            matched = False
            for existing_name in merged_themes.keys():
                existing_keywords = set(existing_name.lower().split())
                new_keywords = set(theme_name.lower().split())
                if len(existing_keywords & new_keywords) >= 2:
                    merged_themes[existing_name].extend(theme['reviews'])
                    matched = True
                    break
            if not matched:
                merged_themes[theme_name] = theme['reviews']
    
    # Sort themes by size
    sorted_themes = sorted(merged_themes.items(), key=lambda x: len(list(set(x[1]))), reverse=True)[:5]
    
    reviews_map = {r['reviewId']: r['content'] for r in reviews_all}
    final_groups = []
    
    for i, (name, r_ids) in enumerate(sorted_themes, 1):
        unique_ids = list(set(r_ids))
        final_groups.append({
            "group_id": f"G{i}",
            "theme": name,
            "review_ids": unique_ids,
            "example_reviews": [reviews_map[rid] for rid in unique_ids[:2] if rid in reviews_map]
        })
    
    # Save formatted groups
    auto_groups_output = {"groups": final_groups}
    os.makedirs('data', exist_ok=True)
    with open('data/review_groups_auto.json', 'w', encoding='utf-8') as f:
        json.dump(auto_groups_output, f, indent=2)

    print(f" Created exactly {len(final_groups)} groups.")

    print("============================================================================")
    print("TASK 4.2: GENERATING PERSONAS FROM THEMES")
    print("============================================================================")
    
    all_personas = []
    used_names = set()
    
    for group in final_groups:
        group_id = group['group_id']
        theme_name = group['theme']
        r_ids = group['review_ids'][:8]
        context_text = "\n".join([f"ID: {rid} | {reviews_map[rid]}" for rid in r_ids if rid in reviews_map])
        
        enhanced_persona_prompt = (
            prompt_config["persona_prompt"] + 
            f"\n\nReturn a JSON object following this structure exactly: "
            f"{{'name': '', 'description': '', 'goals': [], 'pain_points': [], 'context': [], 'constraints': []}}. "
            f"Avoid names: {list(used_names)}"
        )
        
        persona_completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": enhanced_persona_prompt},
                {"role": "user", "content": f"Theme: {theme_name}\nReviews:\n{context_text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.9
        )
        
        res = json.loads(persona_completion.choices[0].message.content)
        
        # Formatting
        persona_obj = {
            "id": f"P{group_id[1:]}",
            "name": res.get('name', 'User Persona'),
            "description": res.get('description', ''),
            "derived_from_group": group_id,
            "goals": res.get('goals', []),
            "pain_points": res.get('pain_points', []),
            "context": res.get('context', []),
            "constraints": res.get('constraints', []),
            "evidence_reviews": r_ids
        }
        
        used_names.add(persona_obj['name'])
        all_personas.append(persona_obj)
        print(f"Created persona: {persona_obj['name']}")
    
    # Save personas
    os.makedirs('personas', exist_ok=True)
    with open('personas/personas_auto.json', 'w', encoding='utf-8') as f:
        json.dump({"personas": all_personas}, f, indent=2)

if __name__ == "__main__":
    run_pipeline()