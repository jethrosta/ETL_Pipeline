import csv
import pandas as pd

def store_to_csv(data):
    """Fungsi untuk menyimpan data ke dalam CSV"""
    try:
        # melihat apakah data berbentuk DataFrame atau tidak
        if not isinstance(data, pd.DataFrame):
            print("Data tidak berbentuk Dataframe. Mengonversi data ke Dataframe...")
            data = pd.DataFrame(data)
        # menyimpan data dengan format csv
        data.to_csv('Fashions_details_data.csv', index=False)
        print("Data berhasil disimpan dalam bentuk CSV!")
    except Exception as e:
        print("Terjadi masalah ketika menyimpan data dalam bentuk CSV: {e}")
    