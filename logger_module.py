'''src/traffic_monitor/logger.py

Logging setup for GitHub Traffic Monitor.
Configures console and rotating file handlers.
'''
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

LOG_FILE_NAME = 'traffic_monitor.log'
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB per file
LOG_BACKUP_COUNT = 3            # keep 3 backup files


def setup_logging(log_dir: str = None, level: str = 'INFO'):
    """
    Configure logging:
      - Console handler at level INFO
      - Rotating file handler at specified level
    """
    # Determine log directory
    if not log_dir:
        log_dir = os.getenv('LOG_DIR', os.getcwd())
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    log_file = log_path / LOG_FILE_NAME

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)

    # Rotating file handler
    fh = RotatingFileHandler(
        log_file, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT
    )
    fh.setLevel(getattr(logging, level.upper(), logging.INFO))
    fh_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)

    logger.info(f"Logging initialized. Writing logs to {log_file}")
