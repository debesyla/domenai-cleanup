#!/usr/bin/env python3
"""
Generic domain removal utility
Remove domains from assets/input-all.txt that exist in assets/input-removees.txt
Results saved to assets/output-removed.txt
"""

import os
from pathlib import Path

# Define paths (following project convention with assets folder)
INPUT_ALL_FILE = Path("assets/input-all.txt")
INPUT_REMOVEES_FILE = Path("assets/input-removees.txt")
OUTPUT_FILE = Path("assets/output-removed.txt")

def remove_domains():
    # Check if input files exist
    if not INPUT_ALL_FILE.exists():
        print(f"❌ Input file not found: {INPUT_ALL_FILE}")
        return

    if not INPUT_REMOVEES_FILE.exists():
        print(f"❌ Removees file not found: {INPUT_REMOVEES_FILE}")
        return

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Read excluded domains into a set (memory efficient for deduplication)
    print(f"Loading domains to remove from {INPUT_REMOVEES_FILE}...")
    excluded_domains = set()
    with open(INPUT_REMOVEES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            domain = line.strip()
            if domain:
                excluded_domains.add(domain)

    print(f"Loaded {len(excluded_domains)} domains to remove")

    # Read full list and filter
    print(f"Processing {INPUT_ALL_FILE}...")
    filtered_domains = []
    with open(INPUT_ALL_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            domain = line.strip()
            if domain and domain not in excluded_domains:
                filtered_domains.append(domain)

    print(f"Filtered {len(filtered_domains)} domains (removed {len(excluded_domains)} existing domains)")

    # Write results
    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for domain in filtered_domains:
            f.write(domain + '\n')

    print(f"✅ Done! Result saved to {OUTPUT_FILE}")
    print(f"Total domains in output: {len(filtered_domains)}")

if __name__ == "__main__":
    remove_domains()
