"""SQLite persistence for BMI records (multi-user)."""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "bmi_records.db"


class BMIStore:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_schema()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_schema(self):
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS records (
                        id           INTEGER PRIMARY KEY AUTOINCREMENT,
                        user         TEXT    NOT NULL,
                        weight_kg    REAL    NOT NULL,
                        height_m     REAL    NOT NULL,
                        bmi          REAL    NOT NULL,
                        category     TEXT    NOT NULL,
                        recorded_at  TEXT    NOT NULL
                    )
                    """
                )
        except sqlite3.Error as e:
            raise RuntimeError(f"Database init failed: {e}")

    def add_record(self, user, weight_kg, height_m, bmi, category):
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO records
                    (user, weight_kg, height_m, bmi, category, recorded_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (user, weight_kg, height_m, bmi, category,
                     datetime.now().isoformat(timespec="seconds")),
                )
        except sqlite3.Error as e:
            raise RuntimeError(f"Could not save record: {e}")

    def get_history(self, user: str):
        """Return list of (recorded_at, bmi) tuples, oldest first."""
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT recorded_at, bmi FROM records
                    WHERE user = ?
                    ORDER BY recorded_at ASC
                    """,
                    (user,),
                ).fetchall()
            return rows
        except sqlite3.Error as e:
            raise RuntimeError(f"Could not load history: {e}")

    def list_users(self):
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    "SELECT DISTINCT user FROM records ORDER BY user"
                ).fetchall()
            return [r[0] for r in rows]
        except sqlite3.Error as e:
            raise RuntimeError(f"Could not list users: {e}")