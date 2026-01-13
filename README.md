
# 📧 Gmail to Google Sheets Automation Pipeline (Python)

**Author:** Hashmalika Chalse

---

## 📌 Project Overview

This project is a Python automation system that:

- Connects to **Gmail API** using OAuth 2.0  
- Connects to **Google Sheets API**  
- Reads real **unread emails** from Gmail Inbox  
- Extracts:
  - Sender
  - Subject
  - Date
  - Body (plain text)
- Appends them into a Google Sheet  
- Marks emails as **read after processing**  
- Prevents **duplicate entries**  
- Stores **state** so old emails are never reprocessed  

---

## 🏗️ High-Level Architecture

+------------------+
| Gmail Inbox |
+--------+---------+
|
| Gmail API (OAuth)
v
+------------------+ +----------------------+
| Python Script | -----> | Google Sheets API |
| (main.py) | | Append Rows |
+--------+---------+ +----------------------+
|
v
state.json (last processed email ID)

yaml
Copy code

---

## 📂 Project Structure

gmail-to-sheets-automation/
│
├── src/
│ ├── gmail_service.py
│ ├── sheets_service.py
│ ├── email_parser.py
│ └── main.py
│
├── credentials/
│ └── credentials.json (DO NOT COMMIT)
│
├── state.json (auto-created)
├── token.json (auto-created, DO NOT COMMIT)
├── config.py
├── requirements.txt
├── .gitignore
└── README.md

yaml
Copy code

---

## ⚙️ Tech Stack

- Python 3  
- Gmail API  
- Google Sheets API  
- OAuth 2.0  

**Libraries:**

- google-api-python-client  
- google-auth-oauthlib  
- beautifulsoup4  

---

## 🔐 OAuth Flow Used

This project uses **OAuth 2.0 Installed App Flow**:

1. User runs the script  
2. Browser opens Google login page  
3. User grants permission  
4. Google returns an access token  
5. Token is saved locally in `token.json`  
6. Next runs reuse the token without login  

✔ No service accounts  
✔ No API keys  
✔ Fully compliant with Gmail API rules  

---

## 🧠 How Duplicate Prevention Works

Two layers of safety:

1. Only fetch:

is:unread in:inbox


2. A local file is used:

state.json
It stores:

```json
{
  "last_id": "previous_email_id"
}

