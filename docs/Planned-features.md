# Planned Features & Upcoming Updates

This file tracks the roadmap for new features and improvements to the Domain Cleaner utility.

---

## v1.1 Progress Logging ✅
- Show progress for large input files (e.g., every 1000 lines processed)
- Optional verbose mode for more detailed feedback

## v1.2 Error Reporting ✅
- Log or output skipped/invalid lines for review
- Option to save errors to a separate file

## v1.3 Unit Tests ✅
- Add automated tests for edge cases, government domain logic, and malformed input
- Improve reliability and maintainability

## v1.4 Robustness & Edge Case Handling ✅
- **Memory optimization**: Stream processing for very large files (millions of domains)
- **Multi-level subdomain handling**: Clarify and test behavior for `portal.admin.lrv.lt`
- **IDN support**: Handle Lithuanian characters (ąčęėįšųū) and Punycode domains
- **Input validation**: Filter IP addresses, trailing dots, invalid characters
- **Encoding flexibility**: Support multiple file encodings beyond UTF-8, handle BOM
- **Offline mode**: Configure tldextract caching for offline operation
- **Nested government domains**: Handle edge cases like `gov.edu.lt`

## v1.5 Domain Validation Rules ✅
- Add domain length validation (1-63 characters per label, reject single-character labels)
- Add hyphen validation (no hyphens at start/end of labels, no consecutive hyphens)
- Improved input normalization

## v1.6 Domain Removal Utility ✅
- Generic domain filtering tool (`src/remove_domains.py`)
- Remove domains from `assets/input-all.txt` that exist in `assets/input-removees.txt`
- Output clean list to `assets/output-removed.txt`
- Memory-efficient processing for large datasets (millions of domains)
- Useful for subtracting processed domains from full lists

---

## v2.0 Multiple File Input
- Support `/assets/input/` folder containing multiple `.txt` files
- Merge all input files and output a single deduplicated `output.txt`
- Useful for batch processing and combining datasets
- Progress tracking across multiple files

---

For more details, see the main documentation in [`DOMAIN-CLEANER.md`](DOMAIN-CLEANER.md).
