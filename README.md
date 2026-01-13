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

```
+------------------+
|   Gmail Inbox   |
+--------+---------+
         |
         | Gmail API (OAuth)
         v
+------------------+        +----------------------+
|  Python Script  | -----> |  Google Sheets API   |
|   (main.py)     |        |    Append Rows       |
+--------+---------+        +----------------------+
         |
         v
  state.json (last processed email ID)
```

---

## 📂 Project Structure

```
gmail-to-sheets-automation/
│
├── src/
│   ├── gmail_service.py
│   ├── sheets_service.py
│   ├── email_parser.py
│   └── main.py
│
├── credentials/
│   └── credentials.json        (DO NOT COMMIT)
│
├── state.json                  (auto-created)
├── token.json                  (auto-created, DO NOT COMMIT)
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

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
```
is:unread in:inbox
```

2. A local file is used:

`state.json`

It stores:

```json
{
  "last_id": "previous_email_id"
}
```

On each run:

- Script stops processing once it reaches the old ID  
- Emails are marked as read  
- Old emails are never fetched again  

✔ No duplicates  
✔ Crash-safe  
✔ Re-run safe  

---

## 🧠 Why This State Storage Was Chosen

- Lightweight (no database needed)  
- Human-readable  
- Survives restarts  
- Fast and reliable  
- Works even if Gmail label sync is slow  

---

## 🚀 Step-by-Step Setup Instructions

### 1️⃣ Create Google Cloud Project

Go to: https://console.cloud.google.com  
Create a new project.

---

### 2️⃣ Enable APIs

Enable:

- Gmail API  
- Google Sheets API  

---

### 3️⃣ Configure OAuth Consent Screen

Go to: **APIs & Services → OAuth consent screen**

- User type: **External**  
- Fill:
  - App Name  
  - Support Email  
  - Developer Email  
- Add your Gmail as **Test User**  
- Save  

---

### 4️⃣ Create OAuth Credentials

Go to: **APIs & Services → Credentials**

- Create **OAuth Client ID**  
- Application type: **Desktop App**  
- Download JSON and place it here:

```bash
credentials/credentials.json
```

---

### 5️⃣ Create Google Sheet

- Create a new Google Sheet  
- Add headers in the first row:

```text
From | Subject | Date | Content
```

- Copy **Sheet ID** from URL  
- Paste it into:

```python
config.py → SPREADSHEET_ID
```

---

### 6️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 7️⃣ Run the Script

```bash
python -m src.main
```

- First run will open browser for login  
- Click **Advanced → Continue** (if warning shows)  
- Click **Allow**  
- Emails will be processed and added to sheet  

---

## 🔁 What Happens If You Run It Twice?

On second run:

- No unread emails found  
- No duplicates added  
- Script exits safely  

---

## 📸 Proof of Execution

Inside `/proof/` folder:

- ✅ Gmail inbox screenshot  
- ✅ Google Sheet with 5+ rows  
- ✅ OAuth consent screen  
- ✅ Terminal output  
- ✅ Re-run output (showing no duplicates)  

Also record a **2–3 minute screen video** showing:

- Project flow  
- Data moving Gmail → Sheets  
- Duplicate prevention  
- Second run behavior  

---

## 🧪 Example Use Cases

- Customer support logging  
- Invoice email tracking  
- Lead capture from emails  
- Automation pipelines  

---

## ⚠️ Security Rules Followed

- ❌ `credentials.json` NOT committed  
- ❌ `token.json` NOT committed  
- ❌ `state.json` NOT committed  
- ❌ No API keys in code  
- ✔ `.gitignore` configured  

---

## 🧗 Challenges Faced

### 1. Parsing HTML Emails

Some emails only contain HTML body. Solved using:

- BeautifulSoup → HTML to text conversion  

### 2. Preventing Duplicate Entries

Solved using:

- Gmail UNREAD label  
- Local persistent `state.json`  

---

## 🚫 Limitations

- Only reads inbox (not spam/promotions)  
- Very large inbox pagination not implemented  
- Attachments not handled  
- Rate limiting not handled (can be added)  

---

## ⭐ Bonus Features Implemented

- ✔ HTML → plain text conversion  
- ✔ Duplicate prevention  
- ✔ Persistent state storage  
- ✔ Safe re-run behavior  
