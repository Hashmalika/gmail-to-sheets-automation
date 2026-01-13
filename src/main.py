import os
import json

from .gmail_service import get_gmail_service
from .sheets_service import append_rows
from .email_parser import extract_email_data
from config import STATE_FILE


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"last_id": None}

def save_state(last_id):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_id": last_id}, f)

def main():
    service = get_gmail_service()
    state = load_state()

    results = service.users().messages().list(
        userId="me",
        q="is:unread in:inbox"
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
        print(f"Added {len(rows)} emails to sheet.")

if __name__ == "__main__":
    main()
