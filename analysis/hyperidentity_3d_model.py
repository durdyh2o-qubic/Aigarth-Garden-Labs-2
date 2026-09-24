import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
import pandas as pd

# Load latest real simulation data
sim_files = sorted(Path('../results').glob('results_mut*.csv'), reverse=True)
if not sim_files:
    print("No simulation data found. Using demo data.")
    generations = np.arange(80)
    fitness = np.array([0.3035 + 0.0004 * np.sin(g/6) + 0.00015 * np.random.randn() for g in generations])
else:
    sim = pd.read_csv(sim_files[0])
    generations = sim['generation'].values
    fitness = sim['best_fitness'].values
    print(f"Loaded real data: {sim_files[0].name} | {len(sim)} generations | Peak: {fitness.max():.6f}")

# Create 3D neural-like fitness landscape
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# X = Generation, Y = Fitness scaled, Z = Simulated "neuron layer" depth
X = generations
Y = fitness * 10000
Z = np.sin(generations / 8) * 500 + fitness * 2000  # Simulated depth/layer dimension

scatter = ax.scatter(X, Y, Z, c=fitness, cmap='viridis', s=80, alpha=0.9, edgecolors='black', linewidth=0.5)

# Connect dots to show evolutionary path (neural connections)
for i in range(len(X)-1):
    ax.plot([X[i], X[i+1]], [Y[i], Y[i+1]], [Z[i], Z[i+1]], 
            color='cyan', alpha=0.4, linewidth=1.5)

ax.set_xlabel('Generation')
ax.set_ylabel('Hyperidentity Fitness (scaled)')
ax.set_zlabel('Simulated Neural Depth / Layer')
ax.set_title('3D Hyperidentity Evolution Landscape\nAigarth Garden Labs — Intelligent Tissue Growth')

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label('Fitness Strength')

plt.tight_layout()
plt.savefig('../results/hyperidentity_3d_landscape.png', dpi=300)
print("✅ 3D model saved to results/hyperidentity_3d_landscape.png")