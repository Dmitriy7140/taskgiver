
import sqlite3

from datetime import datetime, timedelta

class UserDB:
    def __init__(self, db_path="database.db"):

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        # Таблица пользователей с временем последнего задания
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                last_task TIMESTAMP
            )
        ''')
        self.conn.commit()

        # Таблица использованных ссылок
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS used_links (
                link TEXT PRIMARY KEY
            )
        ''')
        self.conn.commit()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS used_reviews (                
                review TEXT PRIMARY KEY)
                ''')
        self.conn.commit()
    # ----------------------------
    # Обновить last_task на текущее время
    # ----------------------------
    def update_last_task(self, user_id: int):
        now = datetime.now().isoformat()
        self.cursor.execute(
            "INSERT OR REPLACE INTO users(tg_id, last_task) VALUES (?, ?)",
            (user_id, now)
        )
        self.conn.commit()

    # ----------------------------
    # Проверка, можно ли выдавать задание
    # ----------------------------
    def can_do_task(self, user_id: int, min_interval_hours=24):
        self.cursor.execute(
            "SELECT last_task FROM users WHERE tg_id=?",
            (user_id,)
        )
        row = self.cursor.fetchone()
        if not row or not row[0]:
            return True

        last_task_time = datetime.fromisoformat(row[0])
        return datetime.now() - last_task_time >= timedelta(hours=min_interval_hours)

    # ----------------------------
    # Выдать одну случайную ссылку, которой ещё нет в used_links
    # ----------------------------
    def add_used_link(self, used_link:str, user_id: int):
        # сохраняем в used_links
        self.cursor.execute(
            "INSERT OR IGNORE INTO used_links(link) VALUES (?)",
            (used_link,)
        )
        self.conn.commit()

        # обновляем last_task
        self.update_last_task(user_id)

        return
    def get_used_links(self) -> list:
        self.cursor.execute('''
        SELECT link FROM used_links''')
        rows = self.cursor.fetchall()
        return rows
    def add_used_review(self, review:str):
        self.cursor.execute('''
        INSERT OR IGNORE INTO used_reviews(review) VALUES (?)''', review)
        self.conn.commit()
        return
    def get_used_reviews(self) -> list:
        self.cursor.execute('''SELECT review FROM used_reviews''')
        rows = self.cursor.fetchall()
        return rows

