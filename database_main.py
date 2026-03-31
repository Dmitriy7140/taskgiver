import sqlite3
from datetime import datetime, timedelta


class UserDB:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        with self._connect() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    tg_id INTEGER PRIMARY KEY,
                    last_task TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_links (
                    tg_id INTEGER,
                    link TEXT,
                    PRIMARY KEY (tg_id, link)
                )
            ''')

            conn.commit()

    def update_last_task(self, user_id: int):
        now = datetime.now().isoformat()

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO users(tg_id, last_task) VALUES (?, ?)",
                (user_id, now)
            )
            conn.commit()

    def get_user_links(self, user_id: int):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT link FROM user_links WHERE tg_id=?",
                (user_id,)
            )
            return [r[0] for r in cursor.fetchall()]

    def add_user_links(self, user_id: int, link: str):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO user_links(tg_id, link) VALUES (?, ?)",
                (user_id, link)
            )
            conn.commit()

    def can_do_task(self, user_id: int, min_interval_hours=24):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT last_task FROM users WHERE tg_id=?",
                (user_id,)
            )
            row = cursor.fetchone()

        if not row or not row[0]:
            return True

        last_task_time = datetime.fromisoformat(row[0])
        return datetime.now() - last_task_time >= timedelta(hours=min_interval_hours)