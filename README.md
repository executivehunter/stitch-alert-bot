# STITCH Alert Bot

Bot Telegram untuk memantau harga token STITCH di jaringan Solana dan mengirimkan notifikasi jika harga menembus batas atas atau bawah.

## 🛠 Cara Install

1. Clone repo ini atau download ZIP
2. Buat file `.env` berdasarkan `.env.example`
3. Jalankan dengan:

```bash
pip install -r requirements.txt
python bot.py
```

## 🔧 Konfigurasi di .env
- `BOT_TOKEN` = Token dari BotFather
- `CHAT_ID` = ID grup/channel kamu
- `COIN_SYMBOL` = Nama token (default: STITCH)
- `UPPER_THRESHOLD` = Batas atas alert
- `LOWER_THRESHOLD` = Batas bawah alert
- `CHECK_INTERVAL` = Interval pengecekan harga (detik)

