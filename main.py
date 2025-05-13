import pandas as pd
from utils.extract import extract_data
from utils.transform import transform_data
from utils.transform import transform_to_DataFrame
from utils.load import load_data

# URL untuk scraping
BASE_URL = 'https://fashion-studio.dicoding.dev/'

# Database URL
DB_URL = "postgresql+psycopg2://developer:supersecretpassword@localhost:5432/fashiondb"

# Google Sheets Config
GSHEET_ID = '1FTkvlwCWrMj_sgFm6b9QUIk5IFJArNfbRtXrTobGeV0'
SHEET_NAME = 'Sheet1'

def main():
    """Proses utama ETL: Extract, Transform, Load"""
    
    print("\n=== Memulai proses Extract ===")
    try:
        raw_data = extract_data(BASE_URL)
        print("Extract selesai.")
    except Exception as e:
        print(f"Kesalahan pada proses Extract: {e}")
        return

    print("\n=== Memulai proses Transform ===")
    try:
        transformed_data = transform_to_DataFrame(raw_data)
        if not transformed_data.empty:
            transformed_data = transform_data(transformed_data, exchange_rate=16000)
            print("Transform selesai.")
        else:
            print("Data kosong setelah proses Extract. Transformasi tidak dilakukan.")
            return
    except Exception as e:
        print(f"Kesalahan pada proses Transform: {e}")
        return

    print("\n=== Memulai proses Load ===")
    try:
        load_data(transformed_data, DB_URL, SHEET_NAME, GSHEET_ID)
    except Exception as e:
        print(f"Kesalahan pada proses Load: {e}")

if __name__ == "__main__":
    main()
