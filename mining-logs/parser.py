#!/usr/bin/env python3
import os
import re
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('mining-logs/parser.log'),
        logging.StreamHandler()
    ]
)

class QubicMiningLogParser:
    def __init__(self, log_path='mining-logs/latest_log.txt'):
        self.log_path = log_path
        self.parsed_data = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def parse_log(self):
        """
        Parse Qubic mining logs with robust handling of variable formats
        and comprehensive error tracking
        """
        self.parsed_data = []  # Reset parsed data
        
        try:
            with open(self.log_path, 'r') as log_file:
                raw_logs = log_file.readlines()
        except FileNotFoundError:
            self.logger.error(f"Log file not found: {self.log_path}")
            return []
        except PermissionError:
            self.logger.error(f"Permission denied reading: {self.log_path}")
            return []

        # Advanced parsing with multiple regex strategies
        parsing_patterns = [
            r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}).*',
            r'Iterations/s:\s*(?P<it_s>[\d.]+).*',
            r'Efficiency:\s*(?P<efficiency>[\d.]+%).*',
            r'Shares\s*:\s*(?P<shares_found>\d+)/(?P<shares_total>\d+).*',
            r'Epoch\s*:\s*(?P<epoch>\d+).*'
        ]

        parsed_lines = 0
        for line in raw_logs:
            for pattern in parsing_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    try:
                        parsed_entry = match.groupdict()
                        
                        # Type conversions and normalization
                        parsed_entry['timestamp'] = datetime.strptime(
                            parsed_entry.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 
                            '%Y-%m-%d %H:%M:%S'
                        )
                        parsed_entry['it_s'] = float(parsed_entry.get('it_s', 0))
                        parsed_entry['efficiency'] = float(
                            parsed_entry.get('efficiency', '0%').rstrip('%')
                        ) / 100
                        parsed_entry['shares_found'] = int(parsed_entry.get('shares_found', 0))
                        parsed_entry['shares_total'] = int(parsed_entry.get('shares_total', 1))
                        parsed_entry['epoch'] = int(parsed_entry.get('epoch', 0))
                        parsed_entry['seed'] = self._generate_mining_seed(line)
                        
                        self.parsed_data.append(parsed_entry)
                        parsed_lines += 1
                        break  # Stop checking other patterns for this line
                    except Exception as e:
                        self.logger.warning(f"Error parsing line: {line.strip()}. Error: {e}")

        self.logger.info(f"Parsed {parsed_lines} lines from {self.log_path}")
        return self.parsed_data

    def _generate_mining_seed(self, log_line):
        """
        Generate a deterministic seed based on log characteristics
        """
        return hash(log_line) % (2**32)

    def to_dataframe(self):
        """
        Convert parsed data to pandas DataFrame with robust handling
        """
        if not self.parsed_data:
            self.parse_log()
        
        if not self.parsed_data:
            self.logger.warning("No data parsed. Returning empty DataFrame.")
            return pd.DataFrame()
        
        df = pd.DataFrame(self.parsed_data)
        return df

    def save_results(
        self, 
        output_csv='mining-logs/parsed_results.csv', 
        output_json='mining-logs/parsed_results.json',
        output_excel='mining-logs/parsed_results.xlsx'
    ):
        """
        Save parsing results in multiple formats
        """
        df = self.to_dataframe()
        
        if df.empty:
            self.logger.warning("No data to save.")
            return
        
        try:
            # CSV for tabular analysis
            df.to_csv(output_csv, index=False)
            
            # JSON for structured data exchange
            df.to_json(output_json, orient='records', indent=2)
            
            # Excel for broader compatibility
            df.to_excel(output_excel, index=False)
            
            self.logger.info(f"Results saved: {output_csv}, {output_json}, {output_excel}")
        except Exception as e:
            self.logger.error(f"Error saving results: {e}")

def main():
    parser = QubicMiningLogParser()
    parser.parse_log()
    parser.save_results()

if __name__ == '__main__':
    main()