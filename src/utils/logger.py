import logging
import json
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

def log_json(level, service, event, **kwargs):
    log_record = {
        "level": level.upper(),
        "service": service,
        "event": event,
        **kwargs
    }
    logger = logging.getLogger(service)
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(json.dumps(log_record))
