# import pandas as pd
# from google.oauth2.service_account import Credentials
# from googleapiclient.discovery import build
# # Configuration
# SERVICE_ACCOUNT_FILE = 'gcp_key.json'
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# GSHEET_ID = '1FTkvlwCWrMj_sgFm6b9QUIk5IFJArNfbRtXrTobGeV0'
# SHEET_NAME = 'Fashion_db_g_sheets'  # Update this to your sheet name

# # Authenticate
# credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# service = build('sheets', 'v4', credentials=credentials)
# sheet = service.spreadsheets()

# # Cek daftar sheet
# sheets_metadata = service.spreadsheets().get(spreadsheetId=GSHEET_ID).execute()
# sheets = sheets_metadata.get('sheets', '')

# for sheet in sheets:
#     print(sheet.get("properties", {}).get("title"))

import sys
print(sys.path)

try:
    from google.oauth2 import service_account
    print("Module google.oauth2 ditemukan!")
except ModuleNotFoundError as e:
    print(f"Error: {e}")
