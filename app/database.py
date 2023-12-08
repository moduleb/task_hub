import mysql
from fastapi import HTTPException
from mysql.connector import OperationalError

from app.config import config
from app.logger import log


try:
    db = mysql.connector.connect(
        host=config.db.HOST,
        user=config.db.USER_NAME,
        password=config.db.PASSWORD,
        database=config.db.DB_NAME,
    )
except Exception as e:
    log.error(f'DB connection error {e}')


def get_cursor():
    try:
        status = db.is_connected()
        log.debug(f'MySQL is connected: {status}')
        if not status:
            db.reconnect()
            log.debug(f'MySQL reconnected...\n'
                      f'MySQL is connected: {db.is_connected()}')
        cursor = db.cursor()
        yield cursor
    # except OperationalError as e:
    #     log.error(f"Ошибка подключения к базе данных: {e}")
    #     raise HTTPException(status_code=500, detail="Ошибка базы данных")
    # except Exception as e:
    #     log.error(f"Ошибка подключения к базе данных: {e}")
    #     raise HTTPException(status_code=500, detail="Ошибка базы данных")
    finally:
        db.commit()
        cursor.close()
