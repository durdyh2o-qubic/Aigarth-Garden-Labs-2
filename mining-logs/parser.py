import re
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging

def parse_qubic_log(log_text: str, filename: str = "unknown") -> pd.DataFrame:
    """Parse real Qubic trainer logs"""
    lines = log_text.splitlines()
    data = []
    current_seed = None
    current_time = None

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    for line in lines:
        try:
            # Extract timestamp if available
            time_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)', line)
            if time_match:
                current_time = time_match.group(1)

            # Extract Mining Seed
            if "Mining Seed:" in line:
                current_seed = line.split("Mining Seed:")[-1].strip()

            # Parse performance line
            if "it/s" in line and "SHARES" in line:
                match = re.search(
                    r'E:(\d+).*?SHARES:\s*(\d+)/(\d+).*?(\d+)\s*it/s.*?\s*(\d+)\s*avg it/s', 
                    line, 
                    re.IGNORECASE
                )
                if match:
                    entry = {
                        'timestamp': current_time or datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'epoch': int(match.group(1)),
                        'shares_found': int(match.group(2)),
                        'shares_total': int(match.group(3)),
                        'it_s': int(match.group(4)),
                        'avg_it_s': int(match.group(5)),
                        'seed': current_seed,
                        'efficiency': round(int(match.group(2)) / int(match.group(3)), 4) if int(match.group(3)) > 0 else 0,
                        'log_file': filename
                    }
                    data.append(entry)
                    
                    # Log unusual entries
                    if entry['shares_found'] > entry['shares_total']:
                        logger.warning(f"Unusual share ratio in log: {entry}")

        except Exception as e:
            # Catch and log parsing errors
            logger.error(f"Error parsing line: {line}")
            logger.exception(e)

    df = pd.DataFrame(data)
    
    # Basic data validation
    if df.empty:
        logger.warning(f"No entries parsed from log file: {filename}")
    
    return df

def main():
    log_path = Path("mining-logs/latest_log.txt")
    
    try:
        if not log_path.exists():
            print("❌ Error: Place your latest mining log as mining-logs/latest_log.txt")
            return

        log_text = log_path.read_text()
        df = parse_qubic_log(log_text, log_path.name)
        
        if not df.empty:
            print(df[['timestamp', 'epoch', 'it_s', 'avg_it_s', 'efficiency', 'seed']])
            
            # Flexible output options
            output_csv = "mining-logs/parsed_results.csv"
            output_json = "mining-logs/parsed_results.json"
            
            df.to_csv(output_csv, index=False)
            df.to_json(output_json, orient='records')
            
            print(f"✅ Parsed {len(df)} entries")
            print(f"   → {output_csv}")
            print(f"   → {output_json}")
        else:
            print("❌ No parsable entries found in the log")

    except Exception as e:
        print(f"❌ Error processing log: {e}")

if __name__ == "__main__":
    main()