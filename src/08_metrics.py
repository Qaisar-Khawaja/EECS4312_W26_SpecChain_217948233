"""computes metrics: coverage/traceability/ambiguity/testability"""
import os
import json
import re

def get_dataset_size():
    path = 'data/reviews_clean.jsonl'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    return 0

def calculate_pipeline_metrics(name, groups_path, personas_path, spec_path, tests_path, id_prefix):
    dataset_size = get_dataset_size()
    
    # Persona Count
    persona_count = 0
    if os.path.exists(personas_path):
        with open(personas_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            persona_count = len(data.get('personas', []))
    
    # Requirements Count & Traceability Links
    req_count = 0
    trace_links = 0
    ambiguous_reqs = 0
    if os.path.exists(spec_path):
        with open(spec_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Handle both FR_auto_1 and FR1 formats
            if '_' in id_prefix:
                # For auto/hybrid: FR_auto_1, FR_hybrid_2
                found_ids = set(re.findall(fr'{id_prefix}_\d+', content))
            else:
                # For manual: FR1, FR2, FR3
                found_ids = set(re.findall(fr'{id_prefix}\d+', content))
            req_count = len(found_ids)
            # Count explicit 'Traceability:
            trace_links = len(re.findall(r'\*\*Traceability\*\*:|Traceability:', content))
            
            vague_terms = [r'\betc\b', r'\bvarious\b', r'\bsome\b', r'\bappropriate\b', r'\bmaybe\b']
            for block in content.split('---'):
                if any(re.search(term, block, re.IGNORECASE) for term in vague_terms):
                    ambiguous_reqs += 1
    
    # Tests Count & Testability
    test_count = 0
    testability_rate = 0.0
    if os.path.exists(tests_path):
        with open(tests_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            tests = data.get('tests', [])
            test_count = len(tests)
            if req_count > 0:
                # Count how many unique requirements actually have a test linked
                tested_reqs = {t.get('requirement_id') for t in tests if t.get('requirement_id')}
                testability_rate = round(len(tested_reqs) / req_count, 2)
    
    # Review Coverage
    coverage = 0
    if os.path.exists(groups_path):
        with open(groups_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Check both 'themes' and 'groups' keys to be safe
            groups = data.get('themes', data.get('groups', []))
            unique_reviews = set()
            for g in groups:
                # Check both 'reviews' and 'review_ids' keys
                r_list = g.get('reviews', g.get('review_ids', []))
                unique_reviews.update(r_list)
            coverage = round(len(unique_reviews) / dataset_size, 2) if dataset_size > 0 else 0
    
    # Final Ratios
    trace_ratio = round(trace_links / req_count, 2) if req_count > 0 else 0.0
    ambiguity_ratio = round(ambiguous_reqs / req_count, 2) if req_count > 0 else 0.0
    
    return {
        "pipeline": name,
        "dataset_size": dataset_size,
        "persona_count": persona_count,
        "requirements_count": req_count,
        "tests_count": test_count,
        "traceability_links": trace_links,
        "review_coverage": coverage,
        "traceability_ratio": trace_ratio,
        "testability_rate": testability_rate,
        "ambiguity_ratio": ambiguity_ratio
    }

def create_summary(m_manual, m_auto, m_hybrid):
    """Create a comparison summary of all three pipelines"""
    return {
        "pipelines": [m_manual, m_auto, m_hybrid],
        "comparison": {
            "persona_count": {
                "manual": m_manual["persona_count"],
                "automated": m_auto["persona_count"],
                "hybrid": m_hybrid["persona_count"]
            },
            "requirements_count": {
                "manual": m_manual["requirements_count"],
                "automated": m_auto["requirements_count"],
                "hybrid": m_hybrid["requirements_count"]
            },
            "tests_count": {
                "manual": m_manual["tests_count"],
                "automated": m_auto["tests_count"],
                "hybrid": m_hybrid["tests_count"]
            },
            "review_coverage": {
                "manual": m_manual["review_coverage"],
                "automated": m_auto["review_coverage"],
                "hybrid": m_hybrid["review_coverage"]
            },
            "traceability_ratio": {
                "manual": m_manual["traceability_ratio"],
                "automated": m_auto["traceability_ratio"],
                "hybrid": m_hybrid["traceability_ratio"]
            },
            "testability_rate": {
                "manual": m_manual["testability_rate"],
                "automated": m_auto["testability_rate"],
                "hybrid": m_hybrid["testability_rate"]
            },
            "ambiguity_ratio": {
                "manual": m_manual["ambiguity_ratio"],
                "automated": m_auto["ambiguity_ratio"],
                "hybrid": m_hybrid["ambiguity_ratio"]
            }
        },
        "insights": {
            "best_traceability": max(
                [("manual", m_manual["traceability_ratio"]), 
                 ("automated", m_auto["traceability_ratio"]), 
                 ("hybrid", m_hybrid["traceability_ratio"])],
                key=lambda x: x[1]
            )[0],
            "best_testability": max(
                [("manual", m_manual["testability_rate"]), 
                 ("automated", m_auto["testability_rate"]), 
                 ("hybrid", m_hybrid["testability_rate"])],
                key=lambda x: x[1]
            )[0],
            "lowest_ambiguity": min(
                [("manual", m_manual["ambiguity_ratio"]), 
                 ("automated", m_auto["ambiguity_ratio"]), 
                 ("hybrid", m_hybrid["ambiguity_ratio"])],
                key=lambda x: x[1]
            )[0],
            "most_efficient": "hybrid" if m_hybrid["requirements_count"] <= m_manual["requirements_count"] and m_hybrid["requirements_count"] <= m_auto["requirements_count"] else "manual"
        }
    }

def run_metrics():
    os.makedirs('metrics', exist_ok=True)
    
    # Define the manual pipeline paths
    m_manual = calculate_pipeline_metrics(
        "manual", 
        "data/review_groups_manual.json", 
        "personas/personas_manual.json", 
        "spec/spec_manual.md", 
        "tests/tests_manual.json", 
        "FR"
    )
    
    # Save manual metrics
    with open('metrics/metrics_manual.json', 'w', encoding='utf-8') as f:
        json.dump(m_manual, f, indent=2)
    print("Manual metrics generated successfully in metrics/metrics_manual.json")
    
    # Define the automated pipeline paths
    m_auto = calculate_pipeline_metrics(
        "automated", 
        "data/review_groups_auto.json", 
        "personas/personas_auto.json", 
        "spec/spec_auto.md", 
        "tests/tests_auto.json", 
        "FR_auto"
    )
    
    # Save automated metrics
    with open('metrics/metrics_auto.json', 'w', encoding='utf-8') as f:
        json.dump(m_auto, f, indent=2)
    print("Automated metrics generated successfully in metrics/metrics_auto.json")
    
    # Define the hybrid pipeline paths
    m_hybrid = calculate_pipeline_metrics(
        "hybrid", 
        "data/review_groups_hybrid.json", 
        "personas/personas_hybrid.json", 
        "spec/spec_hybrid.md", 
        "tests/tests_hybrid.json", 
        "FR_hybrid"
    )
    
    # Save hybrid metrics
    with open('metrics/metrics_hybrid.json', 'w', encoding='utf-8') as f:
        json.dump(m_hybrid, f, indent=2)
    print("Hybrid metrics generated successfully in metrics/metrics_hybrid.json")
    
    # Create and save summary comparison
    summary = create_summary(m_manual, m_auto, m_hybrid)
    with open('metrics/metrics_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    print("Summary metrics generated successfully in metrics/metrics_summary.json")

if __name__ == "__main__":
    run_metrics()