#!/usr/bin/env python3
"""
🌱 Aigarth Garden Status Report — One-Click Overview
"""

from pathlib import Path
import pandas as pd
from datetime import datetime

print("🌱 Aigarth Garden Status Report")
print("=" * 70)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n")

# Mining Status
mining_path = Path("mining-logs/parsed_results.csv")
if mining_path.exists():
    df = pd.read_csv(mining_path)
    print(f"📡 MINING")
    print(f"   Peak it/s      : {df['it_s'].max():,}")
    print(f"   Avg it/s       : {df['it_s'].mean():,.0f}")
    print(f"   Avg Efficiency : {df['efficiency'].mean():.1%}")
    print(f"   Latest Seed    : {df['seed'].iloc[-1] if len(df)>0 else 'N/A'}")
else:
    print("📡 No mining data parsed yet.")

print()

# Simulation Status
sim_files = sorted(Path("results").glob("results_mut*.csv"), reverse=True)
if sim_files:
    sim = pd.read_csv(sim_files[0])
    print(f"🧬 SIMULATION")
    print(f"   Peak Fitness   : {sim['best_fitness'].max():.6f}")
    print(f"   Latest Run     : {len(sim)} generations")
else:
    print("🧬 No simulation results yet.")

print("\nThe Garden is being observed honestly and openly.")
print("Repo → https://github.com/durdyh2o-qubic/Aigarth-Garden-Labs-2")
