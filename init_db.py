import sqlite3
from pathlib import Path

DB = Path("students.db")
if DB.exists():
    print("students.db already exists.")
else:
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)
    cur.executemany("INSERT INTO students (id, name, score) VALUES (?, ?, ?)", [
        ("20230001", "김철수", 85),
        ("20230002", "이영희", 92),
        ("20230003", "박민수", 76),
    ])
    conn.commit()
    conn.close()
    print("students.db created with sample data.")
