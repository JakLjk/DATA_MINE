import logging 
from config import LoggingConf


if LoggingConf.LOG_FILE_PATH_NAME:
        handlers = [logging.FileHandler(LoggingConf.LOG_FILE_PATH_NAME),
                    logging.StreamHandler()]
else: 
    handlers = [logging.StreamHandler()]

logger = logging


logger.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s ||| [%(threadName)s] ",
    handlers=handlers)