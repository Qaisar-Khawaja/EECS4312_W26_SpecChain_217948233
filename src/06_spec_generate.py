"""generates structured specs from personas"""
import os
import json
import re
from groq import Groq

# API Key
client = Groq(api_key="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")

def generate_spec_auto():
    # Load files
    if not os.path.exists('personas/personas_auto.json'):
        print("Error: personas/personas_auto.json not found.")
        return

    with open('personas/personas_auto.json', 'r', encoding='utf-8') as f:
        personas_data = json.load(f)
    
    with open('prompts/prompt_auto.json', 'r', encoding='utf-8') as f:
        prompt_config = json.load(f)
    
    spec_instructions = prompt_config["spec_prompt"]
    all_specs = "# Automated System Requirements Specification (Spec-Auto)\n\n"

    # Counter for ID
    global_req_count = 1

    for persona in personas_data['personas']:
        print(f"Generating requirements for: {persona['name']}...")

        user_payload = (
            f"Persona Data: {json.dumps(persona)}\n\n"
            f"TASK: Generate as many system requirements as needed to address this persona's goals and pain points.\n"
            f"STARTING ID: FR_auto_{global_req_count}\n\n"
            f"STRICT TEMPLATE FOR EVERY REQUIREMENT:\n"
            f"Requirement ID: FR_auto_[NUMBER]\n"
            f"Description: [The system shall...]\n"
            f"Source Persona: [{persona['name']}]\n"
            f"Traceability: [Derived from review group {persona.get('derived_from_group', 'N/A')}]\n"
            f"Acceptance Criteria: [Given/When/Then scenario]\n"
            f"---"
        )
        
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": spec_instructions},
                {"role": "user", "content": user_payload}
            ],
            temperature=0.6
        )

        response_text = completion.choices[0].message.content.strip()
        
        # Append the response
        all_specs += response_text + "\n\n"
        
        # Count how many requirements got generated in this turn
        # so the next persona starts at the correct ID number
        generated_count = response_text.count("Requirement ID: FR_auto_")
        global_req_count += generated_count

    # Save to spec/spec_auto.md
    os.makedirs('spec', exist_ok=True)
    with open('spec/spec_auto.md', 'w', encoding='utf-8') as f:
        f.write(all_specs)

    print(f"Success! Generated approximately {global_req_count - 1} requirements to spec/spec_auto.md")

if __name__ == "__main__":
    generate_spec_auto()