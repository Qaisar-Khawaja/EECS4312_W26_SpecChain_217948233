"""computes metrics: coverage/traceability/ambiguity/testability"""
# import os
# import json
# import re

# def compute_auto_metrics():
#     # 1. Load the automated artifacts
#     groups_path = 'data/review_groups_auto.json'
#     personas_path = 'personas/personas_auto.json'
#     spec_path = 'spec/spec_auto.md'
#     tests_path = 'tests/tests_auto.json'
#     reviews_path = 'data/reviews_clean.jsonl'
    
#     # 2. Dataset Size
#     dataset_size = 0
#     if os.path.exists(reviews_path):
#         with open(reviews_path, 'r') as f:
#             dataset_size = sum(1 for _ in f)

#     # 3. Persona Count
#     persona_count = 0
#     if os.path.exists(personas_path):
#         with open(personas_path, 'r') as f:
#             personas_data = json.load(f)
#             persona_count = len(personas_data.get('personas', []))

#     # 4. Requirements Count
#     requirements_count = 0
#     spec_content = ""
#     if os.path.exists(spec_path):
#         with open(spec_path, 'r') as f:
#             spec_content = f.read()
#         req_ids = set(re.findall(r'Requirement ID:\s*(FR_auto_\d+)', spec_content))
#         requirements_count = len(req_ids)

#     # 5. Tests Count
#     tests_count = 0
#     tests_data = {}
#     if os.path.exists(tests_path):
#         with open(tests_path, 'r') as f:
#             tests_data = json.load(f)
#             tests_count = len(tests_data.get('tests', []))

#     # 6. Traceability Links
#     traceability_links = len(re.findall(r'Traceability:', spec_content))

#     # 7. Advanced Ratios
#     review_coverage = 0
#     if os.path.exists(groups_path):
#         with open(groups_path, 'r') as f:
#             groups_data = json.load(f)
#             total_grouped_reviews = sum(len(g.get('reviews', [])) for g in groups_data.get('themes', []))
#             review_coverage = round(total_grouped_reviews / dataset_size, 3) if dataset_size > 0 else 0

#     traceability_ratio = 1.0 if requirements_count > 0 and traceability_links >= requirements_count else 0.0
    
#     testability_rate = 0.0
#     if tests_count > 0:
#         tested_reqs = {t.get('requirement_id') for t in tests_data.get('tests', [])}
#         testability_rate = round(len(tested_reqs) / requirements_count, 2) if requirements_count > 0 else 0

#     # 8. Final Metrics Object
#     metrics_auto = {
#         "pipeline": "automated",
#         "dataset_size": dataset_size,
#         "persona_count": persona_count,
#         "requirements_count": requirements_count,
#         "tests_count": tests_count,
#         "traceability_links": traceability_links,
#         "review_coverage": review_coverage,
#         "traceability_ratio": traceability_ratio,
#         "testability_rate": testability_rate,
#         "ambiguity_ratio": 0.0 
#     }

#     os.makedirs('metrics', exist_ok=True)
#     with open('metrics/metrics_auto.json', 'w') as f:
#         json.dump(metrics_auto, f, indent=2)
#     print("Automated Metrics Generated Successfully.")

# def compute_hybrid_metrics():
#     # 1. Load the hybrid artifacts
#     groups_path = 'data/review_groups_hybrid.json'
#     personas_path = 'personas/personas_hybrid.json'
#     spec_path = 'spec/spec_hybrid.md'
#     tests_path = 'tests/tests_hybrid.json'
#     reviews_path = 'data/reviews_clean.jsonl'
    
#     dataset_size = 0
#     if os.path.exists(reviews_path):
#         with open(reviews_path, 'r') as f:
#             dataset_size = sum(1 for _ in f)

#     persona_count = 0
#     if os.path.exists(personas_path):
#         with open(personas_path, 'r') as f:
#             personas_data = json.load(f)
#             persona_count = len(personas_data.get('personas', []))

#     requirements_count = 0
#     spec_content = ""
#     if os.path.exists(spec_path):
#         with open(spec_path, 'r') as f:
#             spec_content = f.read()
#         req_ids = set(re.findall(r'Requirement ID:\s*(FR_hybrid_\d+)', spec_content))
#         requirements_count = len(req_ids)

#     tests_count = 0
#     tests_data = {}
#     if os.path.exists(tests_path):
#         with open(tests_path, 'r') as f:
#             tests_data = json.load(f)
#             tests_count = len(tests_data.get('tests', []))

#     traceability_links = len(re.findall(r'Traceability:', spec_content))

