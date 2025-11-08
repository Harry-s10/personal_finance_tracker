import logging
from logging.config import dictConfig

from app.core.config import Environment, settings


def setup_logging():
    "Configure logging based on the environment"

    if settings.ENVIRONMENT == Environment.LOCAL:
        log_format = "%(asctime)s | %(name)s : %(levelname)s | %(message)s"
    else:
        # JSON like simplified format (structure for container)
        log_format = '{"level": "%(levelname)s", "time": "%(asctime)s", "name": "%(name)s", "msg": "%(message)s"}'

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_logger": False,
        "formatter": {
            "default": {"format": log_format, "datefmt": "%Y-%m-%d %H:%M:%S"}
        },
        "handlers": {"class": "logging.StreamHandler", "formatter": "default"},
        "root": {"handlers": ["console"], "level": settings.LOG_LEVEL.value},
    }
    dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(settings.APP_NAME)
    logger.info(
        f"Logging intialied (env={settings.ENVIRONMENT.value}, level={settings.LOG_LEVEL.value})"
    )
    return logger
