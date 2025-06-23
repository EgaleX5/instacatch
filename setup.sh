#!/bin/bash

# Banner Display with colors and enhanced styling
clear
echo -e "\e[1;32m=====================================\e[0m"
echo -e "\e[1;33m    \e[1;34mEgaleX5 Tool Setup Script\e[0m"
echo -e "\e[1;32m=====================================\e[0m"

# Step 0: Check Installed Packages
echo -e "\n\e[1;36m[+] Checking which packages are already installed...\e[0m"

required_pkgs=(python git nano curl openssh cloudflared openssl-tool)
installed_pkgs=()
missing_pkgs=()

for pkg in "${required_pkgs[@]}"; do
    if command -v "$pkg" &>/dev/null; then
        echo -e "\e[1;32m[✓] $pkg is already installed.\e[0m"
        installed_pkgs+=("$pkg")
    else
        echo -e "\e[1;31m[✗] $pkg is NOT installed.\e[0m"
        missing_pkgs+=("$pkg")
    fi
done

# Show summary
echo -e "\n\e[1;33mAlready Installed:\e[0m ${installed_pkgs[*]}"

if [ ${#missing_pkgs[@]} -gt 0 ]; then
    echo -e "\e[1;36mWill be Installed:\e[0m"
    for pkg in "${missing_pkgs[@]}"; do
        echo -e " - $pkg"
    done
else
    echo -e "\e[1;36mWill be Installed:\e[0m Nothing to install. All packages are up to date."
fi

# Step 1: Update and Upgrade Termux
echo -e "\n\e[1;36mUpdating Termux packages...\e[0m"
pkg update -y && pkg upgrade -y

# Step 2: Install Required Termux Packages
echo -e "\e[1;36mInstalling required Termux packages...\e[0m"
pkg install -y python git nano curl openssh cloudflared openssl-tool

# Ensure OpenSSL binary is present
if [ ! -f "/data/data/com.termux/files/usr/bin/openssl" ]; then
    echo -e "\e[1;31m[!] OpenSSL binary missing! Attempting to reinstall...\e[0m"
    pkg install -y openssl-tool
    if [ ! -f "/data/data/com.termux/files/usr/bin/openssl" ]; then
        echo -e "\e[1;31m[✗] Failed to install OpenSSL binary. Please install manually.\e[0m"
    else
        echo -e "\e[1;32m[✓] OpenSSL installed successfully.\e[0m"
    fi
else
    echo -e "\e[1;32m[✓] OpenSSL binary is available.\e[0m"
fi

# Step 3: Install Python Libraries
echo -e "\e[1;36mUpgrading pip and installing Python libraries...\e[0m"
pip install --upgrade pip
pip install flask requests flask-cors Werkzeug Jinja2 itsdangerous click

# Step 4: SSH Setup and Key Generation
echo -e "\n\e[1;36mSetting up SSH...\e[0m"
if ! command -v ssh &>/dev/null; then
    pkg install -y openssh
else
    echo -e "\e[1;32m[✓] SSH is already installed!\e[0m"
fi

# SSH keygen
echo -e "\n\e[1;36mGenerating SSH key pair...\e[0m"
if [ ! -f ~/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -N ""
    echo -e "\e[1;32m[✓] SSH key generated.\e[0m"
else
    echo -e "\e[1;32m[✓] SSH key already exists.\e[0m"
fi

# Step 5: Verify Installations
echo -e "\n\e[1;36mVerifying all installations and dependencies...\e[0m"
echo -e "\n\e[1;33mPython Version:\e[0m"
python --version

echo -e "\e[1;33mInstalled Python Libraries:\e[0m"
pip list

echo -e "\e[1;33mCloudflared Version:\e[0m"
cloudflared --version

echo -e "\e[1;33mSSH Version:\e[0m"
ssh -V

echo -e "\e[1;33mOpenSSL Version:\e[0m"
/data/data/com.termux/files/usr/bin/openssl version

# Final Message
clear
echo -e "\e[1;32m=====================================\e[0m"
echo -e "\e[1;33m      Setup Completed Successfully!\e[0m"
echo -e "\e[1;32m=====================================\e[0m"
echo -e "\n\e[1;36mRun your tool with: \e[1;32mpython3 main.py\e[0m"
echo -e "\e[1;32mEnjoy using EgaleX5's tool without any issues!\e[0m"