#     review_coverage = 0
#     if os.path.exists(groups_path):
#         with open(groups_path, 'r') as f:
#             groups_data = json.load(f)
#             # Accessing 'groups' and 'review_ids' for hybrid
#             total_grouped_reviews = sum(len(g.get('review_ids', [])) for g in groups_data.get('groups', []))
#             review_coverage = round(total_grouped_reviews / dataset_size, 3) if dataset_size > 0 else 0

#     traceability_ratio = 1.0 if requirements_count > 0 and traceability_links >= requirements_count else 0.0
    
#     testability_rate = 0.0
#     if tests_count > 0:
#         tested_reqs = {t.get('requirement_id') for t in tests_data.get('tests', [])}
#         testability_rate = round(len(tested_reqs) / requirements_count, 2) if requirements_count > 0 else 0

#     metrics_hybrid = {
#         "pipeline": "hybrid",
#         "dataset_size": dataset_size,
#         "persona_count": persona_count,
#         "requirements_count": requirements_count,
#         "tests_count": tests_count,
#         "traceability_links": traceability_links,
#         "review_coverage": review_coverage,
#         "traceability_ratio": traceability_ratio,
#         "testability_rate": testability_rate,
#         "ambiguity_ratio": 0.0 
#     }

#     os.makedirs('metrics', exist_ok=True)
#     with open('metrics/metrics_hybrid.json', 'w') as f:
#         json.dump(metrics_hybrid, f, indent=2)
#     print("Hybrid Metrics Generated Successfully.")

# if __name__ == "__main__":
#     # Call both to ensure all data is up to date
#     compute_auto_metrics()
#     compute_hybrid_metrics()
import os
import json
import re

def get_dataset_size():
    path = 'data/reviews_clean.jsonl'
    if os.path.exists(path):
        with open(path, 'r') as f:
            return sum(1 for _ in f)
    return 0

def calculate_pipeline_metrics(name, groups_path, personas_path, spec_path, tests_path, id_prefix):
    dataset_size = get_dataset_size()
    
    # Persona Count
    persona_count = 0
    if os.path.exists(personas_path):
        with open(personas_path, 'r') as f:
            data = json.load(f)
            persona_count = len(data.get('personas', []))

    # Requirements Count & Traceability Links
    req_count = 0
    trace_links = 0
    if os.path.exists(spec_path):
        with open(spec_path, 'r') as f:
            content = f.read()
        req_count = len(set(re.findall(fr'Requirement ID:\s*({id_prefix}_\d+)', content)))
        trace_links = len(re.findall(r'Traceability:', content))

    # Tests Count
    test_count = 0
    testability_rate = 0.0
    if os.path.exists(tests_path):
        with open(tests_path, 'r') as f:
            data = json.load(f)
            tests = data.get('tests', [])
            test_count = len(tests)
            if req_count > 0:
                tested_reqs = {t.get('requirement_id') for t in tests}
                testability_rate = round(len(tested_reqs) / req_count, 2)

    # Review Coverage
    coverage = 0
    if os.path.exists(groups_path):
        with open(groups_path, 'r') as f:
            data = json.load(f)
            # Handle different keys: 'themes' for auto/manual, 'groups' for hybrid
            groups = data.get('themes', data.get('groups', []))
            # Handle different keys: 'reviews' for auto/manual, 'review_ids' for hybrid
            total_reviews = sum(len(g.get('reviews', g.get('review_ids', []))) for g in groups)
            coverage = round(total_reviews / dataset_size, 3) if dataset_size > 0 else 0

    return {
        "pipeline": name,
        "persona_count": persona_count,
        "requirements_count": req_count,
        "tests_count": test_count,
        "review_coverage": coverage,
        "traceability_ratio": 1.0 if req_count > 0 and trace_links >= req_count else 0.0,
        "testability_rate": testability_rate
    }

def run_metrics():
    pipelines = [
        ("manual", "data/review_groups_manual.json", "personas/personas_manual.json", "spec/spec_manual.md", "tests/tests_manual.json", "FR_manual"),
        ("auto", "data/review_groups_auto.json", "personas/personas_auto.json", "spec/spec_auto.md", "tests/tests_auto.json", "FR_auto"),
        ("hybrid", "data/review_groups_hybrid.json", "personas/personas_hybrid.json", "spec/spec_hybrid.md", "tests/tests_hybrid.json", "FR_hybrid")
    ]
    
    summary = {}
    os.makedirs('metrics', exist_ok=True)

    for name, g, p, s, t, prefix in pipelines:
        m = calculate_pipeline_metrics(name, g, p, s, t, prefix)
        summary[name] = m
        with open(f'metrics/metrics_{name}.json', 'w') as f:
            json.dump(m, f, indent=2)

    with open('metrics/metrics_summary.json', 'w') as f:
        json.dump({"comparison": summary}, f, indent=2)
    print("All metrics and summary generated in /metrics.")

if __name__ == "__main__":
    run_metrics()