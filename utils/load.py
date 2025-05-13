import pandas as pd
from utils.load_package.store_to_csv import store_to_csv
from utils.load_package.store_to_db import store_to_postgre
from utils.load_package.store_to_G_sheets import dataframe_to_sheets

def load_data(data, db_url, sheet_name, gsheet_id):
    """Memuat data ke CSV, PostgreSQL, dan Google Sheets"""

    try:
        # Load to CSV
        print("\nLoading data to CSV...")
        store_to_csv(data)

        # Load to PostgreSQL
        print("\nLoading data to PostgreSQL...")
        store_to_postgre(data, db_url)

        # Load to Google Sheets
        print("\nLoading data to Google Sheets...")
        dataframe_to_sheets(data, sheet_name, gsheet_id)

        print("\nData berhasil diload ke semua target!")
    
    except Exception as e:
        print(f"Terjadi kesalahan saat memuat data: {e}")