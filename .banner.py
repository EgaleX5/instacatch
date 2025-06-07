# banner.py

import os
import time
import shutil

# Color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Get terminal width
try:
    term_width = shutil.get_terminal_size().columns
except:
    term_width = 40

# Banner lines (excluding dynamic lines)
banner_text = f"""
{RED}
           E G A L E X 5
     --- Hacking is not a crime, it's skills ---
    Welcome to hacking World
{RESET}
"""

# Show banner with optional typing delay
def show_banner(delay=0.01):
    os.system("clear")
    print(f"{RED}=" * term_width)
    for char in banner_text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print(f"{RED}=" * term_width)
