#!/usr/bin/env python3
"""
🌱 Aigarth Garden Analysis Tools
Hyperidentity Evolution Observatory
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

print("🌱 Aigarth Garden Dashboard")
print("=" * 60)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n")

# Load latest simulation
results_dir = Path('results')
sim_files = sorted(results_dir.glob('results_mut*.csv'), reverse=True)

if sim_files:
    latest = pd.read_csv(sim_files[0])
    print(f"📊 Latest Simulation: {sim_files[0].name}")
    print(f"   Generations : {len(latest)}")
    print(f"   Peak Fitness: {latest['best_fitness'].max():.6f}")
    print(f"   Final Fitness: {latest['best_fitness'].iloc[-1]:.6f}\n")
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(latest.index, latest['best_fitness'], 'b-', linewidth=2.5, label='Best Fitness')
    plt.title('Hyperidentity Evolution — Fitness Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/latest_fitness_curve.png', dpi=300)
    print("   📈 Plot saved → results/latest_fitness_curve.png")
else:
    print("⚠️  No simulation results found yet.")

print("\n✅ Dashboard complete.")
print("Repo → https://github.com/durdyh2o-qubic/Aigarth-Garden-Labs-2")
