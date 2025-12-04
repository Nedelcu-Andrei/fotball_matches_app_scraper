from datetime import datetime
from typing import List, Any
import curl_cffi
from curl_cffi import requests
from app.data.models import Game, Odds
from app.utils.helpers import USER_AGENT, GOT_ERROR_MSG
from app.utils.helpers import format_matches_data, get_status_code_err
from app.utils.cache import load_cache, save_cache, save_raw_data, get_mock
from app.utils.logger import logger as log
from app.utils.parsers import parse_games, parse_odds


########################################## API CLIENT CALL ##########################################
########################################## "::" = Otherwise ##########################################
class ApiClient:
    """ Calls the API ENDPOINT for all the Leagues and Competitions """
    def __init__(self, important_games, use_mock: bool = False) -> None:
        self.use_mock = use_mock
        self.headers = {
            'User-Agent': USER_AGENT,
        }
        self.today = datetime.today().strftime("%Y-%m-%d")
        self.important_games = important_games

        log.info("ApiClient initialized.")

    # -----------------------------
    # INTERNAL NETWORK HELPER
    # -----------------------------
    def _get(self, url: str) -> dict[str, Any] | None:
        """Perform a GET request with logging and error handling."""
        try:
            res = requests.get(url, headers=self.headers, impersonate="chrome120")

            if res.status_code != 200:
                status_code = get_status_code_err(res.status_code)
                log.error(f"GET {url} request failed. Got: {status_code}")
                return None

            try:
                return res.json()
            except ValueError as err:
                log.error(f"Failed to decode JSON from {url}: {err}")
                return res.text

        except curl_cffi.exceptions.CurlError as err:
            log.error(f"Network error while requests {url}: {err}")
            return None

        except Exception as err:
            log.error(f"Unexpected error in GET {url}: {err}")
            return None

    # -----------------------------
    # PUBLIC API CALLS
    # -----------------------------
    def fetch_fixtures_data(self, url: str) -> dict | None:
        """ Fetches the fixtures data from the given API Endpoint(url) """
        if self.use_mock:
            log.info(f"Using MOCK fixtures data...")
            return get_mock("games")

        raw_fixtures_data = self._get(url)
        save_raw_data(raw_fixtures_data, name="games")

        return raw_fixtures_data


    def fetch_odds_data(self, url: str) -> dict | None:
        """ Fetches the odds data from the given API Endpoint(url) """
        if self.use_mock:
            log.info(f"Using MOCK odds data...")
            return get_mock("odds")

        raw_odds_data = self._get(url)
        save_raw_data(raw_odds_data, name="odds")

        return raw_odds_data


    # -----------------------------
    # MAIN ENTRY POINT
    # -----------------------------
    def get_matches(self, games_url: str, odds_url: str) -> str | None:
        """ Fetch the games data from the CACHE if there's any :: Gather and format new data """
        if not self.use_mock:
            cached_data = self.check_cache()
            if cached_data:
                    log.info(f"Returning games from CACHE...")
                    return cached_data

        log.info("Fetching and parsing fixtures...")
        parsed_games = self._fetch_and_parse_games(games_url)

        log.info("Fetching and parsing odds...")
        parsed_odds = self._fetch_and_parse_odds(odds_url, parsed_games)

        log.info("Formatting matches and odds data...")
        formatted_matches = format_matches_data(parsed_games, parsed_odds)

        if not formatted_matches:
            log.info(f"No important games found for today - {self.today} -.")

        # Save data to CACHE
        save_cache(formatted_matches)

        return formatted_matches

    # -----------------------------
    # PRIVATE HELPER METHODS
    # -----------------------------
    def _fetch_and_parse_games(self, url: str) -> List[Game] | None:
        games = self.fetch_fixtures_data(url)
        return parse_games(games, self.important_games)


    def _fetch_and_parse_odds(self, url: str, parsed_games: List[Game]) -> List[Odds] | None:
        odds = self.fetch_odds_data(url)
        return parse_odds(odds, parsed_games)

    # -----------------------------
    # CACHE CHECKER
    # -----------------------------
    def check_cache(self) -> str | None:
        """ Checks for cached data """
        cached_date, cached_data = load_cache()

        if cached_date == self.today:  ## If cached data matches today date, reuse it
            if not cached_data: # If cache exists but there are no games
                log.info(f"No important games found in CACHE for today - {self.today} -.")
            elif cached_data == GOT_ERROR_MSG and not self.use_mock:
                log.info(f"Errors found in CACHE, fetching new data...")
                return None    # Resume to obtaining and parsing data
            return cached_data

        log.info(f"No data for today - {self.today} - found in CACHE. Fetching data from API...")
        return None