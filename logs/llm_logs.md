# LLM Usage Log

## Project
### Faculty Finder – End-to-End Data Engineering Pipeline for Faculty Search

---

## Why This Log Exists

This project used a Large Language Model (LLM) as a development assistant during design,
debugging, and documentation phases.

The LLM was used to:
- Clarify data engineering concepts
- Suggest alternative designs
- Debug errors and edge cases
- Improve code readability and robustness

IMPORTANT:
- All prompts were explicitly written by the developer
- All outputs were reviewed, modified, or rewritten manually
- Final implementation decisions were made by the developer
- No code was blindly copied without validation

This log documents **where and how the LLM was realistically used**.

---

## Usage Timeline (Honest Data Engineering Record)


### Entry 01 — Pipeline Design Validation

**Stage:** Project Planning

**Date:** 2026-01-15

**Problem:**
To validate whether the proposed project flow followed standard data engineering practices.

**Prompt Type:**
“How should an end-to-end data engineering pipeline be structured?”

**LLM Contribution:**

Suggested separation into:
- Ingestion
- Transformation
- Storage
- Serving

**Human Decision:**

Refined the design to:
- Keep scraping and transformation separate
- Store raw data before cleaning
- Make transformation re-runnable independently

**Outcome:**
Prevented tight coupling between scraping and transformation logic.

---

### Entry 02 — Web Scraping Structure Confusion

**Stage:** Ingestion

**Date:** 2026-01-16

**Problem:**
Faculty pages had inconsistent HTML structures across categories.

**Prompt Type:**
“How to handle inconsistent HTML while scraping with BeautifulSoup?”

**LLM Contribution:**
Suggested fallback selectors and defensive parsing.

**Human Debugging:**
- Inspected HTML manually
- Identified alternate class names
- Implemented conditional extraction logic

**Outcome:**
Scraper became resilient to layout variations.

---

### Entry 03 — Email and Encoding Issues

**Stage:** Transformation

**Date:** 2026-01-16

**Problem:**
Emails were obfuscated and addresses contained UTF encoding artifacts.

**Prompt Type:**
“How to normalize obfuscated emails and fix encoding issues?”

**LLM Contribution:**
Suggested string replacement and regex-based cleanup.

**Human Validation:**
- Tested multiple records manually
- Refined regex to avoid data loss

**Outcome:**
Accurate email normalization and clean address fields.

---

### Entry 04 — CSV as an Intermediate Contract

**Stage:** Transformation

**Date:** 2026-01-17

**Problem:**
Deciding whether CSV should be treated as a temporary artifact or a formal contract.

**Prompt Type:**
“Is it good practice to treat transformed CSV files as data contracts?”

**LLM Contribution:**
Suggested that CSV can serve as a stable interface between transformation and storage layers.

**Human Implementation:**
- Treated the CSV schema as fixed
- Validated columns before database loading

**Outcome:**
Reduced coupling between transformation and storage layers.

---

### Entry 05 — Search Strategy for Research Tags

**Stage:** Serving

**Date:** 2026-01-17

**Problem:**
Determining how to search faculty records by research interests efficiently.

**Prompt Type:**
“How to implement simple search over research tags in SQLite?”

**LLM Contribution:**
Suggested LIKE-based filtering for small datasets.

**Human Validation:**
- Confirmed dataset size was manageable
- Verified query performance manually
- Ensured case-insensitive matching

**Outcome:**
Search functionality implemented without unnecessary complexity.

---

### Entry 06 — API Endpoint Granularity

**Stage:** Serving

**Date:** 2026-01-17

**Problem:**
Uncertainty about whether to expose multiple small endpoints or a limited set of generic endpoints.

**Prompt Type:**
“How many endpoints should a small FastAPI data service expose?”

**LLM Contribution:**
Suggested keeping endpoints minimal and focused to avoid over-engineering.

**Human Decision:**

- Fetch faculty by ID
- Search faculty by research tag
- Avoided premature pagination and filtering logic

**Outcome:**
API remained simple, readable, and aligned with project scope.

---

## What the LLM Did NOT Do:
- Did NOT scrape websites
- Did NOT decide the architecture independently
- Did NOT deploy or run code
- Did NOT validate outputs
- Did NOT replace human debugging or reasoning

---

## Final Declaration:
This project represents **human-led data engineering with LLM assistance**.
The LLM served as a **thinking and debugging assistant**,
while **all design choices, implementations, testing, and validations were performed manually**.

**Developer**: Sanil Shah and Divya Mashruwala<br>
**Role**: Data Engineer<br>
**Project**: Faculty Finder