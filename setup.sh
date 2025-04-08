#!/bin/bash

# Banner Display with colors and enhanced styling
clear
echo -e "\e[1;32m=====================================\e[0m"
echo -e "\e[1;33m    \e[1;34mEgaleX5 Tool Setup Script\e[0m"
echo -e "\e[1;32m=====================================\e[0m"

# Step 0: Check Installed Packages
echo -e "\n\e[1;36m[+] Checking which packages are already installed...\e[0m"

required_pkgs=(python git nano curl openssh cloudflared)
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
    echo -e "\e[1;36mWill be Installed:\e[0m"
    echo -e " Nothing to install. All packages are up to date."
fi

# Step 1: Update and Upgrade Termux
echo -e "\n\e[1;36mUpdating Termux packages...\e[0m"
pkg update -y && pkg upgrade -y

# Step 2: Install Required Termux Packages
echo -e "\e[1;36mInstalling required Termux packages...\e[0m"
pkg install -y python git nano curl openssh

# Step 3: Install Python and Dependencies
echo -e "\e[1;36mUpgrading pip and installing Python libraries...\e[0m"
pip install --upgrade pip

# Install Python Libraries with Dependencies
echo -e "\e[1;35mInstalling Flask and Requests (with all sub-dependencies)...\e[0m"
pip install flask requests

# Install Specific Libraries for Better Compatibility (Optional)
echo -e "\e[1;35mInstalling additional Python libraries for better compatibility...\e[0m"
pip install flask-cors Werkzeug Jinja2 itsdangerous click

# Step 4: Install Cloudflared
echo -e "\n\e[1;36mInstalling Cloudflared...\e[0m"
pkg install -y cloudflared
if [ $? -ne 0 ]; then
    echo -e "\e[1;31mCloudflared package installation failed. Downloading binary...\e[0m"
    curl -LO https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm
    chmod +x cloudflared-linux-arm
    mv cloudflared-linux-arm /data/data/com.termux/files/usr/bin/cloudflared
    echo -e "\e[1;32mCloudflared binary downloaded and moved successfully.\e[0m"
else
    echo -e "\e[1;32mCloudflared installation successful.\e[0m"
fi

# Step 5: SSH Setup and Key Generation
echo -e "\n\e[1;36mSetting up SSH...\e[0m"
# Check if SSH is installed
if ! command -v ssh &>/dev/null; then
    echo -e "\e[1;31mSSH client not found! Installing SSH...\e[0m"
    pkg install -y openssh
else
    echo -e "\e[1;32mSSH is already installed!\e[0m"
fi

# Generate SSH key pair (if not already present)
echo -e "\n\e[1;36mGenerating SSH key pair...\e[0m"
if [ ! -f ~/.ssh/id_rsa ]; then
    echo -e "\e[1;35mSSH key pair not found! Generating a new key...\e[0m"
    ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -N ""
else
    echo -e "\e[1;32mSSH key pair already exists.\e[0m"
fi

# Step 6: Verify All Installations
echo -e "\n\e[1;36mVerifying all installations and dependencies...\e[0m"
echo -e "\n\e[1;33mPython Version:\e[0m"
python --version

echo -e "\e[1;33mInstalled Python Libraries:\e[0m"
pip list

echo -e "\e[1;33mCloudflared Version:\e[0m"
cloudflared --version

echo -e "\e[1;33mSSH Version:\e[0m"
ssh -V

# Step 7: Clone the `joker-Eye.py` repository
echo -e "\n\e[1;36mCloning the EgaleX5 tool repository...\e[0m"
git clone https://github.com/egalex5/joker-Eye.git

# Step 8: Display Final Instructions
clear
echo -e "\e[1;32m=====================================\e[0m"
echo -e "\e[1;33m      Setup Completed Successfully!\e[0m"
echo -e "\e[1;32m=====================================\e[0m"
echo -e "\n\e[1;36mRun your tool with: \e[1;32mpython joker-Eye.py\e[0m"
echo -e "\e[1;32mEnjoy using EgaleX5's tool without any issues!\e[0m"
