import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from pathlib import Path
import pandas as pd

# Load latest simulation data (robust column detection)
sim_files = sorted(Path('../results').glob('results_mut*.csv'), reverse=True)
if not sim_files:
    print("No simulation results found. Using demo data.")
    generations = np.arange(80)
    fitness = np.array([0.0035 + 0.0004 * np.sin(g/5) + 0.0003 * np.random.randn() for g in generations])
    gol_cells = np.array([2800 + 300 * np.sin(g/8) + 150 * np.random.randn() for g in generations])
else:
    sim = pd.read_csv(sim_files[0])
    print(f"Loaded: {sim_files[0].name} | {len(sim)} generations")
    
    # Robust column name handling
    if 'gen' in sim.columns:
        generations = sim['gen'].values
    elif 'generation' in sim.columns:
        generations = sim['generation'].values
    else:
        generations = np.arange(len(sim))
    
    if 'best_fitness' in sim.columns:
        fitness = sim['best_fitness'].values
    else:
        fitness = np.zeros(len(sim))
    
    # Simulate correlated 3D GoL cells
    gol_cells = np.array([2800 + 300 * np.sin(g/8) + 200 * (f - fitness.mean())*10000 for g, f in zip(generations, fitness)])

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(generations, fitness*10000, gol_cells, 
                    c=fitness, cmap='viridis', s=60, alpha=0.85)

ax.set_xlabel('Generation')
ax.set_ylabel('Hyperidentity Fitness (scaled)')
ax.set_zlabel('3D GoL Live Cells (correlated)')
ax.set_title('3D Hybrid View: Real Hyperidentity Evolution + GoL Analogy')

def animate(frame):
    ax.view_init(elev=25, azim=frame)
    return scatter,

ani = FuncAnimation(fig, animate, frames=360, interval=40, blit=False)

plt.show()

# Optional: Save as GIF (uncomment if ffmpeg installed)
# ani.save('hybrid_3d_rotation_real.gif', writer='ffmpeg', fps=30)
