"""
CSV to JSON Converter
Author: 7xmohamed
GitHub:  https://github.com/7xmohamed
website: https://7xmohamed.com

Convert a CSV file to a JSON file via command line input.
Supports both header and non-header CSV formats.
"""

import csv
import json
import os
from typing import List, Dict


def read_csv_with_header(csv_path: str) -> List[Dict[str, str]]:
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [
            {k.strip().lower(): v for k, v in row.items() if k is not None}
            for row in reader
        ]


def read_csv_without_header(csv_path: str) -> List[Dict[str, str]]:
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return [{"col_" + str(i): val for i, val in enumerate(row)} for row in reader]


def write_json(data: List[Dict[str, str]], output_path: str) -> None:
    with open(output_path, mode='w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    print("🔧 CSV to JSON Converter")
    print("👤 Author: 7xmohamed")

    csv_path = input("📁 Enter path to CSV file: ").strip()
    if not os.path.isfile(csv_path):
        print("❌ File not found. Please check the path and try again.")
        return

    has_header_input = input("🧾 Does the CSV file have a header? (y/n): ").strip().lower()
    has_header = has_header_input == 'y'

    json_path = input("💾 Enter path to save JSON file (default: filex.json): ").strip() or "filex.json"

    try:
        data = read_csv_with_header(csv_path) if has_header else read_csv_without_header(csv_path)
        write_json(data, json_path)
        print(f"✅ Successfully converted {len(data)} rows to → {json_path}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()