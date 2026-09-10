import time
import subprocess
from datetime import datetime

def run_pipeline():
    print(f"\n[Al-Haqq Autonomous Loop] Executing cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    steps = ["purge.py", "verify.py", "sync_git.py"]
    for script in steps:
        try:
            result = subprocess.run(["python", script], capture_output=True, text=True, check=True)
            print(f"[{script}] Status: SUCCESS")
            for line in result.stdout.strip().split('\n'):
                if line:
                    print(f"   > {line}")
        except subprocess.CalledProcessError as e:
            print(f"[{script}] Error: {e.stderr.strip()}")
        except FileNotFoundError:
            print(f"[{script}] Notice: Script not found, skipping.")

if __name__ == "__main__":
    interval = 60  # Interval in seconds between loops
    print(f"🛡️ Starting Al-Haqq Autonomous Fleet Loop (Interval: {interval}s). Press Ctrl+C to stop.")
    try:
        while True:
            run_pipeline()
            print(f"\nSleeping for {interval} seconds...")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nAutonomous loop terminated by user. Fleet state sovereign and preserved.")
