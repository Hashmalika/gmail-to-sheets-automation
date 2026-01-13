import os
import json

import datetime
from .gmail_service import get_gmail_service
from .sheets_service import append_rows
from .email_parser import extract_email_data
from config import STATE_FILE

import time
from functools import wraps

def retry_on_exception(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    log(f"Error: {e}. Retry {retries}/{max_retries} in {delay}s...")
                    time.sleep(delay)
            raise Exception(f"Failed after {max_retries} retries.")
        return wrapper
    return decorator

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"last_id": None}

def save_state(last_id):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_id": last_id}, f)


def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
def main():
    service = get_gmail_service()
    state = load_state()
    
    SUBJECT_KEYWORD = "Invoice"  # Change as needed
    query = f"is:unread in:inbox subject:{SUBJECT_KEYWORD}"

    results = service.users().messages().list(
      userId="me",
      q=query
    ).execute()
    

    messages = results.get("messages", [])
    if not messages:
        print("No new emails.")
        return

    rows = []
    newest_id = state["last_id"]

    for msg in messages:
        msg_id = msg["id"]

        if state["last_id"] == msg_id:
            break

        full_msg = service.users().messages().get(
            userId="me", id=msg_id, format="full"
        ).execute()

        sender, subject, date, body = extract_email_data(full_msg)

        rows.append([sender, subject, date, body])

        # Mark as read
        service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

        if newest_id is None:
            newest_id = msg_id

    if rows:
        append_rows(rows)
        save_state(newest_id)
        log(f"Added {len(rows)} emails to sheet.")



if __name__ == "__main__":
    main()
