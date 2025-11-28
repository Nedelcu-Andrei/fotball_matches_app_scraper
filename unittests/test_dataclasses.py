import pytest
from app.data.models import Game, Odds

################# Game dataclass object tests #################
class TestGame:
    def test_game_invalid_id(self):
        with pytest.raises(ValueError):
            Game(id="adc", home="TeamA", away="TeamB", time=["2024", "12"], tournament="Liga")

    def test_game_invalid_home_win(self):
        with pytest.raises(TypeError):
            Game(id=10, home=123, away="TeamB", time=["2024", "12"], tournament="Liga")

    def test_game_invalid_away(self):
        with pytest.raises(TypeError):
            Game(id=10, home="TeamA", away=123, time=["2025-02-14", "18:00"], tournament= "Liga")

    def test_game_invalid_tournament(self):
        with pytest.raises(TypeError):
            Game(id=10, home="TeamA", away="TeamB", time=["2025-02-14", "18:00"], tournament= 123)

    def test_game_invalid_odds_int(self):
        with pytest.raises(TypeError):
            Game(id=10, home="TeamA", away="TeamB", time=["2025-02-14", "18:00"], tournament="Liga", odds=12)

    def test_game_invalid_odds_float(self):
        with pytest.raises(TypeError):
            Game(id=10, home="TeamA", away="TeamB", time=["2025-02-14", "18:00"], tournament="Liga", odds=1.2)

    def test_game_invalid_odds_ls(self):
        with pytest.raises(TypeError):
            Game(id=10, home="TeamA", away="TeamB", time=["2025-02-14", "18:00"], tournament="Liga", odds=[])

    def test_game_invalid_odds_tuple(self):
        with pytest.raises(TypeError):
            Game(id=10, home="TeamA", away="TeamB", time=["2025-02-14", "18:00"], tournament="Liga", odds=())

    def test_game_invalid_time_type_tuple(self):
        with pytest.raises(TypeError):
            Game(id=10, home="TeamA", away="TeamB", time=(), tournament="Liga")

    def test_game_invalid_time_type_dict(self):
        with pytest.raises(TypeError):
            Game(id=10, home="TeamA", away="TeamB", time={}, tournament="Liga")

    def test_game_invalid_time_not_list(self):
        with pytest.raises(TypeError):
            Game(id=10, home="TeamA", away="TeamB", time="2025-02-14 18:00", tournament="Liga")

    def test_game_invalid_time_length_wrong(self):
        with pytest.raises(ValueError):
            Game(id=10, home="TeamA", away="TeamB", time=["2025-02-14"], tournament="Liga")

    def test_game_invalid_time_wrong_format_date(self):
        with pytest.raises(ValueError):
            Game(id=10, home="TeamA", away="TeamB", time=["2025/02/14 18:00"], tournament="Liga")

    def test_game_invalid_time_wrong_format_time(self):
        with pytest.raises(ValueError):
            Game(id=10, home="TeamA", away="TeamB", time=["2025-02-14 6 PM"], tournament="Liga")

    def test_game_valid_time(self):
        g = Game(id=10, home="TeamA", away="TeamB", time=["2025-02-14", "18:00"], tournament="Liga")
        assert g.time == ["2025-02-14", "18:00"]




################# Odds dataclass object tests #################
class TestOdds:
    def test_odds_valid(self):
        o = Odds(game_id=12, home_win=1.45, draw=3.2, away_win=2.9)
        assert o.game_id == 12
        assert o.home_win == 1.45

    def test_odds_invalid_game_id(self):
        with pytest.raises(TypeError):
            Odds(game_id="abc", home_win=1.4, draw=2.0, away_win=3.0)

    def test_odds_invalid_game_id_tuple(self):
        with pytest.raises(TypeError):
            Odds(game_id=(), home_win=1.4, draw=2.0, away_win=3.0)

    def test_odds_invalid_game_id_dict(self):
        with pytest.raises(TypeError):
            Odds(game_id={}, home_win=1.4, draw=2.0, away_win=3.0)

    def test_odds_invalid_game_id_set(self):
        with pytest.raises(TypeError):
            Odds(game_id=set, home_win=1.4, draw=2.0, away_win=3.0)

    def test_odds_invalid_game_id_lst(self):
        with pytest.raises(TypeError):
            Odds(game_id=[], home_win=1.4, draw=2.0, away_win=3.0)

    def test_odds_invalid_game_id_zero(self):
        o = Odds(game_id=0, home_win=1.4, draw=2.0, away_win=3.0)
        assert o.game_id == 0

    def test_odds_negative_value(self):
        with pytest.raises(ValueError):
            Odds(game_id=10, home_win=-1.2, draw=2.0, away_win=3.0)

    def test_odds_str_value(self):
        with pytest.raises(TypeError):
            Odds(game_id=10, home_win="-1.2", draw=2.0, away_win=3.0)

    def test_odds_tuple_value(self):
        with pytest.raises(TypeError):
            Odds(game_id=10, home_win=(), draw=2.0, away_win=3.0)

    def test_odds_dict_value(self):
        with pytest.raises(TypeError):
            Odds(game_id=10, home_win={}, draw=2.0, away_win=3.0)

    def test_odds_set_value(self):
        with pytest.raises(TypeError):
            Odds(game_id=10, home_win=set, draw=2.0, away_win=3.0)




