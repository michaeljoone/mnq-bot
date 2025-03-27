
# MNQ Bot Core Structure (main.py)

import os
import time
import requests
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

# === ENVIRONMENT CONFIG ===
TRADOVATE_USERNAME = os.getenv("TRADOVATE_USERNAME")
TRADOVATE_PASSWORD = os.getenv("TRADOVATE_PASSWORD")
TRADOVATE_API_BASE = os.getenv("TRADOVATE_API_BASE")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# === SEND ALERT TO TELEGRAM ===
def send_telegram(msg):
    try:
        bot.send_message(chat_id=TELEGRAM_USER_ID, text=msg)
    except Exception as e:
        print(f"Telegram error: {e}")

# === LOGIN TO TRADOVATE ===
def login():
    url = f"{TRADOVATE_API_BASE}/auth/accesstokenrequest"
    payload = {
        "name": TRADOVATE_USERNAME,
        "password": TRADOVATE_PASSWORD,
        "appId": "MNQBot",
        "appVersion": "1.0",
        "cid": 0
    }
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        token = r.json()["accessToken"]
        return token
    else:
        send_telegram("Login failed to Tradovate.")
        return None

# === EXAMPLE STRATEGY LOOP ===
def run_bot():
    token = login()
    if not token:
        return

    send_telegram("MNQ Bot is now live!")

    headers = {"Authorization": f"Bearer {token}"}

    while True:
        # --- Example: Fetch MNQ price (replace with real logic later) ---
        price_data = requests.get(f"{TRADOVATE_API_BASE}/md/quote/MNQM5", headers=headers)
        if price_data.status_code == 200:
            price = price_data.json().get("last", 0)
            print(f"Price: {price}")
            send_telegram(f"MNQ Price: {price}")
        else:
            print("Failed to get price.")

        time.sleep(60)  # check every 1 minute

if __name__ == "__main__":
    run_bot()
