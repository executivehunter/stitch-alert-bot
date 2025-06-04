
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
COIN_SYMBOL = os.getenv("COIN_SYMBOL", "STITCH")
UPPER_THRESHOLD = float(os.getenv("UPPER_THRESHOLD", 0.0005999))
LOWER_THRESHOLD = float(os.getenv("LOWER_THRESHOLD", 0.0003999))
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 30))

def get_price():
    url = f"https://public-api.birdeye.so/public/price?address=FZtZ18nBcmMGybLaAzDChWETuFfBMXcp49yDT2L2Y2R9"
    headers = {"X-API-KEY": "public"}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return float(data["data"]["value"])
    except Exception as e:
        print("Error fetching price:", e)
        return None

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

def main():
    while True:
        price = get_price()
        if price:
            print(f"[INFO] Harga {COIN_SYMBOL}: {price}")
            if price >= UPPER_THRESHOLD:
                send_alert(f"🚀 {COIN_SYMBOL} menembus harga atas: {price}")
            elif price <= LOWER_THRESHOLD:
                send_alert(f"⚠️ {COIN_SYMBOL} turun di bawah harga batas: {price}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
