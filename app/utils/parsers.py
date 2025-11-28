from datetime import datetime
from typing import List
from app.utils.helpers import format_time, fractional_to_decimal
from app.utils.logger import logger as log
from app.data.models import Game, Odds
from app.utils.validators import validate_start_timestamp


# -----------------------------
# PARSERS
# -----------------------------
def parse_games(data: dict, important_teams: set[str]) -> List[Game] | None:
    """ Parses the important teams data from the API """
    try:
        games_today: List[Game] = []
        today_date = datetime.today().strftime("%Y-%m-%d")

        for event in data["events"]:
            home = event["homeTeam"]["name"]
            away = event["awayTeam"]["name"]

            if home in important_teams or away in important_teams:
                if validate_start_timestamp(event["startTimestamp"]):
                    start_time = format_time(event["startTimestamp"])

                    if start_time[0] != today_date:  # Filter the games from other days
                        continue

                    games_today.append(Game(
                        id = event["id"],
                        home = event["homeTeam"]["name"],
                        away = event["awayTeam"]["name"],
                        time = start_time,
                        tournament = event["tournament"]["name"],
                    ))

        return games_today

    except (TypeError, ValueError) as err:
        log.error(f"Error while parsing games: {err}")
        return None

    except Exception as err:
        log.error(f"Unexpected error while parsing games: {err}")
        return None


def parse_odds(odds_data: dict, games_data: List[Game]) -> List[Odds] | None:
    """ Parses the odds data from the API """
    try:
        parsed_odds: List[Odds] = []

        for game in games_data:
            game_id = str(game.id)

            try:
                choices = odds_data["odds"][game_id]["choices"]

                parsed_odds.append(
                    Odds(
                    game_id = game.id,
                    home_win = fractional_to_decimal(choices[0]["fractionalValue"]),
                    draw = fractional_to_decimal(choices[1]["fractionalValue"]),
                    away_win = fractional_to_decimal(choices[2]["fractionalValue"]),
                ))

            except KeyError:
                log.info(f"No odds found for game with id: {game_id}. Skipping...")
                continue

        return parsed_odds

    except (TypeError, ValueError) as err:
        log.error(f"Error while parsing odds: {err}")
        return None

    except Exception as err:
        log.error(f"Unexpected error while parsing odds: {err}")
        return None