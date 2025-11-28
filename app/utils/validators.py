from app.data.models import Game, Odds


########################## No complex validation needed over the dataclass post_init validations at the moment ##########################

def validate_start_timestamp(data: int) -> bool:
    return len(str(data)) == 10


def validate_odds_data(data: Odds) -> bool:
    pass