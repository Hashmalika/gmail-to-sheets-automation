from googleapiclient.discovery import build
from .gmail_service import get_gmail_service
from config import SPREADSHEET_ID, SHEET_NAME


def get_sheets_service():
    gmail_creds = get_gmail_service()._http.credentials
    return build("sheets", "v4", credentials=gmail_creds)

def append_rows(rows):
    service = get_sheets_service()
    body = {"values": rows}

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_NAME,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
