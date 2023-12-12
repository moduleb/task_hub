"""
Модуль установки соединения с базой данных
"""

from typing import Generator

import mysql
from fastapi import HTTPException
from mysql.connector import OperationalError

from app.config import config
from app.logger import db_log


class DB:
    """
    Класс для взаимодействия с базой данных
    """
    initialized = False

    def __init__(self):
        """
        Инициализирует класс DB и устанавливает соединение с базой данных,
        если оно еще не было инициализировано.
        """
        if not DB.initialized:
            db_log.debug('Class DB init process...')
            self.db = self.connect()
            DB.initialized = True

    def connect(self):
        """
        Устанавливает соединение с базой данных.

        Returns:
            db: Объект соединения с базой данных.

        Raises:
            HTTPException: Если не удалось установить соединение с базой данных.
        """
        try:
            db = mysql.connector.connect(
                host=config.db.host,
                user=config.db.user_name,
                password=config.db.password,
                database=config.db.db_name,
            )
            db_log.debug('DB created: %s', db)
            return db

        except Exception as e:
            db_log.critical('Не удалось установить соединение с базой данных: %s', e)
            raise HTTPException(status_code=500,
                                detail='Не удалось установить соединение с базой данных'
                                ) from e

    def is_connected(self):
        """
        Проверяет, активно ли соединение с базой данных.

        Returns:
            bool: True, если соединение активно, False - нет.
        """
        status = self.db.is_connected()
        db_log.debug('DB is connected: %s', status)
        return status

    def reconnect_(self, attempts):
        """
        Пере-подключается к базе данных.

        Args:
            attempts (int): Количество попыток переподключения.
        """
        self.db.reconnect(attempts=attempts)
        db_log.debug('DB reconnect...')

    def get_cursor(self) -> Generator:
        """
        Возвращает курсор базы данных.

        Yields:
            mysql.connector.cursor: Курсор базы данных.

        Raises:
            HTTPException:
            Нне удалось установить соединение с базой данных,даже после переподключения.
        """
        if not self.is_connected():
            self.reconnect_(attempts=3)

            if not self.is_connected():
                db_log.error(
                    'Не удалось установить соединение с базой данных, даже после переподключения')
                raise HTTPException(500, 'Не удалось установить соединение с базой данных')

        try:
            cursor = self.db.cursor()
            db_log.debug('Cursor received: %s', cursor)
            yield cursor

        except OperationalError as e:
            db_log.debug('Не удалось установить соединение с базой данных: %s', e)
            raise HTTPException(status_code=500,
                                detail='Не удалось установить соединение с базой данных'
                                ) from e

        finally:
            # Сохраняем изменения, закрываем курсор
            self.db.commit()
            db_log.debug('Database commit...')
            result = cursor.close()
            db_log.debug('Cursor closed: %s', result)
