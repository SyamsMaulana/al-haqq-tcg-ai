import subprocess
import sys

def run_script(script_name):
    print(f"🚀 Executing {script_name}...")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
        print(f"✅ {script_name} completed successfully.\n")
    else:
        print(f"❌ Error in {script_name}:\n{result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 65)
    print("⚡ AL-HAQQ MASTER DEPLOYMENT & SOVEREIGN ENGINE PIPELINE")
    print("=" * 65)
    
    run_script("sovereign_sentinel.py")
    run_script("budget_monitor.py")
    run_script("fleet_cli.py")
    run_script("sync_git.py")
    
    print("🎉 All sovereign fleet assets successfully deployed, verified, and synchronized!")
    print("=" * 65)
