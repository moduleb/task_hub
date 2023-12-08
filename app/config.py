# pip install python-dotenv
import os
from dataclasses import dataclass, field


@dataclass
class LoggerConfig:
    LOG_LEVEL: str = 'DEBUG'


@dataclass
class DatabaseConfig:
    HOST: str = "localhost"
    USER_NAME: str = "user"
    PASSWORD: str = "password"
    DB_NAME: str = "task_hub"


@dataclass
class BaseConfig:
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    log: LoggerConfig = field(default_factory=LoggerConfig)
    config_type: str = 'dev'


@dataclass
class ProdConfig(BaseConfig):
    db: DatabaseConfig = field(default_factory=lambda: DatabaseConfig(
        HOST="mysql",
        DB_NAME="internet_lab"))
    log: LoggerConfig = field(default_factory=lambda: LoggerConfig(
        LOG_LEVEL='DEBUG'))
    config_type: str = 'prod'


if os.environ.get("FASTAPI_ENV") == "production":
    config = ProdConfig()
else:
    config = BaseConfig()
