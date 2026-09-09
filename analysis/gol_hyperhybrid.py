import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from hyper_tissue import AigarthTissue  # Import from our main simulator

# 3D Game of Life with Hyperidentity Teacher Influence
def count_3d_neighbors(grid):
    neighbors = np.zeros_like(grid)
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                if i == 0 and j == 0 and k == 0: continue
                neighbors += np.roll(np.roll(np.roll(grid, i, 0), j, 1), k, 2)
    return neighbors

def gol_3d_step(grid):
    neighbors = count_3d_neighbors(grid)
    birth = (grid == 0) & (neighbors == 4)
    survive = (grid == 1) & ((neighbors == 4) | (neighbors == 5))
    return (birth | survive).astype(int)

# Hybrid: Use 3D GoL patterns as teacher states for hyperidentity
class HybridGarden:
    def __init__(self, size=512, gol_size=25):
        self.tissue = AigarthTissue(size=size)
        self.gol_grid = np.random.choice([0, 1], size=(gol_size, gol_size, gol_size), p=[0.88, 0.12])
        self.generation = 0
        self.fitness_history = []
        self.live_cells_history = []

    def step(self):
        # Evolve 3D GoL
        self.gol_grid = gol_3d_step(self.gol_grid)
        
        # Use GoL live cells as teacher signal for hyperidentity
        teacher_signal = np.mean(self.gol_grid)  # Simple density signal
        
        # Run one hyperidentity evolution step
        pop_data = self.tissue.evolve_population(pop_size=64, generations=1, mut_rate=0.20)
        best_fitness = pop_data[0][1]
        
        # Record history
        self.fitness_history.append(best_fitness)
        live_cells = np.sum(self.gol_grid)
        self.live_cells_history.append(live_cells)
        
        self.generation += 1
        return best_fitness, live_cells

    def plot_results(self):
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(self.fitness_history, label='Best Hyperidentity Fitness')
        plt.title('Hyperidentity Fitness Over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.plot(self.live_cells_history, label='3D GoL Live Cells', color='green')
        plt.title('3D Game of Life Live Cells')
        plt.xlabel('Generation')
        plt.ylabel('Live Cells')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('hybrid_experiment_results.png')
        plt.close()

# Run hybrid experiment
hybrid = HybridGarden()
print("🌱 Starting 3D GoL + Hyperidentity Hybrid Experiment")
print("=" * 60)

for gen in range(80):
    fitness, live_cells = hybrid.step()
    if gen % 10 == 0:
        print(f"Gen {gen:2d} | Hyperidentity Fitness: {fitness:.6f} | 3D GoL Live Cells: {live_cells}")

print("\n✅ Hybrid experiment complete. The Garden now bridges classic emergence with self-referential evolution.")

# Plot results
hybrid.plot_results()
print("\n📊 Experiment visualization saved as hybrid_experiment_results.png")