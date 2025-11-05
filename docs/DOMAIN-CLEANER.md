## ✅ Recommended folder structure

```
project-root/
│
├── assets/
│   ├── input.txt         # raw list of domains or URLs (domain_cleaner.py)
│   ├── output.txt        # cleaned and deduped root domains (domain_cleaner.py)
│   ├── input-all.txt     # full domain list (remove_domains.py)
│   ├── input-removees.txt # domains to remove (remove_domains.py)
│   ├── output-removed.txt # filtered results (remove_domains.py)
│   └── sample/           # (optional) example datasets for testing
│
├── src/
│   ├── domain_cleaner.py # main cleaning logic
│   ├── remove_domains.py # domain subtraction utility
│   ├── utils/            # (optional) small helper scripts if needed
│   └── __init__.py
│
├── docs/
│   └── DOMAIN-CLEANER.md # documentation (this file)
│
├── .gitignore
├── requirements.txt
└── run.sh                # optional: single-line script to launch cleaner
```

---

## 🧾 `/docs/DOMAIN-CLEANER.md`

```markdown
# 🧹 Domain Cleaner Utility

## Overview

**Domain Cleaner** is a lightweight Python utility designed to prepare raw .lt (Lithuanian) domain data for detailed domain analysis.  
It reads a plain-text list of domains or URLs, cleans and normalizes them, handles government vs. commercial domain rules, removes duplicates, and outputs a tidy `.txt` list ready for bulk domain checkers.

This tool is ideal for preprocessing .lt domains before bulk WHOIS, DNS, or HTTP checks.

---

## 📁 Folder Structure

```

project-root/
├── assets/
│   ├── input.txt   # raw .lt domain input data (one domain or URL per line)
│   └── output.txt  # cleaned and deduplicated output (one domain per line)
│
├── src/
│   └── domain_cleaner.py  # main cleaning script
│
└── docs/
└── DOMAIN-CLEANER.md  # this documentation

````

---

## ⚙️ How It Works

1. **Reads** a text file with one .lt domain or URL per line.  
2. **Normalizes** the value (removes `http://`, `https://`, `www.`, paths, etc.).  
3. **Extracts** the domain using [`tldextract`](https://pypi.org/project/tldextract/).  
4. **Applies .lt domain rules**:
   - **Government domains** (`.lrv.lt`, `.edu.lt`, `.mil.lt`, `.gov.lt`): Preserves subdomains
   - **Commercial domains**: Strips subdomains (keeps only `example.lt`, drops `blog.example.lt`)
5. **Deduplicates** results.  
6. **Outputs** the cleaned list to `assets/output.txt` (one domain per line, ready for bulk domain checkers).

---

## 🐍 Example Script: `/src/domain_cleaner.py`

```python
from urllib.parse import urlparse
import tldextract

INPUT_FILE = "assets/input.txt"
OUTPUT_FILE = "assets/output.txt"

def clean_domains():
    cleaned = set()

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if not raw:
                continue

            ext = tldextract.extract(raw)
            if not ext.domain or not ext.suffix:
                continue

            # Domain reconstruction with .lt government domain rules
            domain = f"{ext.domain}.{ext.suffix}"
            
            # Government/institutional domains - preserve subdomains
            if ext.suffix in ['lrv.lt', 'edu.lt', 'mil.lt', 'gov.lt']:
                if ext.subdomain:
                    domain = f"{ext.subdomain}.{domain}"
            # All other domains - strip subdomains
            elif ext.subdomain:
                continue  # Skip, use root domain only

            cleaned.add(domain.lower())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for domain in sorted(cleaned):
            f.write(domain + "\n")

    print(f"✅ {len(cleaned)} unique root domains saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_domains()
````

---

## 🧩 Requirements

Install dependencies once:

```bash
pip install tldextract
```

Create a `requirements.txt` file for easier environment setup:

```
tldextract
```

---

## ▶️ Usage

Place your raw domain list in `assets/input.txt`, one per line.

Then run:

```bash
python3 src/domain_cleaner.py
```

or if it’s in the root folder:

```bash
python3 domain-cleaner.py
```

Output will be written to:

```
assets/output.txt
```

---

## 🧠 Notes

* **Lithuanian domain focus**: Specifically designed for .lt domain preprocessing
* **Government domain handling**: Preserves subdomains for `.lrv.lt`, `.edu.lt`, `.mil.lt`, `.gov.lt`
* **Commercial domain handling**: Strips subdomains (i.e., `blog.example.lt` → `example.lt`)
* **URL handling**: Processes full URLs like `https://subdomain.example.lt/path` correctly
* **Performance**: Memory efficient with `set()` deduplication, handles thousands of domains quickly
* **Output format**: One domain per line, ready for detailed domain checkers
* **Error tolerance**: Ignores invalid entries (empty lines, malformed URLs)
* **Cross-platform**: Works on Linux, macOS, Windows

---

```

---

## 🗑️ Domain Removal Utility

**New in v1.6**: A companion utility for subtracting processed domains from larger lists.

### Purpose
Remove domains that have already been processed from a full domain list. Useful for:
- Subtracting completed batches from full datasets
- Filtering out domains that failed previous checks
- Creating incremental processing workflows

### Usage

1. Place your full domain list in `assets/input-all.txt`
2. Place domains to remove in `assets/input-removees.txt`
3. Run the utility:

```bash
python3 src/remove_domains.py
```

### Example Files

**`assets/input-all.txt`** (full list):
```
example.lt
blog.example.lt
subdomain.lrv.lt
processed.lt
another.lt
```

**`assets/input-removees.txt`** (domains to remove):
```
processed.lt
blog.example.lt
```

**`assets/output-removed.txt`** (result):
```
example.lt
subdomain.lrv.lt
another.lt
```

**`output.txt`** (result):
```
example.lt
subdomain.lrv.lt
another.lt
```

### Script: `/src/remove_domains.py`

```python
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
```

### Performance
- **Memory efficient**: Uses `set()` for fast lookups
- **Large file support**: Handles millions of domains
- **Fast processing**: Linear time complexity O(n + m)

---

## 🔮 Future Improvements

* Add CLI flags (`--input`, `--output`)
* Add optional filters (TLD whitelist, blacklist, domain length)
* Add logging / progress display
* Integrate with next-stage checkers (WHOIS, HTTP, DNS)

---

## 🧰 Quick Run Script (Optional)

Add a small `run.sh` for convenience:

```bash
#!/bin/bash
python3 src/domain_cleaner.py
```

Then simply run:

```bash
./run.sh
```

---

## ✅ Summary

This mini-app serves as the **first pipeline step** for .lt domain intelligence work:

* **Cleans .lt domain data** with Lithuanian-specific business rules
* **Preserves government subdomains** while stripping commercial ones  
* **Standardizes output format** (one domain per line)
* **Ensures deduplication** and performance optimization
* **Prepares data** for detailed domain checkers (WHOIS, DNS, HTTP analysis)

Ideal before bulk domain analysis or connecting with automated domain checking tools.

```
