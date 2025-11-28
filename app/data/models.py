from dataclasses import dataclass
from datetime import datetime
from typing import List
from app.utils.logger import logger as log


@dataclass
class Odds:
    """ Odds Dataclass with post_init method for core validations."""
    game_id: int
    home_win: float
    draw: float
    away_win: float

    def __post_init__(self):
        if not isinstance(self.game_id, int):
            try:
                self.game_id = int(self.game_id)
            except (ValueError, TypeError):
                log.error(f"Invalid game_id, must be an integer/Failed to convert. Got {self.game_id!r}")
                raise TypeError(f"Game ID must be an integer/Failed to convert. Got {self.game_id!r}")

        for val, name in zip(
                (self.home_win, self.draw, self.away_win),
                ("home_win", "draw", "away_win")):
            if not isinstance(val, (int, float)):
                raise TypeError(f"Odds {name} values must be int or float, got {val!r}")
            if val < 0:
                raise ValueError(f"Odds {name} must be positive, got {val!r}")


@dataclass
class Game:
    """ Game Dataclass with post_init method for core validations."""
    id: int
    home: str
    away: str
    time: List[str]
    tournament: str
    odds: Odds | None = None #optional because we merge them later

    def __post_init__(self):
        if not isinstance(self.id, int):
            try:
                self.id = int(self.id)
            except TypeError:
                log.error(f"Invalid id, must be an integer/Failed to convert. Got {self.id!r}")
                raise TypeError(f"Game ID must be an integer/Failed to convert. Got {self.id!r}")

        for val, name in zip((self.home, self.away, self.tournament),
                             ("home", "away", "tournament")):
            if not isinstance(val, str):
                log.error(f"{name} values must be str, got {val!r}")
                raise TypeError(f"{name} values must be str, got {val!r}")

        if not isinstance(self.time, List):
            log.error(f"Time values must be List, got {self.time!r}")
            raise TypeError(f"Time values must be List, got {self.time!r}")

        if len(self.time) > 2:
            log.info(f"Got more than 2 values in time column: {self.time}. Please check!")

        if len(self.time) < 2:
            log.info(f"Got less than 2 values in time column: {self.time}")
            raise ValueError(f"Time value must be greater than 2 values in time column. Got {self.time!r}")

        if not isinstance(self.time, List):
            raise TypeError(f"Time values must be List, got {self.time!r}")

        date, time = self.time
        # Validate date
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise ValueError(f"Date must be in YYYY-MM-DD format, got: {date!r}")

        # Validate time
        try:
            time = datetime.strptime(time, "%H:%M")
        except (ValueError, TypeError):
            raise ValueError(f"Time must be in HH:MM format, got: {time!r}")

        if not isinstance(self.odds, Odds | None):
            log.error(f"Invalid odds, must be an Odd obj. or None, got {self.odds!r}")
            raise TypeError(f"Invalid odds, must be an Odds obj. or None, got {self.odds!r}")
