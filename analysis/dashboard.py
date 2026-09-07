#!/usr/bin/env python3
"""
🌱 Aigarth Garden Multi-Run Dashboard
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

print("🌱 Aigarth Garden Multi-Run Dashboard")
print("=" * 70)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n")

results_dir = Path('../results')
sim_files = sorted(results_dir.glob('results_mut*.csv'), reverse=True)

if not sim_files:
    print("⚠️ No simulation results found yet.")
else:
    plt.figure(figsize=(12, 8))
    for file in sim_files[:8]:  # Show up to 8 latest runs
        df = pd.read_csv(file)
        label = file.name.replace('results_mut0.2_', '').replace('.csv', '')[:20]
        plt.plot(df.index, df['best_fitness'], label=label, linewidth=2, alpha=0.85)
        print(f"📊 {file.name}: {len(df)} gens | Peak: {df['best_fitness'].max():.6f}")
    
    plt.title('Hyperidentity Evolution — Multiple Runs Comparison')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('../results/multi_run_comparison.png', dpi=300)
    print("\n📈 Multi-run comparison plot saved → results/multi_run_comparison.png")

print("\n✅ Dashboard complete.")
print("Repo → https://github.com/durdyh2o-qubic/Aigarth-Garden-Labs-2")
