# Faculty Finder – Data Engineering Pipeline

## Overview
**Faculty Finder** is an end-to-end **Data Engineering project** that builds a structured pipeline to extract, clean, store, and serve faculty information from a university website.  
The system converts unstructured web data into a **queryable, API-driven dataset**, enabling future use cases such as **faculty recommendation systems, internship discovery, and chatbot-based search**.

This repository focuses on the **Data Engineering lifecycle**, covering ingestion, transformation, storage, and serving layers using industry-aligned practices.

---

## Problem Statement
Faculty information is typically scattered across multiple web pages and directories in unstructured HTML format.  
Students face difficulty identifying relevant faculty members based on research interests, academic background, or expertise areas.

Before applying NLP or semantic search, a **reliable and reproducible data pipeline** is required to extract, clean, and organize this information into a structured format.

---

## Solution
This project implements a **production-style ETL pipeline** that:

- Scrapes faculty data from multiple directories
- Normalizes and cleans inconsistent web data
- Stores structured data in a relational database
- Exposes read-only APIs for downstream applications

The pipeline is modular, idempotent, and designed for safe re-execution.

---

## Architecture

University Website<br>
↓<br>
Web Scraping (Requests + BeautifulSoup)<br>
↓<br>
Raw JSON Data<br>
↓<br>
Data Cleaning & Transformation (Pandas)<br>
↓<br>
Clean CSV Dataset<br>
↓<br>
SQLite Database<br>
↓<br>
FastAPI (Read-Only APIs)<br>

---

## 🧩 Pipeline Components

### 1️ Ingestion
- Scrapes multiple faculty categories:
  - Faculty
  - Adjunct Faculty
  - Distinguished Professors
  - Professors of Practice
- Handles pagination and inconsistent HTML structures
- Collects profile-level data from faculty pages
- Stores raw scraped output in JSON format

---

### 2️ Transformation
The transformation layer prepares high-quality, analysis-ready data:

- Email and phone number normalization
- UTF-8 encoding cleanup
- Handling missing values
- Tokenization of research areas
- Generation of searchable **research tags**
- Creation of a natural-language **bio** field
- Creation of a `combined_text` column for future NLP usage

The transformed dataset is exported as CSV and JSON.

---

### 3️ Storage
- SQLite used for lightweight, relational storage
- Schema-driven table design
- Idempotent schema creation
- Safe re-runs without schema conflicts
- Structured columns for analytics and APIs

---

### 4️ Serving (API Layer)
A **FastAPI-based read-only API** exposes faculty data for consumption.

| Endpoint | Description |
|--------|------------|
| `GET /faculty` | Fetch all faculty records |
| `GET /faculty/{id}` | Fetch faculty by ID |
| `GET /faculty/search/?tag=<keyword>` | Search faculty by research tag |

Swagger UI is available at:
http://127.0.0.1:8000/docs


---

## 📁 Repository Structure

Assignment1/<br>
│<br>
├── api/<br>
│   └── main.py<br>
│<br>
├── data/<br>
│   |── daiict_faculty_transformed.json<br>
|   |── daiict_faculty_transformed.csv<br>
|   └── daiict_all_faculty_raw.json<br>
│<br>
├── db/<br>
│   ├── schema.sql<br>
│   └── faculty_finder.db<br>
│<br>
├── logs/<br>
│   └── llm_logs.md<br>
│<br>
├── load_to_sqlite.py<br>
├── all_faculty_scrapper.py<br>
├── daiict_faculty_transformed.py<br>
├── run_schema.py<br>
└── README.md<br>

---

## ▶️ How to Run

### 1️ Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# Linux/Mac: source venv/bin/activate
# Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2️ Scrape Faculty Data
```bash
python scraper/all_faculty_scrapper.py
```
### 3️ Transform Data
```bash
python transform/daiict_faculty_transformed.py
```

### 4️ Load Data into Database
```bash
python load_to_sqlite.py
```

### 5️ Start API Server
```bash
uvicorn main:app --reload
```
---

## 🎓 Learning Outcomes

- End-to-end data pipeline design
- Web scraping and data ingestion
- Data cleaning and transformation
- Schema design and relational storage
- API development using FastAPI

- Modular and maintainable code organization

