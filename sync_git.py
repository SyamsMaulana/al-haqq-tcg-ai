import os
import subprocess
from datetime import datetime

def git_sync():
    print("=== Al-Haqq Protocol: Git Sync Engine ===")
    commit_msg = f"Auto-sync fleet state: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
    
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Successfully synchronized fleet state with remote repository.")
    except subprocess.CalledProcessError as e:
        print(f"Git sync notice: {e}")

if __name__ == "__main__":
    git_sync()
