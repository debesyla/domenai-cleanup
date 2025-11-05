import tldextract
from pathlib import Path
import re
from urllib.parse import urlparse

INPUT_FILE = Path("assets/input.txt")
OUTPUT_FILE = Path("assets/output.txt")

# Lithuanian government/institutional domains and special suffixes
GOV_DOMAINS = {"lrv", "edu", "mil"}
GOV_SUFFIXES = {"lrv.lt", "edu.lt", "mil.lt", "gov.lt"}

def clean_domains():
    if not INPUT_FILE.exists():
        print(f"❌ Input file not found: {INPUT_FILE}")
        return

    cleaned = set()
    errors = []
    processed_count = 0
    skipped_count = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        line_count = 0
        for line in f:
            line_count += 1
            if line_count % 1000 == 0:
                print(f"...processed {line_count} lines...")

            raw_line = line.rstrip("\n")

            # Ignore empty lines entirely (do not count or log them)
            if not raw_line.strip():
                continue

            processed_count += 1
            domain, reason = process_domain(raw_line)
            if domain:
                cleaned.add(domain.lower())
            else:
                skipped_count += 1
                errors.append((line_count, raw_line, reason))


    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for domain in sorted(cleaned):
            f.write(domain + "\n")

    # Write errors to assets/errors.txt
    errors_file = Path("assets/errors.txt")
    with open(errors_file, "w", encoding="utf-8") as ef:
        for line_num, line_val, reason in errors:
            # Skip logging empty lines to errors file per request
            if reason == "empty line":
                continue
            ef.write(f"Line {line_num}: {reason} | {line_val}\n")

    print(f"✅ Cleaned {len(cleaned)} unique .lt domains saved to {OUTPUT_FILE}")
    print(f"Processed {processed_count} non-empty lines.")
    print(f"⚠️ {skipped_count} lines skipped. See {errors_file} for details.")

def is_valid_domain_length(domain: str) -> tuple[bool, str | None]:
    """Validate domain length. Returns (is_valid, reason).
    
    Domain labels must be 1-63 characters. Single character domains are illegal.
    """
    labels = domain.split('.')
    for label in labels:
        if len(label) == 1:
            return False, "single character label"
        if len(label) > 63:
            return False, "label exceeds 63 characters"
    return True, None

def is_valid_hyphen_rules(domain: str) -> tuple[bool, str | None]:
    """Validate hyphen rules. Returns (is_valid, reason).
    
    Hyphens are legal but cannot be:
    - First character of a label
    - Last character of a label
    - Two in a row (consecutive hyphens)
    """
    labels = domain.split('.')
    for label in labels:
        if label.startswith('-'):
            return False, "hyphen at start of label"
        if label.endswith('-'):
            return False, "hyphen at end of label"
        if '--' in label:
            return False, "consecutive hyphens"
    return True, None

def process_domain(raw: str):
    """Process a single raw input line. Returns (domain, None) on success or (None, reason) on skip.

    Normalizes, strips trailing dots, handles URLs, removes www., skips IPs and invalid characters,
    and only returns .lt domains with government subdomain preservation rules.
    """
    if raw is None:
        return None, "empty"

    cleaned = raw.strip()
    if not cleaned:
        return None, "empty line"

    # Strip trailing dots
    cleaned = cleaned.rstrip('.')

    # If input is a URL, extract netloc
    if re.match(r'^[a-zA-Z]+://', cleaned):
        parsed = urlparse(cleaned)
        cleaned = parsed.netloc or cleaned

    # Remove www. prefix if present
    if cleaned.lower().startswith('www.'):
        cleaned = cleaned[4:]

    # Skip if it's an IP address
    if re.match(r'^\d+(\.\d+){3}$', cleaned):
        return None, "ip address"

    # Allow only valid domain characters (letters, digits, dash, dot)
    if not re.match(r'^[\w\-.]+$', cleaned, re.UNICODE):
        return None, "invalid characters"

    cleaned = cleaned.lower()

    ext = tldextract.extract(cleaned)
    if not ext.domain or not ext.suffix:
        return None, "invalid domain/suffix"

    suffix = ext.suffix
    domain = f"{ext.domain}.{suffix}"
    # Preserve government subdomains either by special suffixes or second-level gov domains
    if suffix in GOV_SUFFIXES or (suffix == "lt" and ext.domain in GOV_DOMAINS):
        if ext.subdomain:
            domain = f"{ext.subdomain}.{domain}"
        is_valid, reason = is_valid_domain_length(domain)
        if not is_valid:
            return None, reason
        is_valid, reason = is_valid_hyphen_rules(domain)
        if not is_valid:
            return None, reason
        return domain, None

    # Commercial .lt: reject if subdomain exists, otherwise accept
    if suffix == "lt":
        if ext.subdomain:
            return None, "non-govt subdomain"
        is_valid, reason = is_valid_domain_length(domain)
        if not is_valid:
            return None, reason
        is_valid, reason = is_valid_hyphen_rules(domain)
        if not is_valid:
            return None, reason
        return domain, None

    return None, "non-.lt domain"


if __name__ == "__main__":
    clean_domains()
