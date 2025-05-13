import pandas as pd
import re

def transform_to_DataFrame(data):
    """Mengubah data menjadi DataFrame"""
    df = pd.DataFrame(data)
    return df

def transform_data(data, exchange_rate):
    """Menggabungkan semua transformasi data menjadi satu fungsi"""

    # Menghapus baris unknown product
    data = data.loc[data["Product Title"] != "Unknown Product"].copy()

    # Transformasi Harga
    def clean_price(price_str):
        price_str = str(price_str).replace('$', '').strip()
        if 'Price not found' in price_str:
            return 0.0  # Set price to 0.0 if 'Price not found'
        try:
            return float(price_str)
        except Exception as e:
            print(f"Terjadi error pada transformasi harga: {e}")
            return 0.0

    # Menggunakan loc untuk menghindari SettingWithCopyWarning
    data.loc[:, 'Price_in_USD'] = data['Price'].apply(clean_price)

    # Transformasi exchange rate
    data.loc[:, 'Price_in_rupiah'] = data['Price_in_USD'] * exchange_rate

    # Transformasi Rating
    def clean_rating(rating_str):
        rating_str = str(rating_str).strip()
        if "⭐ Invalid Rating / 5" in rating_str or "Not Rated" in rating_str:
            return 0.0  
        try:
            return float(re.search(r"(\d+(\.\d+)?)", rating_str).group(1))
        except Exception as e:
            print(f"Terjadi error pada transformasi rating: {e}")
            return 0.0

    # Menggunakan loc untuk menghindari SettingWithCopyWarning
    data.loc[:, 'Rating'] = data['Rating'].apply(clean_rating)

    # Transformasi Colors
    def clean_colors(colors_str):
        colors_str = str(colors_str).strip()
        try:
            # Extract only numeric values, e.g., "10 Colors" or "5 options"
            colors = re.search(r"(\d+)", colors_str)
            return int(colors.group(1)) if colors else 0
        except Exception as e:
            print(f"Terjadi error pada transformasi Color: {e}")
            return 0

    # Menggunakan loc untuk menghindari SettingWithCopyWarning
    data.loc[:, 'Colors'] = data['Colors'].apply(clean_colors)

    # Menghapus kolom redundan karena harga sudah menjadi rupiah
    data.loc[:, "Price"] = data['Price_in_rupiah']
    data = data.drop(columns=['Price_in_USD', 'Price_in_rupiah'])

    return data
