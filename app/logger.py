import logging

from app.config import config

logging.basicConfig(level=logging.DEBUG,
                    format='%(filename)s - %(levelname)s - %(message)s')

log = logging.getLogger("main")

if config.log.LOG_LEVEL == 'DEBUG':
    log.setLevel(logging.DEBUG)
elif config.log.LOG_LEVEL == 'ERROR':
    log.setLevel(logging.ERROR)