"""runs the full pipeline end-to-end""""""
Master Orchestrator: Executes the Automated Requirements Engineering Pipeline.
This script automates the flow from raw data to metrics.
"""
import subprocess
import sys

def run_script(script_name):
    print(f"--- Running {script_name} ---")
    try:
        subprocess.run([sys.executable, f"src/{script_name}"], check=True)
        print(f"Successfully completed {script_name}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        sys.exit(1)

def main():

    run_script("01_collect_or_import.py")
    run_script("02_clean.py")


    run_script("05_personas_auto.py")

    run_script("06_spec_generate.py")

    # Step 5: Test Case Generation
    # Produces: tests/tests_auto.json
    run_script("07_tests_generate.py")

    run_script("08_metrics.py")

    print("========================================")
    print("AUTOMATED PIPELINE EXECUTION COMPLETE")
    print("========================================")

if __name__ == "__main__":
    main()