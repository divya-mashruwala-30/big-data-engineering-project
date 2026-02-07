# [Faculty Finder](https://faculty-find.streamlit.app/) – Data Engineering Pipeline

## Overview
[Faculty Finder](https://faculty-find.streamlit.app/) is an end-to-end **Data Engineering project** that builds a structured pipeline to extract, clean, store, and serve faculty information from a university website.  
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
<center>
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
↓<br>
FAISS Indexing on Faculty profiles<br>
↓<br>
Cosine Similarity for matching<br>
↓<br>
Docker for containerization and orchestration<br>
↓<br>
Streamlit for UI and deployment<br>
↓<br>

[Faculty Recommender System Web App](https://faculty-find.streamlit.app/)
</center>

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

### 5️ Recommender Application
A **Streamlit** dashboard that consumes the transformed CSV directly to provide interactive search and recommendations.
- **Input**: `daiict_faculty_transformed.csv`
- **Core Logic**: FAISS Indexing + Cosine Similarity
- **Output**: Ranked list of faculty profiles matching the query


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
├── recommender_app/<br>
│   |── Dockerfile.txt<br>
|   └── daiict_faculty_transformed.csv<br>
|   └── streamlit.py<br>
|   └── recommender.py<br>
|   └── requirements.txt<br>
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

## 📊 Dataset Insights & Analysis

After building the data pipeline and transforming the dataset, exploratory analysis was performed to understand the structure, distribution, and completeness of the faculty data.

---

### 🔹 Dataset Overview

- **Total Faculty Records:** 110  
- The dataset contains profiles from multiple faculty categories including core faculty, adjunct faculty, and professors of practice.

---

### 🔹 Faculty Distribution

| Faculty Type | Count |
|--------------|------|
| Faculty | 67 |
| Adjunct Faculty | 26 |
| Adjunct Faculty International | 11 |
| Professor of Practice | 4 |
| Distinguished Professor | 2 |


This distribution shows that the dataset is dominated by regular faculty, with additional contributions from adjunct and practice professors.

---

### 🔹 Research Specialization Trends

- **Total Unique Research Areas Identified:** 353  
- **Top 5 Research Areas:**
  - Machine Learning (6)
  - Information Retrieval (6)
  - Computer Vision (6)
  - Natural Language Processing (5)
  - Image Processing (5)

These trends indicate strong representation of modern computing and AI-driven research domains.

---

### 🔹 Data Quality Summary

- **Fully Detailed Profiles (Education + Email + Specialization):** 106  
- The dataset demonstrates strong completeness and is suitable for further analytics, semantic search, and NLP-based applications.

---

These insights confirm that the pipeline successfully produced a **diverse, information-rich, and analysis-ready dataset**.

---

## 🔹 [Faculty Recommender System](https://faculty-find.streamlit.app/)
A **Streamlit-based recommender application** has been built on top of the transformed data (`daiict_faculty_transformed.csv`). This system allows users to search for faculty members using natural language queries.
#### **Key Features:**
- **Hybrid Search Logic**:
  1.  **Exact Name Match**: Instantly finds faculty by name.
  2.  **Keyword Match**: Filters based on research interests (e.g., "Deep Learning", "VLSI").
  3.  **Semantic Search**: Uses **vector embeddings** to find conceptual matches even if exact keywords are missing (e.g., query "brain computer interface" matches "Human-Computer Interaction").
- **Vector Search Engine**: Powered by **FAISS** (Facebook AI Similarity Search) for high-performance similarity search.
- **Embeddings**: Uses **Sentence-BERT (`all-MiniLM-L6-v2`)** to generate 384-dimensional dense vectors for faculty profiles.
- **Interactive UI**: A modern dashboard built with **Streamlit**, featuring profile cards, dynamic filtering, and direct links to faculty profile pages.


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
python scraper/all_faculty_scraper.py
```
### 3️ Transform Data
```bash
python transform/faculty_transformed.py
```

### 4️ Load Data into Database
```bash
python load_to_sqlite.py
```

### 5️ Start API Server
```bash
uvicorn main:app --reload
```

### 6️ Start Recommender App
```bash
streamlit run recommender_app/streamlit.py
```

### 7️ Access Live Demo
[Faculty Finder App](https://faculty-find.streamlit.app/)

## 🚀 Future Enhancements

- **Automated Data Pipeline**: Integrate **Apache Airflow** or **Prefect** to schedule weekly scraping and updates.
- **LLM-Powered Chatbot**: Build a **RAG (Retrieval-Augmented Generation)** system to allow students to chat with the dataset (e.g., "Who works on NLP?").
- **Knowledge Graph**: Migrate to **Neo4j** to model complex relationships between faculty, research areas, and publications.
- **Cloud Deployment**: Containerize the full stack using **Docker Compose** and deploy on **AWS/GCP** for global access.
- **Research Collaboration Network**: Visualize co-authorship and research overlap using graph algorithms.

---

## 🎓 Learning Outcomes

- End-to-end data pipeline design
- Web scraping and data ingestion
- Data cleaning and transformation
- Schema design and relational storage
- API development using FastAPI
- **Vector Search & Embeddings**: Implementing semantic search using FAISS and Sentence Transformers.
- **Interactive Dashboards**: Building data-driven applications with **Streamlit**.
- **Containerization**: Using **Docker** for reproducible deployments.
