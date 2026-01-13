# from googleapiclient.discovery import build
# from .gmail_service import get_gmail_service
# from config import SPREADSHEET_ID, SHEET_NAME


# def get_sheets_service():
#     gmail_creds = get_gmail_service()._http.credentials
#     return build("sheets", "v4", credentials=gmail_creds)

# def append_rows(rows):
#     service = get_sheets_service()
#     body = {"values": rows}

#     service.spreadsheets().values().append(
#         spreadsheetId=SPREADSHEET_ID,
#         range=SHEET_NAME,
#         valueInputOption="RAW",
#         insertDataOption="INSERT_ROWS",
#         body=body
#     ).execute()

from googleapiclient.discovery import build
from .gmail_service import get_gmail_service
from config import SPREADSHEET_ID, SHEET_NAME
import time
from functools import wraps

# -------------------------
# Retry Decorator for API calls
# -------------------------
def retry_on_exception(max_retries=3, delay=2):
    def decorator(func):
        from functools import wraps
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    # Only wait, no logging
                    time.sleep(delay)
            raise Exception(f"Failed after {max_retries} retries.")
        return wrapper
    return decorator

# -------------------------
# Sheets Service
# -------------------------
def get_sheets_service():
    """Get Google Sheets service using Gmail credentials."""
    gmail_creds = get_gmail_service()._http.credentials
    return build("sheets", "v4", credentials=gmail_creds)

# -------------------------
# Append Rows with Retry
# -------------------------
@retry_on_exception(max_retries=3, delay=2)
def append_rows(rows):
    service = get_sheets_service()
    body = {"values": rows}
    
    return service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_NAME,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
