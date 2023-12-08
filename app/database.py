import mysql
from fastapi import HTTPException
from mysql.connector import OperationalError

from app.config import config
from app.logger import log

error_msg = 'Database error'

class DB:
    def __init__(self):
        self.db = self.__connect()


    def __connect(self):
        try:
            db = mysql.connector.connect(
                host=config.db.HOST,
                user=config.db.USER_NAME,
                password=config.db.PASSWORD,
                database=config.db.DB_NAME,
            )
            log.debug(f'DB created: {db}')
            return db
        except Exception as e:
            log.error(f'{error_msg}: {e}')
            raise HTTPException(status_code=500, detail=error_msg)

    def __is_connected(self):
        status = self.db.is_connected()
        log.debug(f'DB is connected: {status}')
        return status

    def __reconnect(self, attempts):
        self.db.reconnect(attempts=attempts)
        log.debug(f'DB reconnect...')

    def get_cursor(self):
        if not self.__is_connected():
            self.__reconnect(attempts=3)
        if not self.__is_connected():
            raise Exception
        try:
            cursor = self.db.cursor()
            yield cursor
        except OperationalError as e:
            log.error(f"{error_msg}: {e}")
            raise HTTPException(status_code=500, detail=error_msg)
        except Exception as e:
            log.error(f"{error_msg}: {e}")
            raise HTTPException(status_code=500, detail=error_msg)
        finally:
            self.db.commit()
            cursor.close()

db = DB()