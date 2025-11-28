import requests
from dotenv import load_dotenv
import os
from app.utils.logger import logger as log

############## LOAD ENV VARIABLES ##############
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") ###### ID for the Telegram bot chat with tel. number


def send_telegram_message(text: str) -> None:
    """ Sends a telegram message """
    log.info("Sending telegram message...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})  ## text = games data

