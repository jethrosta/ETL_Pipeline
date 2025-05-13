from sqlalchemy import create_engine

def store_to_postgre(data, db_url):
    """Fungsi untuk menyimpan data ke dalam PostgreSQL"""
    try:
        # membuat engine database
        engine = create_engine(db_url)

        # menyimpan data ke tabel 'fashiondb' jika tabel sudah ada, data akan ditambahkan (apend)
        with engine.connect() as con:
            data.to_sql('fashiondb', con=con, if_exists='append', index=False)
            print("Data berhasil ditambahkan ke data base!")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")