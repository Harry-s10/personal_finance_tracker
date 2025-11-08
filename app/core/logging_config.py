import json
import logging
import os
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler

from app.core.config import settings


def setup_logging():
    """Configure logging"""
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    log_path = os.path.join(settings.LOG_DIR, settings.LOG_FILE)

    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                "timestamp": datetime.now(UTC).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }
            if record.exc_info:
                log_entry["exception"] = self.formatException(record.exc_info)
            return json.dumps(log_entry)

    text_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    if settings.LOG_FORMAT == "json":
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(text_format, date_format)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = RotatingFileHandler(
        log_path, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        handlers=[console_handler, file_handler],
        force=True,
    )

    logger = logging.getLogger(settings.APP_NAME)
    logger.info(
        f"Logging initialized: (env={settings.ENVIRONMENT}, level={settings.LOG_LEVEL})"
    )
    return logger


logger = setup_logging()
