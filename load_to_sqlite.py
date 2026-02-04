import pandas as pd
import sqlite3
import json
import os

DB_PATH = "Assignment1/db/faculty_finder.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "daiict_faculty_transformed.csv")

df = pd.read_csv(CSV_PATH)

# Convert lists to strings
df["specialization_list"] = df["specialization_list"].apply(json.dumps)
df["research_tags"] = df["research_tags"].apply(json.dumps)

# Connect to sqlite
conn = sqlite3.connect(DB_PATH)

# Load data
df.to_sql(
    "faculty",
    conn,
    if_exists="replace", 
    index=False
)

conn.close()

print("Data loaded into SQLite successfully")
print(f"Rows inserted: {len(df)}")
