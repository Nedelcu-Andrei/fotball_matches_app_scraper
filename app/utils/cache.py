import json
from pathlib import Path
from app.utils.helpers import TODAY
from app.utils.logger import logger as log
import sys


def get_cache_file() -> Path:
    """ Checks what PATH to use for the CACHE file """
    # RUNNING AS EXE
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        cache_dir = exe_dir / "cache"
        cache_dir.mkdir(exist_ok=True)
        return cache_dir / "cached_games_data.json"

    # RUNNING FROM SOURCE
    base_dir = Path(__file__).resolve().parent.parent      ## Get base_dir path(root/app..)
    return base_dir / "cache" / "cached_games_data.json"   ## Create path for the cached data


def get_raw_data_cache_file(name: str) -> Path:
    """ Checks what PATH to use for the CACHE file. Dev only. """
    # RUNNING FROM SOURCE
    base_dir = Path(__file__).resolve().parent.parent      ## Get base_dir path(root/app..)
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / "cache" / f"raw_{name}.json"


CACHE_FILE = get_cache_file()

def load_cache() -> tuple:
    """ Loads the cached games data """
    if not CACHE_FILE.exists():
        return None, None

    try:
        with CACHE_FILE.open() as f:
            cached_games = json.load(f)
        return cached_games.get("date"), cached_games.get("data")
    except:
        return None, None


def save_cache(data: str) -> None:
    """ Saves the cached games data + curr date """
    CACHE_FILE.parent.mkdir(exist_ok=True)

    cached = {
        "date": TODAY,
        "data": data
    }

    with open(CACHE_FILE, "w") as f:
        json.dump(cached, f)


def save_raw_data(data: str | dict, name: str = "data") -> None:
    """ Saves the raw data from the API call """
    cache_file_raw = get_raw_data_cache_file(name)
    cache_file_raw.parent.mkdir(parents=True, exist_ok=True)

    cached = {
        "date": TODAY,
        "data": data
    }

    # -------------------------------
    # TRY JSON SAVE FIRST
    # -------------------------------
    try:
        with open(cache_file_raw, "w", encoding="utf-8") as f:
            json.dump(cached, f, ensure_ascii=False, indent=4)
            return

    except (TypeError, ValueError) as err:
        # JSON encoding failed (likely unserializable structure)
        log.error(f"JSON save failed: {err}. Falling back to text format.")

    # -------------------------------
    # FALLBACK TO PLAIN TEXT
    # -------------------------------
    txt_file = cache_file_raw.with_suffix(".txt")
    try:
        with open(txt_file, "w") as f:
            f.write(str(data))
        log.info(f"Raw data saved as plain text: {txt_file.name}")

    except Exception as err:
        log.error(f"Failed to save raw data as text file: {err}")