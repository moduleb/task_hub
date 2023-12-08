from typing import List

from fastapi import HTTPException

from app.logger import log
from app.redis_ import r

REDIS_ERROR_MSG = "Redis error"


class RedisDAO:
    """
    Класс для работы с хранилищем Redis
    """
    @staticmethod
    def add_token(username: str, token: str) -> None:
        """
        Добавление токена в список деактивированных токенов пользователя
        """
        try:
            result = r.rpush(username, token)
            log.debug(f"Токен добавлен в список активных, index: {result}")
        except Exception as e:
            log.error(f"{REDIS_ERROR_MSG} {e}")
            raise HTTPException(status_code=500, detail=REDIS_ERROR_MSG)

    @staticmethod
    def check_token(username: str, token: str) -> bool:
        """
        Проверка наличия токена в списке деактивированных токенов пользователя
        """
        try:
            # получаем список всех токенов, хранящихся с ключем username
            # 0 - индекс начала поиска (с самого начала)
            # -1 - индекс конца поиска (до самого конца)
            tokens: List[bytes] = r.lrange(username, 0, -1)

            # Redis сохраняет токены в байтах, поэтому преобразуем в байты входящий токен
            result = token.encode("utf-8") in tokens

            log.debug(f"Токен в списке активных: {result}")
            return result
        except Exception as e:
            log.error(f"{REDIS_ERROR_MSG} {e}")
            raise HTTPException(status_code=500, detail=REDIS_ERROR_MSG)


    @staticmethod
    def delete_token(username: str, token: str) -> None:
        """
        Удаление токена из списка активных токенов пользователя
        """
        try:
            # получаем список токенов
            tokens = r.lrange(username, 0, -1)

            # получаем индекс токена в списке
            index = tokens.index(token.encode('UTF-8'))

            # Заменяем значение по индексу с токена на __DELETED__
            r.lset(username, index, "__DELETED__")
            # Удаляем все записи со значением __DELETED__
            result = r.lrem(username, 0, "__DELETED__")

            log.debug(f"Удаление токена из списка активных: {result}")


        except ValueError as e:
            log.debug(f"Токена уже удален: {e}")
        except Exception as e:
            log.error(f"{REDIS_ERROR_MSG} {e}")
            raise HTTPException(status_code=500, detail=REDIS_ERROR_MSG)



    @staticmethod
    def delete_all_tokens(username: str) -> None:
        """
        Удаление всех токенов пользователя
        """
        try:
            result = r.delete(username)
            log.debug(f"Удаление списка токенов в Redis: {result}")
        except Exception as e:
            log.error(f"{REDIS_ERROR_MSG} {e}")
            raise HTTPException(status_code=500, detail=REDIS_ERROR_MSG)

    @staticmethod
    def get_amount_of_tokens(username: str) -> int:

        """
        Узнаем количество активных токенов пользователя
        """
        try:
            # получаем список токенов
            tokens = r.lrange(username, 0, -1)
            amount_of_tokens = len(tokens)
            log.debug(f"Количество активных токенов {username}: {amount_of_tokens}")
            return amount_of_tokens

        except Exception as e:
            log.error(f"{REDIS_ERROR_MSG} {e}")
            raise HTTPException(status_code=500, detail=REDIS_ERROR_MSG)