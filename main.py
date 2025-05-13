import pandas as pd
from utils.extract import extract_data
from utils.transform import transform_data
from utils.transform import transform_to_DataFrame
from utils.load import load_data

# URL untuk scraping
BASE_URL = <Masukkan link untuk scrapping>

# Database URL
DB_URL = <Masukkan link DB dari postgreSQL>

# Google Sheets Config
GSHEET_ID = <masukkan link id google sheets>
SHEET_NAME = <masukan nama sheets tab, bukan nama file spreadsheets>

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
