"""
Модуль для работы с базой данных
"""
import sqlite3


class AttendanceDatabase:
    """
    Класс реализует методы для работы с локальной базой данных
    """
    def __init__(self, dp_path: str = "data/attendance.db") -> None:
        """
        Инициализация локальной базы данных, подключение, создание в случае отсутствия
        
        :param dp_path: путь до файла с БД `(default = 'data/attendance.db')`
        """
        self.conn = sqlite3.connect(dp_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()
        
    def _create_table(self) -> None:
        """
        Метод создает локальную БД с полями:
        - `id`: integer primary key autoincrement
        - `user_id`: integer,
        - `username`: text,
        - `timestamp`: text,
        - `synced`: integer default 0
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                timestamp TEXT,
                synced INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()
        
    def add_attendance(
        self, 
        user_id: int, 
        username: str, 
        timestamp: str
    ) -> None:
        """
        Метод добавляет отметку о посещении в локальную БД
        
        :param user_id: ID VK пользователя
        :param username: имя пользователя
        :param timestamp: временная метка записи
        """
        self.cursor.execute("INSERT INTO attendance (user_id, username, timestamp) VALUES (?, ?, ?)",
                            (user_id, username, timestamp))
        self.conn.commit()
        
    def get_unsynced_records(self) -> list:
        """
        Метод возвращает записи из локальной БД, несинхронизированные с удаленной БД
        
        :return unsynced_data: несинхронизированные записи локальной БД
        """
        self.cursor.execute("SELECT * FROM attendance WHERE synced = 0")
        return self.cursor.fetchall()
    
    def mark_as_synced(self, record_id: int) -> None:
        """
        Метод отмечает запись в локальной БД как синхронизированную
        
        :param record_id: ID записи в локальной БД
        """
        self.cursor.execute("UPDATE attendance SET synced = 1 WHERE id = ?", (record_id,))
        self.conn.commit()
        
    def remove_user(self, user_id: int) -> None:
        """
        Метод удаляет запись из локальной БД по ID VK пользователя
        
        :param user_id: ID VK пользователя
        """
        self.cursor.execute("DELETE FROM attendance WHERE user_id = ?", (user_id,))
        self.conn.commit()
