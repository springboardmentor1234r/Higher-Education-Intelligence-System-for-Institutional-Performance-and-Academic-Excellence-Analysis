"""run_pipeline.py — runs all 5 real-data stages in order."""
import subprocess, sys, os
STAGES = ["data_collection.py", "data_cleaning.py", "data_integration.py", "validate_data.py", "load_to_bi.py"]
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for stage in STAGES:
        print(f"\n{'='*70}\nSTAGE: {stage}\n{'='*70}")
        r = subprocess.run([sys.executable, os.path.join(here, stage)])
        if r.returncode != 0:
            print(f"Pipeline stopped: {stage} failed."); sys.exit(1)
    print("\nPipeline finished. See data/warehouse/ for BI-ready outputs.")
