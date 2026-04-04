"""generates tests from specs"""
import os
import json
from groq import Groq

# 1. Initialize the Groq client
client = Groq(api_key="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")

def generate_tests_auto():
    # 2. Load the automated specification
    spec_path = 'spec/spec_auto.md'
    if not os.path.exists(spec_path):
        print(f"Error: {spec_path} not found. Please run the spec generation first.")
        return

    with open(spec_path, 'r') as f:
        spec_content = f.read()

    # 3. Load the test prompt
    with open('prompts/prompt_auto.json', 'r') as f:
        prompt_config = json.load(f)
    
    test_instructions = prompt_config["test_prompt"]

    print("Generating validation tests from spec_auto.md...")

    # 4. Call the AI to generate the JSON test suite
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": test_instructions},
            {"role": "user", "content": f"System Specification:\n{spec_content}"}
        ],
        response_format={"type": "json_object"}
    )

    # 5. Parse and Save the output to tests/tests_auto.json
    test_data = json.loads(completion.choices[0].message.content)
    
    os.makedirs('tests', exist_ok=True)
    with open('tests/tests_auto.json', 'w') as f:
        json.dump(test_data, f, indent=2)

    print("Success! Validation tests saved to tests/tests_auto.json")

if __name__ == "__main__":
    generate_tests_auto()