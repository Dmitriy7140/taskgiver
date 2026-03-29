
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

        # Таблица выданных ссылок
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_links (
                    tg_id INTEGER,
                    link TEXT,
                    PRIMARY KEY (tg_id, link)
                )
            ''')
        self.conn.commit()


    # ----------------------------
    # Метод 1: обновить last_task на текущее время
    # ----------------------------
    def update_last_task(self, user_id: int):
        now = datetime.now().isoformat()
        self.cursor.execute(
            "INSERT OR REPLACE INTO users(tg_id, last_task) VALUES (?, ?)",
            (user_id, now)
        )
        self.conn.commit()

    # ----------------------------
    # Метод 2: получить ссылки, которые уже выдавались пользователю
    # ----------------------------
    def get_user_links(self, user_id: int):
        self.cursor.execute(
            "SELECT link FROM user_links WHERE tg_id=?",
            (user_id,)
        )
        return [r[0] for r in self.cursor.fetchall()]

    # ----------------------------
    # Метод 3: добавить ссылки, выданные пользователю
    # ----------------------------
    def add_user_links(self, user_id: int, link: str):

        self.cursor.execute(
            "INSERT OR IGNORE INTO user_links(tg_id, link) VALUES (?, ?)",
            (user_id, link)
        )
        self.conn.commit()

    # ----------------------------
    # Метод 4: проверить, можно ли выдавать задание
    # Возвращает True если прошло >=1 часа, False иначе
    # ----------------------------
    def can_do_task(self, user_id: int, min_interval_hours=24):
        self.cursor.execute(
            "SELECT last_task FROM users WHERE tg_id=?",
            (user_id,)
        )
        row = self.cursor.fetchone()
        if not row or not row[0]:
            return True  # пользователь не найден или last_task пустой → можно дать

        last_task_time = datetime.fromisoformat(row[0])
        if datetime.now() - last_task_time >= timedelta(hours=min_interval_hours):
            return True
        else:
            return False