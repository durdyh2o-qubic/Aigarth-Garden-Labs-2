#!/usr/bin/env python3
"""
Aigarth Garden: Hyperidentity Evolution Observatory

Lightweight data analysis for mining and simulation results.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def load_mining_logs(path):
    """Load and validate mining logs."""
    try:
        df = pd.read_csv(path)
        print(f"Mining Logs: {len(df)} entries")
        return df
    except Exception as e:
        print(f"Error loading mining logs: {e}")
        return None

def load_simulation_results(path):
    """Load and validate simulation results."""
    try:
        df = pd.read_csv(path)
        print(f"Simulation Results: {len(df)} generations")
        return df
    except Exception as e:
        print(f"Error loading simulation results: {e}")
        return None

def visualize_performance(mining_df, sim_df):
    """Create performance visualization."""
    plt.figure(figsize=(12, 6))
    
    if mining_df is not None:
        plt.subplot(1, 2, 1)
        plt.plot(mining_df['it_s'], label='Iterations/Second')
        plt.title('Mining Performance')
        plt.xlabel('Log Entry')
        plt.ylabel('it/s')
        plt.legend()
    
    if sim_df is not None:
        plt.subplot(1, 2, 2)
        plt.plot(sim_df['best_fitness'], label='Best Fitness')
        plt.title('Simulation Fitness')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.legend()
    
    plt.tight_layout()
    plt.show()

def main():
    """Main analysis workflow."""
    mining_logs_path = Path('../mining-logs/parsed_results.csv')
    sim_results_path = sorted(Path('../results').glob('results_mut*.csv'))[-1]
    
    mining_df = load_mining_logs(mining_logs_path)
    sim_df = load_simulation_results(sim_results_path)
    
    visualize_performance(mining_df, sim_df)

if __name__ == "__main__":
    main()