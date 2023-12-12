"""
Создаем и настраиваем логгеры
"""

import logging

from app.config import config

# Устанавливаем настройки обработчика по умолчанию
logging.basicConfig(format='%(filename)s - %(levelname)s - %(message)s')

# Создаем логгер и устанавливаем уровень
db_log = logging.getLogger('db')
db_log.setLevel(level=getattr(logging, config.log.db_log_level))

log = logging.getLogger('main')
log.setLevel(level=getattr(logging, config.log.log_level))

# Фиксируем форматирование
# formatter = logging.Formatter('%(filename)s - %(levelname)s - %(message)s')
# Создаем обработчик вывода в консоль
# console_handler = logging.StreamHandler()
# Добавляем к нему форматирование
# console_handler.setFormatter(formatter)
# Добавляем обработчик к логгеру
# db_log.addHandler(console_handler)
