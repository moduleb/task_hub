from typing import Generator

import mysql
from fastapi import HTTPException
from mysql.connector import OperationalError

from app.config import config
from app.logger import db_log


class DB:
    initialized = False
    def __init__(self):
        if not DB.initialized:
            db_log.debug('Class DB init process...')
            self.db = self.connect()
            DB.initialized = True

    def connect(self):
        try:
            db = mysql.connector.connect(
                host=config.db.host,
                user=config.db.user_name,
                password=config.db.password,
                database=config.db.db_name,
            )
            db_log.debug('DB created: %s',db)
            return db

        except Exception as e:
            db_log.critical('Failed to connect to the database: %s', e)
            raise HTTPException(status_code=500, detail='Failed to connect to the database') from e

    def is_connected(self):
        status = self.db.is_connected()
        db_log.debug('DB is connected: %s', status)
        return status

    def reconnect_(self, attempts):
        self.db.reconnect(attempts=attempts)
        db_log.debug('DB reconnect...')

    def get_cursor(self) -> Generator:

        if not self.is_connected():
            self.reconnect_(attempts=3)

            if not self.is_connected():
                db_log.error('Failed to connect to the database after reconnecting')
                raise HTTPException(500, 'Failed to connect to the database')

        try:
            cursor = self.db.cursor()
            db_log.debug('Cursor received: %s', cursor)
            yield cursor

        except OperationalError as e:
            db_log.debug('Failed to connect to the database: %s', e)
            raise HTTPException(status_code=500, detail='Failed to connect to the database') from e

        finally:
            self.db.commit()
            db_log.debug('Database commit...')
            result = cursor.close()
            db_log.debug('Cursor closed: %s', result)
