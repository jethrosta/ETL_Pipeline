import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
# from utils.transform import transform_data, transform_to_DataFrame
# from load_package.store_to_db import store_to_postgre
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    try:
        session = requests.session()
        response = session.get(url)
        return response.content
    except Exception as e:
        print(f"Terjadi kesalahan ketika melakukan request terhadap {url}: {e}")
        return None  # Pastikan baris ini dieksekusi

    
def extract_fashion_data(article):
    """Mengambil data fashion berupa Nama Produk, Harga Produk, Rating, Jumlah Warna, Ukuran, Gender baju"""
    # Inisialisasi variabel dengan nilai default
    product_title = "Unknown"
    price = "Price not found"
    rating = "Rating not found"
    colors = "Colors not found"
    sizes = "Sizes not found"
    gender = "Gender not found"
    
    # Mengambil judul produk fashion
    product_title_element = article.find('h3')
    if product_title_element:
        product_title = product_title_element.text.strip()

    # Mengambil harga produk
    price_element = article.find('div', class_='price-container')
    if price_element:
        price_span = price_element.find('span', class_='price')
        if price_span:
            price = price_span.text.strip()

    # Mengambil informasi lainnya (Rating, Colors, Size, Gender)
    p_elements = article.find_all('p')
    for p in p_elements:
        text = p.get_text(strip=True)

        if "Rating:" in text:
            rating = text.replace("Rating:", "").strip()
        elif "Colors" in text:
            colors = text.strip()
        elif "Size:" in text:
            sizes = text.replace("Size:", "").strip()
        elif "Gender:" in text:
            gender = text.replace("Gender:", "").strip()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # Membuat dictionary untuk hasil
    fashions = {
        "Product Title": product_title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": sizes,
        "Gender": gender,
        "Timestamp": timestamp
    }
    return fashions

def extract_data(base_url, start_page = 1, max_pages = 50, delay = 2):
    """Fungsi utama untuk mengambil keseluruhan data fashion mulai dari request hingga menyimpannya dalam variabel data disetiap page"""
    data = []
    page_number = start_page

    while True:
        if page_number == 1:
            url = base_url # halaman pertama
        else:
            url = f"{base_url}page{page_number}"

        print(f"Scraping halaman: {url}")

        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            articles_element = soup.find_all('div', class_='collection-card')
            
            # jika tidak ada artikel yang ditemukan, hentikan scraping
            if not articles_element:
                print(f"Tidak ada artikel pada halaman {page_number}. Scraping dihentikan!")
                break

            for article in articles_element:
                fashion = extract_fashion_data(article)
                data.append(fashion)

            # cek apakah page sudah mencapai batas
            if page_number >= max_pages:
                print(f"Mencapai batas halaman {max_pages}. Scraping berhenti!")
                break

            next_button = soup.find('li', class_='page-item next')
            if next_button:
                page_number += 1
                time.sleep(delay)
            else:
                break
        
        else:
            break
    
    return data

# def extract_and_transform(base_url):
#     data = extract(base_url)
#     if data:
#         df = transform_to_DataFrame(data)
#         df = transform_data(df, exchange_rate=16000)
#         return df
#     else:
#         print("Tidak ada data yang ditemukan")
#         return pd.DataFrame()

# if __name__ == "__main__":
#     BASE_URL = 'https://fashion-studio.dicoding.dev/'
#     fashion_data = extract_and_transform(BASE_URL)
#     print(fashion_data.info())