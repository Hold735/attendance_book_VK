"""
Модуль для синхронизации локальной базы данных с удаленной базой данных Google Sheets
"""
import gspread
from google.oauth2.service_account import Credentials

from database import AttendanceDatabase
from config.config import GOOGLE_CREDENTIALS_PATH, GOOGLE_SHEET_NAME


class GoogleSync:
    """
    Класс реализует методы для работы с удаленной базой данных Google Sheets  
    """
    def __init__(
        self, 
        db: AttendanceDatabase
    ):
        """
        Инициализация удаленной базы данных.
        Авторизация, подключение, подготовка листов.
        
        :param db: объект локальной БД
        """
        
        creds = Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_PATH, 
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets", 
                "https://www.googleapis.com/auth/drive"
            ]
        )
        client = gspread.authorize(creds)
        self.spreadsheet = client.open(GOOGLE_SHEET_NAME)
        self.sheets = self.spreadsheet.sheet1
        self.db = db
        
    def sync_data(self):
        """
        Метод синхронизирует удаленную БД с локальной БД.
        Метод отправляет несинхронизованные данные в Google Sheets 
        из локальной БД и производит маркировку синхронизации.
        """
        unsynced = self.db.get_unsynced_records()
        for record in unsynced:
            self.sheets.append_row(record[1:])
            self.db.mark_as_synced(record[0])
