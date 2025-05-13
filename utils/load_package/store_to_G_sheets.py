import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Configuration
SERVICE_ACCOUNT_FILE = 'gcp_key.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
GSHEET_ID = '1FTkvlwCWrMj_sgFm6b9QUIk5IFJArNfbRtXrTobGeV0'
SHEET_NAME = 'Fashion_db_g_sheets'  # Update this to your sheet name

# Authenticate
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

def dataframe_to_sheets(data, sheet_name, gsheet_id):
    """Write DataFrame to Google Sheets."""
    try:
        # Ensure the data is a DataFrame
        if not isinstance(data, pd.DataFrame):
            print("Data is not a DataFrame. Converting to DataFrame...")
            data = pd.DataFrame(data)

        # Convert DataFrame to list of lists
        data_list = [data.columns.tolist()] + data.values.tolist()

        # Define the range to update (adjust the range as needed)
        range_ = f"{sheet_name}!A1"

        # Prepare the request body
        body = {
            'values': data_list
        }

        # Update the data in the Google Sheets
        response = sheet.values().update(
            spreadsheetId=gsheet_id,
            range=range_,
            valueInputOption="RAW",
            body=body
        ).execute()

        print(f"Data successfully written to {sheet_name} in Google Sheets!")
        print(f"{response.get('updatedCells')} cells updated.")

    except Exception as e:
        print(f"An error occurred while writing to Google Sheets: {e}")



