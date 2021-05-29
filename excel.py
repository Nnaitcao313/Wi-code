from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google.oauth2 import service_account

def get_values():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    SERVICE_ACCOUNT_FILE = 'e_key.json'

    creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)


    SAMPLE_SPREADSHEET_ID = '1IzoBBLi2t5-QJ1DcDCeawGEEM-lsmwyxAGm--p46f_U'

    SAMPLE_RANGE_NAME = 'A2:E400'

    service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    return values




