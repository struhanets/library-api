import os

import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)

    return response.json()
