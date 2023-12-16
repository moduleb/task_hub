"""Файл настроек приложения"""
import os
from dataclasses import dataclass, field


@dataclass
class LoggerConfig:
    """Конфигурация логгера"""
    log_level: str = 'DEBUG'
    db_log_level: str = 'DEBUG'


@dataclass
class DatabaseConfig:
    """Конфигурация базы данных"""
    host: str = "localhost"
    user_name: str = "user"
    password: str = "password"
    db_name: str = "task_hub"


@dataclass
class BaseConfig:
    """Базовая конфигурация"""
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    log: LoggerConfig = field(default_factory=LoggerConfig)
    config_type: str = 'dev'


@dataclass
class ProdConfig(BaseConfig):
    """Продакшн конфигурация"""
    db: DatabaseConfig = field(default_factory=lambda: DatabaseConfig(
        host="mysql",
        db_name="task_hub"))
    log: LoggerConfig = field(default_factory=lambda: LoggerConfig(
        log_level='ERROR',
        db_log_level='ERROR'))
    config_type: str = 'prod'


config: BaseConfig
if os.environ.get("FASTAPI_ENV") == "production":
    config = ProdConfig()
else:
    config = BaseConfig()
