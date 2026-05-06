import logging
import json
import sys
from src.config.constants import LOG_LEVEL, LOGGER_NAME

def get_logger(name: str = LOGGER_NAME) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    # Set log level from environment/config
    logger.setLevel(LOG_LEVEL.upper())
    return logger


def log_json(level, service, event, **kwargs):
    log_record = {
        "level": level.upper(),
        "service": service,
        "event": event,
        **kwargs
    }
    logger = get_logger(service)
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(json.dumps(log_record))
