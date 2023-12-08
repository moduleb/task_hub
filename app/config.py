# pip install python-dotenv
import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


# загружаем файл .env в переменные окружения
load_dotenv()


@dataclass
class LoggerConfig:
    LOG_LEVEL: str = 'DEBUG'


@dataclass
class RedisConfig:
    HOST: str = 'localhost'
    PORT: int = 6379


@dataclass
class DatabaseConfig:
    HOST: str = "localhost"
    USER_NAME: str = "user"
    PASSWORD: str = "password"
    DB_NAME: str = "test_legprom"


@dataclass
class TokenConfig:
    SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    EXPIRATION_TIME_MINUTES: int = 60


@dataclass
class PasswordHashConfig:
    SALT: bytes = os.getenv("PWD_SALT")
    ITERATIONS: int = int(os.getenv("PWD_ITERATIONS"))
    ALGORITHM: str = os.getenv("PWD_ALGORITHM")


@dataclass
class BaseConfig:
    password: PasswordHashConfig = field(default_factory=PasswordHashConfig)
    token: TokenConfig = field(default_factory=TokenConfig)
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    log: LoggerConfig = field(default_factory=LoggerConfig)
    config_type: str = 'dev'


@dataclass
class ProdConfig(BaseConfig):
    db: DatabaseConfig = field(default_factory=lambda: DatabaseConfig(
        HOST="mysql",
        DB_NAME="internet_lab"))
    redis: RedisConfig = field(default_factory=lambda: RedisConfig(
        HOST="redis"))
    log: LoggerConfig = field(default_factory=lambda: LoggerConfig(
        LOG_LEVEL='DEBUG'))
    config_type: str = 'prod'


if os.environ.get("FASTAPI_ENV") == "production":
    config = ProdConfig()
else:
    config = BaseConfig()
