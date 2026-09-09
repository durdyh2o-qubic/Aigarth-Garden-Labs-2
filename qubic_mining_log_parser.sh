#!/bin/bash
# Qubic Mining Log Parser - 2-Hour Interval Data Collection

# Activate virtual environment
source ~/Aigarth-Garden-Labs/mining_env/bin/activate

# Change to project directory
cd ~/Aigarth-Garden-Labs

# Get current time in UTC
current_day=$(date -u +"%A")
current_time=$(date -u +"%H:%M")

# Check if it's Wednesday before 11:59 PM UTC
if [[ "$current_day" == "Wednesday" && "$current_time" < "11:59" ]]; then
    # Run the mining log parser
    python mining-logs/parser.py
    
    # Only keep the most recent parsing results and maintain a compact history
    find mining-logs/ -name "parsed_results.*" -mtime +7 -delete
    
    # Git operations to track and push changes
    git add mining-logs/parsed_results.csv mining-logs/parsed_results.json
    git commit -m "Update Mining Logs - $(date -u +"%Y-%m-%d %H:%M UTC")"
    git push origin main
else
    # If it's past Wednesday 11:59 PM UTC, generate final summary and stop
    echo "Epoch end time reached. Generating final summary."
    
    # Generate final summary with extended analytics
    python3 - << END
import pandas as pd
import json
import numpy as np
from datetime import datetime

try:
    # Read parsed results
    df = pd.read_csv('mining-logs/parsed_results.csv')

    # Advanced performance metrics
    summary = {
        'epoch_end_time': datetime.utcnow().isoformat(),
        'total_epochs': int(df['epoch'].max() - df['epoch'].min() + 1),
        'total_shares_found': int(df['shares_found'].sum()),
        'total_shares_attempted': int(df['shares_total'].sum()),
        'shares_success_rate': round(df['shares_found'].sum() / df['shares_total'].sum(), 4) * 100,
        'avg_efficiency': round(df['efficiency'].mean(), 4),
        'max_efficiency': round(df['efficiency'].max(), 4),
        'min_efficiency': round(df['efficiency'].min(), 4),
        'max_iterations_per_second': int(df['it_s'].max()),
        'avg_iterations_per_second': round(df['it_s'].mean(), 2),
        'mining_seed': df['seed'].iloc[0],
        
        # Statistical insights
        'iterations_stats': {
            'mean': round(df['it_s'].mean(), 2),
            'median': round(df['it_s'].median(), 2),
            'std_dev': round(df['it_s'].std(), 2)
        },
        'efficiency_stats': {
            'mean': round(df['efficiency'].mean(), 4),
            'median': round(df['efficiency'].median(), 4),
            'std_dev': round(df['efficiency'].std(), 4)
        }
    }

    # Write summary to JSON
    with open('mining-logs/epoch_final_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))

except Exception as e:
    print(f"Error generating summary: {e}")
END

    # Archive final logs with timestamp
    mkdir -p ~/Aigarth-Garden-Labs/mining-logs/archive/$(date -u +"%Y-%m-%d")
    cp mining-logs/latest_log.txt ~/Aigarth-Garden-Labs/mining-logs/archive/$(date -u +"%Y-%m-%d")/final_log_$(date -u +"%H%M%S").txt
    
    # Git operations for final commit
    git add mining-logs/epoch_final_summary.json
    git commit -m "Final Epoch Summary - $(date -u +"%Y-%m-%d %H:%M UTC")"
    git push origin main
    
    # Stop the cron job
    exit 1
fi