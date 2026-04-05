"""generates tests from specs"""
import os
import json
import re
from groq import Groq

# Groq ID
client = Groq(api_key="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")

def generate_tests_auto():
    spec_path = 'spec/spec_auto.md'

    if not os.path.exists(spec_path):
        print(f"Error: {spec_path} not found.")
        return

    with open(spec_path, 'r', encoding='utf-8') as f:
        spec_content = f.read()

    # Split the spec into individual requirements
    req_blocks = re.split(r'\n(?=Requirement ID:)', spec_content)
    req_blocks = [b.strip() for b in req_blocks if "Requirement ID:" in b]
    
    total_reqs = len(req_blocks)
    print(f"Found {total_reqs} requirements.")

    all_tests = []

    # Loop through each requirement one by one
    for i, block in enumerate(req_blocks, 1):
        # Get the ID
        match = re.search(r'FR_auto_\d+', block)
        req_id = match.group(0) if match else f"FR_auto_{i}"

        print(f"  [{i}/{total_reqs}] Generating test T_auto_{i} for {req_id}...")

        #Formatting
        user_payload = (
            f"Requirement Details:\n{block}\n\n"
            f"TASK: Generate EXACTLY ONE validation test for this requirement.\n"
            "STRICT JSON FORMAT:\n"
            "{\n"
            f"  \"test_id\": \"T_auto_{i}\",\n"
            f"  \"requirement_id\": \"{req_id}\",\n"
            "  \"scenario\": \"...\",\n"
            "  \"steps\": [\"step 1\", \"step 2\"],\n"
            "  \"expected_result\": \"...\"\n"
            "}"
        )

        try:
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "system", "content": "You are a Senior QA Engineer. Return ONLY JSON."},
                    {"role": "user", "content": user_payload}
                ],
                response_format={"type": "json_object"},
                temperature=0.2 
            )

            test_obj = json.loads(completion.choices[0].message.content)
            
            # Avoid nested returns
            if "tests" in test_obj and isinstance(test_obj["tests"], list):
                all_tests.append(test_obj["tests"][0])
            else:
                all_tests.append(test_obj)

        except Exception as e:
            print(f"Failed for {req_id}: {e}")

    # Save
    os.makedirs('tests', exist_ok=True)
    with open('tests/tests_auto.json', 'w', encoding='utf-8') as f:
        json.dump({"tests": all_tests}, f, indent=2, ensure_ascii=False)

    print(f"\n Generated {len(all_tests)} tests for {total_reqs} requirements.")

if __name__ == "__main__":
    generate_tests_auto()