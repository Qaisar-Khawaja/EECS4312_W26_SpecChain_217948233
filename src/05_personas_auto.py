"""automated persona generation pipeline"""
"""automated persona generation pipeline"""
import os
import json
from groq import Groq

# 1. Initialize the Groq client
client = Groq(api_key="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")

def run_pipeline():
    # --- TASK 4.1: GROUPING ---
    # 2. Load the cleaned reviews
    reviews_all = []
    with open('data/reviews_clean.jsonl', 'r') as f:
        for line in f:
            reviews_all.append(json.loads(line))

    # 3. Sample reviews (Taking every 30th)
    sample = reviews_all[::30][:150]
    formatted_data = "\n".join([f"ID: {r['reviewId']} | Content: {r['content']}" for r in sample])

    # 4. Load the prompt instructions (Both prompts are in here now)
    with open('prompts/prompt_auto.json', 'r') as f:
        prompt_config = json.load(f)

    print("Step 1: Grouping reviews into themes...")

    # 5. Call API for Grouping
    grouping_completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": prompt_config["prompt"]},
            {"role": "user", "content": f"Review Data:\n{formatted_data}"}
        ],
        response_format={"type": "json_object"}
    )

    auto_groups = json.loads(grouping_completion.choices[0].message.content)
    
    # Save groups to data/
    os.makedirs('data', exist_ok=True)
    with open('data/review_groups_auto.json', 'w') as f:
        json.dump(auto_groups, f, indent=2)
    print("Done! Groups saved to data/review_groups_auto.json")

    # --- TASK 4.2: PERSONA GENERATION ---
    print("\nStep 2: Generating personas based on those groups...")
    
    # Map reviews for quick lookup by ID
    reviews_map = {r['reviewId']: r['content'] for r in reviews_all}
    all_personas = []

    # Loop through the themes generated in Step 1
    # Note: Using 'themes' as the key based on your previous AI output
    for i, theme in enumerate(auto_groups.get('themes', []), 1):
        theme_name = theme['name']
        group_id = theme['id']
        
        # Get actual review text for context
        r_ids = theme['reviews'][:5] 
        context_text = "\n".join([f"ID: {rid} | {reviews_map[rid]}" for rid in r_ids if rid in reviews_map])

        print(f"Creating Persona P{i} for {theme_name}...")

        persona_completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": prompt_config["persona_prompt"]},
                {"role": "user", "content": f"Theme: {theme_name}\nReviews:\n{context_text}"}
            ],
            response_format={"type": "json_object"}
        )

        persona = json.loads(persona_completion.choices[0].message.content)
        
        # Ensure it has the required metadata
        persona['id'] = f"P{i}"
        persona['derived_from_group'] = group_id
        all_personas.append(persona)

    # 6. Save final personas to personas/ folder
    os.makedirs('personas', exist_ok=True)
    with open('personas/personas_auto.json', 'w') as f:
        json.dump({"personas": all_personas}, f, indent=2)

    print("\nSuccess! Final personas saved to personas/personas_auto.json")

if __name__ == "__main__":
    run_pipeline()