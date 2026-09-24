#!/usr/bin/env python3
"""
🌱 Aigarth Garden Full Automation Pipeline
- Parses latest mining log
- Runs daily status report
- Pushes new results to public repo (safe)
- Runs every 2 hours until epoch end
"""

import subprocess
from pathlib import Path
from datetime import datetime

def run_parser():
    print("📡 Parsing latest mining log...")
    try:
        # Using garden_venv/bin/python to ensure dependencies are met
        result = subprocess.run(["./garden_venv/bin/python", "mining-logs/parser.py"], 
                              capture_output=True, text=True, cwd=".")
        print(result.stdout.strip())
    except Exception as e:
        print(f"Parser warning: {e}")

def run_report():
    print("\n📊 Generating Garden Status Report...")
    try:
        # Using garden_venv/bin/python
        result = subprocess.run(["./garden_venv/bin/python", "garden_report.py"], 
                              capture_output=True, text=True, cwd=".")
        print(result.stdout.strip())
    except Exception as e:
        print(f"Report warning: {e}")

def git_push():
    print("\n🚀 Pushing updates to public Garden...")
    try:
        subprocess.run(["git", "add", "results/", "mining-logs/parsed_results.csv"], check=True, cwd=".")
        subprocess.run(["git", "commit", "-m", f"Automated Garden Update - {datetime.now().strftime('%Y-%m-%d %H:%M')}"], 
                      check=True, cwd=".")
        subprocess.run(["git", "push"], check=True, cwd=".")
        print("✅ Pushed to GitHub successfully")
    except subprocess.CalledProcessError:
        print("ℹ️  No new changes to push")

if __name__ == "__main__":
    print("🌱 Starting Aigarth Garden Automation Cycle")
    print("=" * 70)
    
    run_parser()
    run_report()
    git_push()
    
    print(f"\n✅ Cycle complete at {datetime.now().strftime('%H:%M UTC')}")
    print("The Intelligent Tissue continues to evolve.")
