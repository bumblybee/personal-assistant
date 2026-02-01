import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "notes.db"


def get_db():
    """Get a database connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def run_query(query: str, params: tuple = ()):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
    finally:
        conn.commit()
        conn.close()


def init_db():
    run_query("""
      CREATE TABLE IF NOT EXISTS notes (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          content TEXT NOT NULL,
          tag TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    run_query("""
      CREATE TABLE IF NOT EXISTS reminders (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          content TEXT NOT NULL,
          remind_at TEXT DEFAULT NULL,
          done INTEGER DEFAULT 0,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    print(f"Database created at: {DB_PATH}")


def seed_sample_data():
    existing_notes = run_query("SELECT * FROM notes")
    if not existing_notes or len(existing_notes) == 0:
        sample_notes = [
            ("Research SQLite full-text search", "learning"),
            ("Call to reschedule PT", None),
        ]

        for content, tag in sample_notes:
            run_query("INSERT INTO notes (content, tag) VALUES (?, ?)", (content, tag))
        print(f"Added {len(sample_notes)} sample notes")


if __name__ == "__main__":
    init_db()
    seed_sample_data()
