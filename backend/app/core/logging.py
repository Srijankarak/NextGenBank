import os
import sys
from loguru import logger
from backend.app.core.config import settings

# 1. Remove Loguru's default handler so we can configure our own
logger.remove()

# 2. Directory where log files will be saved: backend/app/logs/
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 3. Standard banking log format
LOG_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
    "{level: <8} | "
    "{name}:{function}:{line} - "
    "{message}"
)

# 4. Sink 1: Live colored output in your terminal
logger.add(
    sink=sys.stderr,
    format=LOG_FORMAT,
    level="DEBUG" if settings.ENVIRONMENT == "local" else "INFO",
    colorize=True,
)

# 5. Sink 2: debug.log file (rotated at 10MB, retained 30 days, zipped)
logger.add(
    sink=os.path.join(LOG_DIR, "debug.log"),
    format=LOG_FORMAT,
    level="DEBUG" if settings.ENVIRONMENT == "local" else "INFO",
    filter=lambda record: record["level"].no <= logger.level("WARNING").no,
    rotation="10MB",
    retention="30 days",
    compression="zip",
)

# 6. Sink 3: error.log file (captures ERROR and CRITICAL with deep stack traces)
logger.add(
    sink=os.path.join(LOG_DIR, "error.log"),
    format=LOG_FORMAT,
    level="ERROR",
    rotation="10MB",
    retention="30 days",
    compression="zip",
    backtrace=True,
    diagnose=True,
)


def get_logger():
    """Return the configured singleton logger instance."""
    return logger
