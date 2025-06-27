'''src/traffic_monitor/formatter.py

Formatter: formats and outputs traffic stats in table, CSV, or JSON formats.
'''
import os
import csv
import json
import logging
from typing import List, Dict
from pathlib import Path
from tabulate import tabulate

class Formatter:
    """
    Formats and outputs traffic stats.

    Supported formats:
      - table: pretty-printed to stdout
      - csv: writes file 'traffic_stats.csv' in output_dir
      - json: writes file 'traffic_stats.json' in output_dir
    """
    def __init__(self, stats: List[Dict[str, int]], output_dir: str = '.'):
        self.stats = stats
        self.output_dir = Path(output_dir)
        self.logger = logging.getLogger(__name__)

    def print(self, fmt: str):
        fmt = fmt.lower()
        if fmt == 'table':
            self._print_table()
        elif fmt == 'csv':
            self._write_csv()
        elif fmt == 'json':
            self._write_json()
        else:
            self.logger.error(f"Unsupported format: {fmt}")
            raise ValueError(f"Unsupported format: {fmt}")

    def _print_table(self):
        headers = ['Repo', 'Views', 'Unique Views', 'Clones', 'Unique Clones']
        rows = [
            [s['name'], s['views_count'], s['views_uniques'], s['clones_count'], s['clones_uniques']]
            for s in self.stats
        ]
        table = tabulate(rows, headers=headers, tablefmt='github')
        print(table)

    def _write_csv(self):
        file_path = self.output_dir / 'traffic_stats.csv'
        headers = ['name', 'views_count', 'views_uniques', 'clones_count', 'clones_uniques']
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for s in self.stats:
                    writer.writerow(s)
            self.logger.info(f"CSV written to {file_path}")
        except Exception as e:
            self.logger.error(f"Error writing CSV: {e}")
            raise

    def _write_json(self):
        file_path = self.output_dir / 'traffic_stats.json'
        try:
            with open(file_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(self.stats, jsonfile, indent=2)
            self.logger.info(f"JSON written to {file_path}")
        except Exception as e:
            self.logger.error(f"Error writing JSON: {e}")
            raise
'''}
