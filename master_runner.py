import json
import subprocess
from datetime import datetime
def run_master_pipeline():
 print("=== New Era Protocol: Master Pipeline Execution ===")
 print("Author: ICAM (Syams Maulana) | Al-Haqq Framework v3.0.0\n")
 scripts = ["adjudicator.py", "soul.py", "sync.py", "verify.py"]
 for s in scripts:
  print(f"-> Executing {s}...")
  result = subprocess.run(["python", s], capture_output=True, text=True)
  print(result.stdout.strip())
  print("-" * 40)
 print("Master pipeline execution completed seamlessly.")
if __name__ == "__main__":
 run_master_pipeline()
