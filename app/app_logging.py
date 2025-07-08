from loguru import logger as app_logger
import sys
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "lms_backend.log")

app_logger.remove()
app_logger.add(sys.stdout, level=LOG_LEVEL, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
app_logger.add(LOG_FILE, level=LOG_LEVEL, rotation="10 MB", retention="10 days", compression="zip") 