import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path

class AigarthHyperidentityVisualizer:
    def __init__(self, mining_logs_path='../mining-logs', 
                 results_path='../results', 
                 hyperidentity_path='../hyperidentity_logs'):
        """
        Initialize visualizer with paths to different data sources
        """
        self.mining_logs_path = Path(mining_logs_path)
        self.results_path = Path(results_path)
        self.hyperidentity_path = Path(hyperidentity_path)
        
        # Data storage
        self.mining_data = None
        self.hyperidentity_data = None
        
    def load_mining_logs(self):
        """
        Load and process mining logs
        """
        # Find most recent mining log
        mining_files = sorted(self.mining_logs_path.glob('qubic_mining_log_*.csv'), reverse=True)
        
        if not mining_files:
            print("No mining logs found. Using demo data.")
            # Generate demo mining data
            self.mining_data = pd.DataFrame({
                'timestamp': pd.date_range(start='2024-01-01', periods=100, freq='H'),
                'hashrate': np.random.normal(100, 20, 100),
                'shares_submitted': np.random.randint(50, 200, 100),
                'epoch': np.arange(100)
            })
        else:
            self.mining_data = pd.read_csv(mining_files[0])
        
        return self.mining_data
    
    def load_hyperidentity_data(self):
        """
        Load hyperidentity simulation results
        """
        hyperidentity_files = sorted(self.results_path.glob('results_mut_*.csv'), reverse=True)
        
        if not hyperidentity_files:
            print("No hyperidentity logs found. Using demo data.")
            # Generate demo hyperidentity data
            self.hyperidentity_data = pd.DataFrame({
                'generation': np.arange(100),
                'best_fitness': 0.5 + 0.1 * np.sin(np.arange(100)/10) + np.random.normal(0, 0.05, 100),
                'mutation_rate': 0.01 + 0.005 * np.sin(np.arange(100)/20)
            })
        else:
            self.hyperidentity_data = pd.read_csv(hyperidentity_files[0])
        
        return self.hyperidentity_data
    
    def create_neural_network_gif(self, output_path='../results/hyperidentity_neural_network.gif'):
        """
        Create an animated 3D visualization representing neural network evolution
        """
        # Ensure data is loaded
        mining_data = self.load_mining_logs()
        hyperidentity_data = self.load_hyperidentity_data()
        
        # Prepare figure
        fig = plt.figure(figsize=(12, 8), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        
        # Color map for neural network 'connections'
        colors = plt.cm.viridis(np.linspace(0, 1, len(hyperidentity_data)))
        
        # Initialization function
        def init():
            ax.clear()
            ax.set_xlabel('Mining Epoch')
            ax.set_ylabel('Hyperidentity Fitness')
            ax.set_zlabel('Neural Complexity')
            ax.set_title('Aigarth Hyperidentity Neural Network Evolution')
            return []
        
        # Animation update function
        def update(frame):
            ax.clear()
            
            # Plot data up to current frame
            data_slice = hyperidentity_data.iloc[:frame+1]
            
            # X: Mining Epoch, Y: Fitness, Z: Neural Complexity
            scatter = ax.scatter(
                data_slice['generation'], 
                data_slice['best_fitness'], 
                data_slice['mutation_rate'] * 1000,  # Scale mutation rate
                c=colors[:frame+1], 
                s=50 + data_slice['best_fitness'] * 500,  # Dynamic point size
                alpha=0.7,
                edgecolors='black',
                linewidths=0.5
            )
            
            # Connect points to simulate neural network connections
            for i in range(len(data_slice)-1):
                ax.plot(
                    data_slice['generation'].iloc[i:i+2], 
                    data_slice['best_fitness'].iloc[i:i+2], 
                    data_slice['mutation_rate'].iloc[i:i+2] * 1000, 
                    color='cyan', 
                    alpha=0.3, 
                    linewidth=1
                )
            
            ax.set_xlabel('Mining Epoch')
            ax.set_ylabel('Hyperidentity Fitness')
            ax.set_zlabel('Neural Complexity')
            ax.set_title(f'Aigarth Hyperidentity: Generation {frame}')
            
            return scatter
        
        # Create animation
        anim = FuncAnimation(
            fig, 
            update, 
            frames=len(hyperidentity_data), 
            init_func=init, 
            interval=100,  # milliseconds between frames
            blit=False
        )
        
        # Save as high-quality GIF
        anim.save(
            output_path, 
            writer='pillow', 
            fps=10,  # Frames per second
            dpi=100
        )
        
        plt.close(fig)
        print(f"✅ Neural Network Hyperidentity GIF saved to {output_path}")
        
    def generate_report(self):
        """
        Generate a markdown report of the visualization
        """
        report_path = self.results_path / 'hyperidentity_neural_network_report.md'
        
        with open(report_path, 'w') as f:
            f.write("# Aigarth Hyperidentity Neural Network Analysis\n\n")
            
            # Mining Log Summary
            f.write("## Mining Log Summary\n")
            f.write(f"- Total Epochs: {len(self.mining_data)}\n")
            f.write(f"- Average Hashrate: {self.mining_data['hashrate'].mean():.2f}\n")
            f.write(f"- Total Shares Submitted: {self.mining_data['shares_submitted'].sum()}\n\n")
            
            # Hyperidentity Summary
            f.write("## Hyperidentity Simulation Summary\n")
            f.write(f"- Total Generations: {len(self.hyperidentity_data)}\n")
            f.write(f"- Peak Fitness: {self.hyperidentity_data['best_fitness'].max():.4f}\n")
            f.write(f"- Average Mutation Rate: {self.hyperidentity_data['mutation_rate'].mean():.4f}\n")
        
        print(f"📄 Hyperidentity report generated: {report_path}")

# Main execution
visualizer = AigarthHyperidentityVisualizer()
visualizer.create_neural_network_gif()
visualizer.generate_report()