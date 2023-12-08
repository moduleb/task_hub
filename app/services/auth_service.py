import base64

import hashlib
import random
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from app.config import config
from app.dto.redis_dao import RedisDAO
from app.logger import log

api_key_header = APIKeyHeader(name='Authorization')


def _decode_token(token: str) -> dict:
    try:
        data = jwt.decode(token, config.token.SECRET, algorithms=[config.token.ALGORITHM])
        return data

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Срок действия токена истек")
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Недействительная подпись токена")
    except jwt.DecodeError:
        log.debug(f'Ошибка декодирования токена:')
        raise HTTPException(status_code=401, detail="Ошибка декодирования токена")

class AuthService:

    @staticmethod
    async def hash_pass(password: str) -> str:
        """
        Хеширует пароль и возвращает его в виде строки.
        """
        try:
            hash_digest = hashlib.pbkdf2_hmac(
                hash_name=config.password.ALGORITHM,
                password=password.encode('utf-8'),
                salt=config.password.SALT.encode('utf-8'),
                iterations=config.password.ITERATIONS
            )
            hash_pass = base64.b64encode(hash_digest).decode('utf-8')
            return hash_pass

        except Exception as e:
            log.error(f'Ошибка хеширования пароля: {e}')
            raise HTTPException(500, detail="Ошибка хеширования пароля")


    @staticmethod
    async def create_access_token(username: str) -> str:
        """
        Генерирует токен доступа
        """

        # Устанавливаем время жизни токена и записываем в data
        minutes = config.token.EXPIRATION_TIME_MINUTES
        expire_time= datetime.utcnow() + timedelta(minutes=minutes)


        payload = {'username': username,
                   'exp': expire_time,
                   'random_number': random.randint(10000, 99999)}
        token = jwt.encode(payload, config.token.SECRET, algorithm=config.token.ALGORITHM)

        # Сохраняем токен в список активных
        RedisDAO.add_token(username, token)

        return token

    @staticmethod
    def verify_token(token: str = Security(api_key_header)) -> str:
        """
        Декодирует токен и проверяет его наличие
        в списке неактивных токенов пользователя в Redis
        """

        data = _decode_token(token)
        username = data.get("username")

        # Проверяем наличие токена в списке активных
        if not RedisDAO.check_token(username, token):
            raise HTTPException(status_code=401, detail="Токен недействителен")

        return username


    @staticmethod
    def logout(token: str = Security(api_key_header)):
        """
        Декодирует токен и добавляет его в список неактивных токенов пользователя в Redis
        """
        data = _decode_token(token)
        username = data.get("username")

        if username is None:
            raise HTTPException(status_code=401, detail="Неверные данные для аутентификации")

        # Удаляем токен из списка активных
        RedisDAO.delete_token(username, token)

        # Возвращаем username
        return username

    @staticmethod
    async def delete(username):
        RedisDAO.delete_all_tokens(username)


