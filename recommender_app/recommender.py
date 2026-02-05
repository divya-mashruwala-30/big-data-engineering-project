import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

# DATA_PATH = "daiict_faculty_transformed.csv"
# Get the absolute path to the data file relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "daiict_faculty_transformed.csv")

# Constants
SYNONYMS = {
    "nlp": "natural language processing",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "cv": "computer vision",
    "ds": "data science",
    "iot": "internet of things"
}

model = None
index = None


def load_resources():
    """
    Loads the dataframe, model, and FAISS index.
    Returns:
        tuple: (df, model, index)
    """
    df = pd.read_csv(DATA_PATH)
    df["combined_text"] = df["combined_text"].fillna("")
    df["name_lower"] = df["name"].str.lower()
    df["bio_lower"] = df["bio"].str.lower()
    df["education_lower"] = df["education"].str.lower()

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(df["combined_text"].tolist(), convert_to_numpy=True)
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    return df, model, index


def expand_query(query):
    q = query.lower().strip()
    return SYNONYMS.get(q, q)


def search_faculty(query, df, model, index):
    """
    Searches for faculty using the provided resources.
    Args:
        query (str): User query
        df (pd.DataFrame): Faculty data
        model (SentenceTransformer): Embedding model
        index (faiss.Index): FAISS index
    Returns:
        pd.DataFrame: Filtered results
    """
    query = expand_query(query)
    query_lower = query.lower()

    # 🔹 Case 1: Exact Name Match
    name_matches = df[df["name_lower"].str.contains(query_lower)]
    if len(name_matches) == 1:
        return name_matches

    # 🔹 Case 2: Keyword Filtering First (Broad Match)
    keyword_matches = df[
        df["combined_text"].str.lower().str.contains(query_lower)
    ]

    if len(keyword_matches) > 0:
        return keyword_matches

    # 🔹 Case 3: Semantic Search with Dynamic Threshold
    query_embedding = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, len(df))  # search all

    scores = scores[0]
    indices = indices[0]

    threshold = 0.35  # similarity threshold (tunable)

    filtered_indices = [indices[i] for i in range(len(scores)) if scores[i] > threshold]

    if len(filtered_indices) > 0:
        return df.iloc[filtered_indices]

    # 🔹 Case 4: Fallback — return top 5 semantic matches
    return df.iloc[indices[:5]]
