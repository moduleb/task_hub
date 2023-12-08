# pip install email-validator
import re

from pydantic import BaseModel, field_validator, EmailStr


def field_validator_username(func):
    def wrapper(cls, username):
        # Проверка длины имени
        if len(username) < 3 or len(username) > 16:
            raise ValueError('Username должен содержать от 3 до 16 символов')

        # Проверка на недопустимые символы (можно только англ. буквы в любом регистре, цифры и символы "-_"
        if not re.match(r'^[a-zA-Z0-9-_]+$', username):
            raise ValueError('Username содержит недопустимые символы')
        return func(cls, username)
    return wrapper


def field_validator_password(func):
    def wrapper(cls, password):
        # Проверка длины пароля
        if len(password) < 6 or len(password) > 20:
            raise ValueError('Password должен содержать от 6 до 20 символов')

        # Проверка на недопустимые символы (разрешены только спецсимволы, цифры и англ. буквы в любом регистре)
        if not re.match(r'^[a-zA-Z0-9!#$%&()*+-:<=>?@[\]^_{|}~]+$', password):
            raise ValueError('Password содержит недопустимые символы')

        # Проверка на обязательное содержание хотя бы одной буквы строчной, заглавной и цифры
        if not re.match(r'.*[a-z]', password) or \
                not re.match(r'.*[A-Z]', password) or \
                not re.match(r'.*\d', password):
            raise ValueError(
                "Password должен содержать буквы английского алфавита в нижнем и верхнем регистре "
                "и хотя бы одну цифру.")
        return func(cls, password)
    return wrapper

class UserRegDTO(BaseModel):
    username: str
    password: str
    email: EmailStr

    @field_validator('username')
    @field_validator_username
    def validate_username(cls, username):
        return username

    @field_validator('password')
    @field_validator_password
    def validate_password(cls, password):
        return password


class UserLoginDTO(BaseModel):
    username: str
    password: str

    @field_validator('username')
    @field_validator_username
    def validate_username(cls, username):
        return username

    @field_validator('password')
    @field_validator_password
    def validate_password(cls, password):
        return password


class UserUpdateDTO(BaseModel):
    password: str
    email: EmailStr

    @field_validator('password')
    @field_validator_password
    def validate_password(cls, password):
        return password


