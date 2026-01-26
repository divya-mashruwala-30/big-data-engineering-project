from fastapi import FastAPI, HTTPException
import sqlite3
import json
import os

app = FastAPI(title="Faculty Finder API")

# DATABASE CONFIG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "faculty_finder.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # return dict-like rows
    return conn


# 1 GET ALL FACULTY
@app.get("/getfaculty")
def get_all_faculty():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM faculty;")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="No faculty found")

    result = []
    for row in rows:
        faculty = dict(row)
        faculty["specialization_list"] = json.loads(faculty["specialization_list"])
        faculty["research_tags"] = json.loads(faculty["research_tags"])
        result.append(faculty)

    return result


# 2 GET FACULTY BY ID

@app.get("/faculty/{faculty_id}")
def get_faculty_by_id(faculty_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM faculty WHERE faculty_id = ?;",
        (faculty_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Faculty not found")

    faculty = dict(row)
    faculty["specialization_list"] = json.loads(faculty["specialization_list"])
    faculty["research_tags"] = json.loads(faculty["research_tags"])

    return faculty


# 3 GET FACULTY BY SPECIALIZATION LIST

@app.get("/specialization/{keyword}")
def get_faculty_by_specialization(keyword: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT *
    FROM faculty
    WHERE LOWER(specialization_list) LIKE ?
    """

    cursor.execute(query, (f"%{keyword.lower()}%",))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No faculty found with specialization containing '{keyword}'"
        )

    result = []
    for row in rows:
        faculty = dict(row)
        faculty["specialization_list"] = json.loads(faculty["specialization_list"])
        faculty["research_tags"] = json.loads(faculty["research_tags"])
        result.append(faculty)

    return result
