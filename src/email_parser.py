# import base64
# from bs4 import BeautifulSoup

# def extract_email_data(message):
#     headers = message["payload"]["headers"]

#     def get_header(name):
#         for h in headers:
#             if h["name"] == name:
#                 return h["value"]
#         return ""

#     sender = get_header("From")
#     subject = get_header("Subject")
#     date = get_header("Date")

#     body = ""

#     parts = message["payload"].get("parts", [])
#     if parts:
#         for part in parts:
#             if part["mimeType"] == "text/plain":
#                 data = part["body"]["data"]
#                 body = base64.urlsafe_b64decode(data).decode("utf-8")
#                 break
#             if part["mimeType"] == "text/html":
#                 data = part["body"]["data"]
#                 html = base64.urlsafe_b64decode(data).decode("utf-8")
#                 body = BeautifulSoup(html, "html.parser").get_text()

#     return sender, subject, date, body.strip()

import base64
from bs4 import BeautifulSoup

def extract_email_data(message):
    headers = message["payload"]["headers"]

    def get_header(name):
        for h in headers:
            if h["name"] == name:
                return h["value"]
        return ""

    sender = get_header("From")
    subject = get_header("Subject")
    date = get_header("Date")

    body = ""

    # Gmail message parts
    parts = message["payload"].get("parts", [])
    if parts:
        for part in parts:
            mime_type = part.get("mimeType", "")
            data = part.get("body", {}).get("data")
            if not data:
                continue
            decoded = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

            if mime_type == "text/plain":
                body = decoded
                break  # Prefer plain text
            elif mime_type == "text/html":
                # Convert HTML to clean text
                soup = BeautifulSoup(decoded, "html.parser")
                body = soup.get_text(separator="\n")  # keeps line breaks
                break

    # fallback: sometimes body is in payload itself
    if not body and "body" in message["payload"]:
        data = message["payload"]["body"].get("data")
        if data:
            decoded = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
            soup = BeautifulSoup(decoded, "html.parser")
            body = soup.get_text(separator="\n")

    return sender, subject, date, body.strip()
