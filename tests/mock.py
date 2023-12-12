"""
Создаем мок объекты для тестов
"""

from unittest.mock import MagicMock
from app.database import DB


class Mock:
    """
    Создает мок объекты и устанавливает их связь и возвращаемые значения
    mysql.connector.connect = db
    db.cursor = cursor
    """
    def __init__(self, mock_connect):
        self.mock_connect = mock_connect

        # создаем мок объекты
        self.mock_db = MagicMock()
        self.mock_cursor = MagicMock()

        # mysql.connector.connect = db
        self.mock_connect.return_value = self.mock_db

        # db.is_connected = True
        self.mock_db.is_connected.return_value = True

        # db.cursor = cursor
        self.mock_db.cursor.return_value = self.mock_cursor

        # создаемт объект класса DB
        self.db_class = DB()

        # Устанавливаем в False, чтобы класс инициализировался каждый раз при запуске
        DB.initialized = False
