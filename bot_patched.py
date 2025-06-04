
import os
import requests
import time
import logging
from dotenv import load_dotenv
from telegram import Bot

# Load .env file
load_dotenv()

# Telegram config
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Token config
SYMBOL = os.getenv("SYMBOL", "STITCH")
ADDRESS = os.getenv("TOKEN_ADDRESS")
UPPER_THRESHOLD = float(os.getenv("UPPER_THRESHOLD", 0.0006))
LOWER_THRESHOLD = float(os.getenv("LOWER_THRESHOLD", 0.0004))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_price():
    try:
        url = f"https://public-api.birdeye.so/public/price?address={ADDRESS}"
        headers = {"X-API-KEY": "public"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        value = data.get("data", {}).get("value")
        if value is not None:
            return float(value)
        else:
            logger.warning(f"No price value in response: {data}")
            return None
    except Exception as e:
        logger.error(f"Error getting price: {e}")
        return None

def send_alert(message):
    try:
        bot = Bot(token=TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        logger.error(f"Error sending Telegram alert: {e}")

def main():
    last_price = None
    while True:
        price = get_price()
        if price is None:
            time.sleep(10)
            continue

        logger.info(f"{SYMBOL} Price: {price}")
        if last_price is None:
            last_price = price

        if price >= UPPER_THRESHOLD and last_price < UPPER_THRESHOLD:
            send_alert(f"🚨 {SYMBOL} price just broke above 🚀 {UPPER_THRESHOLD}\nCurrent: {price}")
        elif price <= LOWER_THRESHOLD and last_price > LOWER_THRESHOLD:
            send_alert(f"🔻 {SYMBOL} price just dropped below ⚠️ {LOWER_THRESHOLD}\nCurrent: {price}")

        last_price = price
        time.sleep(15)

if __name__ == "__main__":
    main()
