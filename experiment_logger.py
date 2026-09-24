#!/usr/bin/env python3
import os
import sys
import json
import numpy as np
from datetime import datetime
import subprocess

sys.path.append('/home/durdyh2o/Aigarth-Garden-Labs/simulations')
from hyper_tissue import AigarthTissue

class HyperidentityExperimentLogger:
    def __init__(self, log_dir='/home/durdyh2o/Aigarth-Garden-Labs/logs/hyperidentity'):
        """
        Initialize experiment logger for Hyperidentity neural tissue experiments
        
        Args:
            log_dir (str): Directory to store experiment logs
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Git repository tracking
        self.repo_path = '/home/durdyh2o/Aigarth-Garden-Labs'
        
    def get_git_info(self):
        """
        Retrieve current git repository information
        
        Returns:
            dict: Git repository details
        """
        try:
            # Current branch
            branch = subprocess.check_output(
                ['git', '-C', self.repo_path, 'rev-parse', '--abbrev-ref', 'HEAD'], 
                text=True
            ).strip()
            
            # Latest commit
            commit = subprocess.check_output(
                ['git', '-C', self.repo_path, 'rev-parse', 'HEAD'], 
                text=True
            ).strip()
            
            # Uncommitted changes
            status = subprocess.check_output(
                ['git', '-C', self.repo_path, 'status', '--porcelain'], 
                text=True
            )
            has_uncommitted = bool(status.strip())
            
            return {
                'branch': branch,
                'commit': commit,
                'has_uncommitted_changes': has_uncommitted
            }
        except Exception as e:
            return {
                'error': str(e),
                'details': 'Unable to retrieve git information'
            }
    
    def run_experiment(self, 
                       size=512, 
                       seed=86, 
                       pop_size=128, 
                       generations=10, 
                       mut_rate=0.20):
        """
        Run a Hyperidentity neural tissue experiment and log results
        
        Args:
            size (int): Tissue size
            seed (int): Random seed
            pop_size (int): Population size
            generations (int): Number of generations
            mut_rate (float): Mutation rate
        
        Returns:
            dict: Experiment results and log details
        """
        # Timestamp for this experiment
        timestamp = datetime.now().isoformat()
        
        # Create tissue
        tissue = AigarthTissue(size=size, seed=seed)
        
        # Run evolution
        population = tissue.evolve_population(
            pop_size=pop_size, 
            generations=generations, 
            mut_rate=mut_rate
        )
        
        # Analyze population
        fitness_scores = [fit for _, fit in population]
        
        # Prepare experiment log
        experiment_log = {
            'timestamp': timestamp,
            'parameters': {
                'size': size,
                'seed': seed,
                'population_size': pop_size,
                'generations': generations,
                'mutation_rate': mut_rate
            },
            'results': {
                'best_fitness': max(fitness_scores),
                'worst_fitness': min(fitness_scores),
                'mean_fitness': np.mean(fitness_scores),
                'fitness_std': np.std(fitness_scores)
            },
            'git_info': self.get_git_info()
        }
        
        # Save log file
        log_filename = f"{timestamp.replace(':', '-')}_hyperidentity_log.json"
        log_path = os.path.join(self.log_dir, log_filename)
        
        with open(log_path, 'w') as f:
            json.dump(experiment_log, f, indent=2)
        
        print(f"Experiment log saved: {log_path}")
        return experiment_log
    
    def generate_summary(self, num_logs=10):
        """
        Generate a summary of recent experiments
        
        Args:
            num_logs (int): Number of recent logs to summarize
        
        Returns:
            dict: Experiment summary
        """
        # Get all log files, sorted by timestamp
        log_files = sorted(
            [f for f in os.listdir(self.log_dir) if f.endswith('_hyperidentity_log.json')],
            reverse=True
        )
        
        # Limit to recent logs
        recent_logs = log_files[:num_logs]
        
        summary = {
            'total_experiments': len(recent_logs),
            'experiments': []
        }
        
        for log_file in recent_logs:
            with open(os.path.join(self.log_dir, log_file), 'r') as f:
                log_data = json.load(f)
                summary['experiments'].append({
                    'timestamp': log_data['timestamp'],
                    'best_fitness': log_data['results']['best_fitness'],
                    'mean_fitness': log_data['results']['mean_fitness'],
                    'branch': log_data['git_info'].get('branch', 'unknown')
                })
        
        return summary

def main():
    logger = HyperidentityExperimentLogger()
    
    if len(sys.argv) < 2:
        print("Hyperidentity Experiment Logger")
        print("Usage:")
        print("  python experiment_logger.py run [size] [seed] [pop_size] [generations] [mut_rate]")
        print("  python experiment_logger.py summary [num_logs]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'run':
        # Default parameters or user-specified
        params = [int(p) for p in sys.argv[2:]] if len(sys.argv) > 2 else []
        logger.run_experiment(*params)
    
    elif command == 'summary':
        num_logs = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        summary = logger.generate_summary(num_logs)
        print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()