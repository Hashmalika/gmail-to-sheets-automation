📧 Gmail to Google Sheets Automation (Python)

Author: Hashmalika Chalse

📌 Project Overview

This project is a Python automation system that:

Connects to Gmail API using OAuth 2.0

Connects to Google Sheets API

Reads real unread emails from Gmail Inbox

Extracts:

Sender

Subject

Date

Body (plain text)

Appends them into a Google Sheet

Marks emails as read after processing

Prevents duplicate entries

Stores state so old emails are never reprocessed

🏗️ High-Level Architecture
+------------------+
|   Gmail Inbox   |
+--------+---------+
         |
         | Gmail API (OAuth)
         v
+------------------+        +----------------------+
|   Python Script | -----> |  Google Sheets API   |
| (main.py)       |        |  Append Rows         |
+--------+---------+        +----------------------+
         |
         v
  state.json (last processed email ID)

📂 Project Structure
gmail-to-sheets/
│
├── src/
│   ├── gmail_service.py
│   ├── sheets_service.py
│   ├── email_parser.py
│   └── main.py
│
├── credentials/
│   └── credentials.json   (DO NOT COMMIT)
│
├── state.json             (auto-created)
├── config.py
├── requirements.txt
├── .gitignore
└── README.md

⚙️ Tech Stack

Python 3

Gmail API

Google Sheets API

OAuth 2.0

Libraries:

google-api-python-client

google-auth-oauthlib

beautifulsoup4

🔐 OAuth Flow Used

This project uses OAuth 2.0 Installed App Flow:

User runs the script

Browser opens Google login page

User grants permission

Google returns an access token

Token is saved locally in token.json

Next runs reuse the token without login

✔ No service accounts
✔ No API keys
✔ Fully compliant with Gmail API rules

🧠 How Duplicate Prevention Works

Two layers of safety:

Only fetch:

is:unread in:inbox


A local file is used:

state.json


It stores:

{
  "last_id": "previous_email_id"
}


On each run:

Script stops processing once it reaches the old ID

Emails are marked as read

Old emails are never fetched again

✔ No duplicates
✔ Crash-safe
✔ Re-run safe

🧠 Why This State Storage Was Chosen

Lightweight (no database needed)

Human-readable

Survives restarts

Fast and reliable

Works even if Gmail label sync is slow

🚀 Step-by-Step Setup Instructions
1️⃣ Create Google Cloud Project

Go to: https://console.cloud.google.com

Create new project

2️⃣ Enable APIs

Enable:

Gmail API

Google Sheets API

3️⃣ Create OAuth Credentials

Go to: APIs & Services → Credentials

Create OAuth Client ID

Type: Desktop App

Download JSON

Put it in:

credentials/credentials.json

4️⃣ Create Google Sheet

Create a new Google Sheet

Add headers:

From | Subject | Date | Content


Copy Sheet ID from URL

Paste into:

config.py → SPREADSHEET_ID

5️⃣ Install Dependencies
pip install -r requirements.txt

6️⃣ Run the Script
python src/main.py


First run will open browser for login

Grant permission

Emails will be processed and added to sheet

🔁 What Happens If You Run It Twice?

Second run:

No unread emails found

No duplicates added

Script exits safely

📸 Proof of Execution (To Be Added in Repo)

Inside /proof/ folder:

✅ Gmail inbox screenshot

✅ Google Sheet with 5+ rows

✅ OAuth consent screen

✅ (Optional) Terminal output
