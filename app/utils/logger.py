import logging
from pathlib import Path
import sys
from datetime import datetime


def get_log_file() -> Path:
    """Chooses where to store the log file"""
    log_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # EXE mode
    if getattr(sys, "frozen", False):
        base =  Path(sys.executable).resolve().parent / "cache"
    else:
        # Source code mode
        base = Path(__file__).resolve().parent.parent / "cache"

    # Make sure the directory EXISTS
    base.mkdir(parents=True, exist_ok=True)

    # Source code mode
    ######################### Logging INFO in root/app/cache... #########################
    return base / f"app_logger_info - {log_timestamp}.log"


LOG_FILE = get_log_file()

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
)

logger = logging.getLogger(__name__)
