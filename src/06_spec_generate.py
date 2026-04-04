"""generates structured specs from personas"""
import os
import json
from groq import Groq

# 1. Initialize the Groq client
client = Groq(api_key="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")

def generate_spec_auto():
    # 2. Load the automated personas
    persona_path = 'personas/personas_auto.json'
    if not os.path.exists(persona_path):
        print(f"Error: {persona_path} not found. Please run the persona generation first.")
        return

    with open(persona_path, 'r') as f:
        personas_data = json.load(f)

    # 3. Load the spec prompt
    with open('prompts/prompt_auto.json', 'r') as f:
        prompt_config = json.load(f)
    
    spec_instructions = prompt_config["spec_prompt"]

    all_specs = "# Automated System Requirements Specification (Spec-Auto)\n\n"

    # 4. Generate requirements for each persona
    for i, persona in enumerate(personas_data['personas'], 1):
        print(f"Generating requirements for: {persona['name']}...")

        # We pass the ID to the AI so it uses FR_auto_1, FR_auto_2, etc.
        user_payload = f"Persona: {persona['name']}\nGroup: {persona['derived_from_group']}\nStarting ID: FR_auto_{i}"
        
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": spec_instructions},
                {"role": "user", "content": user_payload}
            ]
        )

        response_text = completion.choices[0].message.content.strip()
        all_specs += response_text + "\n\n---\n\n"

    # 5. Save the output to spec/spec_auto.md
    os.makedirs('spec', exist_ok=True)
    with open('spec/spec_auto.md', 'w') as f:
        f.write(all_specs)

    print("Success! Specification saved to spec/spec_auto.md")

if __name__ == "__main__":
    generate_spec_auto()