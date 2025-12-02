from app.services.api_client import ApiClient
from app.services.telegram_sender import send_telegram_message
from app.utils.helpers import API_SPORTS, API_SPORTS_ODDS, TODAY
from app.utils.logger import logger as log
from app.data.teams import IMPORTANT_TEAMS


def main() -> None:
    client = ApiClient(IMPORTANT_TEAMS, use_mock=True)  # add parameter use_mock=True for testing
    data = client.get_matches(API_SPORTS, API_SPORTS_ODDS)
    if not data:
        send_telegram_message(f"No important matches for today: {TODAY}")
    else:
        send_telegram_message(data)
    log.info("Completed!")


if __name__ == "__main__":
    main()