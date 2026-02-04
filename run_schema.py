import sqlite3

DB_PATH = "Assignment1/db/faculty_finder.db"
SCHEMA_PATH = "Assignment1/db/schema.sql"

conn = sqlite3.connect(DB_PATH)

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema_sql = f.read()

conn.executescript(schema_sql)
conn.commit()
conn.close()

print("Schema created successfully")
