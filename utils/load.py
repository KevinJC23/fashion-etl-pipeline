from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd

def store_to_csv(data, filename):
    try:
        data.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving data to CSV: {e}")


def store_to_postgre(data, db_url):
    try:
        engine = create_engine(db_url)
        with engine.connect() as con:
            data.to_sql('products', con=con, if_exists='replace', index=False)
            print("Data successfully saved to PostgreSQL database")
    except Exception as e:
        print(f"An error occurred while saving data to PostgreSQL: {e}")


def store_to_googlesheets(data, json_keyfile, spreadsheet_id):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    try:
        creds = Credentials.from_service_account_file(json_keyfile, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        data_clean = data.fillna('')
        values = [data_clean.columns.values.tolist()] + data_clean.values.tolist()

        body = {'values': values}

        num_rows = len(data_clean) + 1
        num_cols = len(data_clean.columns)

        def get_col_letter(n):
            string = ""
            while n > 0:
                n, remainder = divmod(n - 1, 26)
                string = chr(65 + remainder) + string
            return string
            
        range_name = f"Sheet1!A1:{get_col_letter(num_cols)}{num_rows}"

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body,
        ).execute()

        print("Data successfully saved to Google Sheets")
    except Exception as e:
        print(f"An error occurred while saving data to Google Sheets: {e}")