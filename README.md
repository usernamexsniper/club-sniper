# 🎯 Club Sniper – Username Availability Checker for Club.com

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Club Sniper** is a high‑performance Python tool that checks whether usernames are available on **club.com**. It generates thousands of random usernames (or reads from a file) and checks them concurrently at blazing speed.

> **YouTube Tutorial:** [@usernamexsnipping][https://youtube.com/@usernamexsnipping] (https://youtube.com/@usernamexsnipping)  
> **Telegram Channel:** [usernamexsniper] (https://t.me/usernamexsniper)

---

## 📦 Features

- ✅ **Single username check** – Quickly test one name.
- ✅ **Bulk generation + check** – Generate thousands of random usernames (custom length & count) and check all at once.
- ✅ **File input** – Provide your own list of usernames (one per line).
- ✅ **Multi‑threaded** – 20 concurrent workers for maximum speed.
- ✅ **Smart fallback** – Uses profile page checking if the official API is unavailable.
- ✅ **Colored output** – Green = available, Red = taken, Yellow = error.
- ✅ **Anti‑tamper** – Basic protection against renaming the script.

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/usernamexsniper/club-sniper.git
cd club-sniper
2. Install dependencies
bash
pip install -r requirements.txt
The only required package is requests. colorama is optional but recommended for colored output.

🎮 Usage
Run the script:

bash
python club.py
Main Menu
text
==================================================
   CLUB RIPPER - Username Sniper
   YouTube: @usernamexsnipping | GitHub: @usernamexsnipper
==================================================

[1] Generate & check usernames
[2] Check from file
[3] Exit
Option 1 – Generate & Check
Enter the number of usernames to generate (e.g., 500).

Enter the length of each username (e.g., 4 for 4‑character names).

The script will generate random lowercase alphanumeric usernames and check them on club.com.

Available usernames are displayed in green and can be saved to a file.

Option 2 – Check from File
Provide a text file containing one username per line.

The script checks each username and shows availability.

Example output
text
[+] Generating 500 usernames...
[+] Checking 500 usernames on club.com...

[1/500] ✓ AVAILABLE: a3k9
[2/500] ✗ TAKEN:     wealth
[3/500] ✓ AVAILABLE: zx4m
...

[+] Found 23 available usernames:
    a3k9
    zx4m
    ...

Save to file? (y/n): y
Filename (default: available.txt): my_names.txt
[+] Saved to my_names.txt
⚙️ How It Works
Club Sniper uses two methods to determine availability:

Official API (if found) – The script can be configured to call club.com's internal API endpoint. This is the fastest method (milliseconds per check).
If you discover the real API endpoint, update the REAL_API_URL variable at the top of club.py.

Profile Page Fallback – If no API is available, the script simply tries to visit https://club.com/@{username}.

HTTP 200 + page contains "not found" → available

HTTP 200 + normal profile → taken

HTTP 404 → available

This method works reliably because club.com does not block profile page checks.

🔧 Customisation
You can tweak the script by editing these variables inside club.py:

python
REAL_API_URL = None          # Set to the actual API endpoint if you find it
USERNAME_PARAM = "username"  # Parameter name the API expects
MAX_WORKERS = 20             # Number of concurrent threads
📂 File Structure
text
club-sniper/
├── club.py             # Main script
├── requirements.txt    # Dependencies
├── README.md           # This file
└── LICENSE             # MIT license (optional)
⚠️ Disclaimer
This tool is for educational purposes only. Use it responsibly.

Do not spam club.com with excessive requests.

Respect the website's terms of service.

The author is not responsible for any misuse.

🧑‍💻 Author
YouTube: @usernamexsnipping

Telegram: @usernamexsniper

GitHub: @usernamexsniper

⭐ Support
If you find this tool useful, please star the repository and share the YouTube tutorial with others. Pull requests and suggestions are welcome!

📜 License
This project is licensed under the MIT License – see the LICENSE file for details.

text

---

## ✅ Also create `requirements.txt`

```txt
requests>=2.31.0
colorama>=0.4.6
