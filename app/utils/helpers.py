from datetime import datetime, timedelta, timezone
from typing import List

import ipdb
from dotenv import load_dotenv
from requests.models import REDIRECT_STATI

from app.data.models import Game, Odds
from app.utils.logger import logger as log
import os

############## LOAD ENV VARIABLES ##############
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

################################### UTILS FOR THE API CLIENT ###################################
TODAY = datetime.today().strftime("%Y-%m-%d")
API_SPORTS = f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{TODAY}"
API_SPORTS_ODDS = f"https://www.sofascore.com/api/v1/sport/football/odds/1/{TODAY}"
# API_SPORTS_ODDS_EVENT = f"https://www.sofascore.com/api/v1/event/{EVENT-ID}/odds/1/all" ## the id from the api-sports
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
TELEGRAM_BOT_API_INFO=f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates" ######## Get info on your bot (CHAT ID, etc...)
GOT_ERROR_MSG = "Errors while gathering matches data. Check log file!"

##### HTTP STATUS CODES #####
CLIENT_ERRORS = [400, 401, 403, 404, 405, 408, 409, 429]
SERVER_ERRORS = [500, 501, 502, 503, 504]
REDIRECT_STATUS_CODES = [301, 302, 304]

################################### UTILS FOR THE API CLIENT ###################################

# HELPERS FOR CONVERSIONS/STRING MANIPULATION
def format_time(start_time: int) -> List[str]:
    """ Formats timestamps to actual date and hour:min of the game """
    tz = timezone(timedelta(hours=2))
    dt = datetime.fromtimestamp(start_time, tz)
    date = dt.date().isoformat()
    hour_minute = dt.strftime("%H:%M")

    return [date, hour_minute]


def fractional_to_decimal(frac: str) -> float:
    """ Converts fractional odds value to decimal """
    num, den = frac.split("/")
    return round(float(num) / float(den) + 1, 2)


def get_status_code_err(status_code: int) -> str:
    """ Return error message for the specific request status code """
    if status_code in CLIENT_ERRORS:
        return f"{status_code} Client Error while requesting. Please check!"
    elif status_code in SERVER_ERRORS:
        return f"{status_code} Server Error while requesting. Please check!"
    elif status_code in REDIRECT_STATUS_CODES:
        return f"{status_code} Redirect Status Code  while requesting. Please check!"

    return f"{status_code} Error while requesting. Please check!"


def format_matches_data(matches: List[Game], odds: List[Odds]) -> str | None:
    """ Adds the odds to the matches data then converts them into a string """
    try:
        lines = []
        odds_lookup = {item.game_id: item for item in odds}   # ID as Key for each set of odds to interrogate easily

        for match in matches:
            try:
                game_odds = odds_lookup.get(match.id, None)
                match.odds = game_odds
                lines.append(f"{match.home} vs {match.away} at {match.time[1]} in {match.tournament}. "
                             f"Cote: 1: {match.odds.home_win} / X: {match.odds.draw} / 2: {match.odds.away_win}")
            except TypeError:
                log.info(f"No odds for the game: {match.home} vs {match.away}. Saving without odds data.")
                # Append match without odds.
                lines.append(f"{match.home} vs {match.away} at {match.time[1]} in {match.tournament}.")

        return "\n".join(lines)

    except TypeError as err:
        log.error(f"TypeError in format_matches_data: {err}")
        return GOT_ERROR_MSG


