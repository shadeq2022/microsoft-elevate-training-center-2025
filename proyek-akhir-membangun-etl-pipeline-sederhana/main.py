import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from utils.extract import scrape_main
from utils.transform import transform
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql

load_dotenv()  # baca file .env

DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", ""))

# ── Konfigurasi ─────────────────────────────────
SPREADSHEET_ID = "1eZu078_cjVJnYFIfZtNts9YiUVKYntoQhUhB7onyMaE"
CREDENTIALS_FILE = "google-sheets-api.json"
DB_URL = f"postgresql+psycopg2://postgres:{DB_PASSWORD}@localhost:5432/fashion_db"
CSV_PATH = "products.csv"

def main():
    print("=" * 50)
    print("ETL Pipeline — Fashion Studio Scraper")
    print("=" * 50)

    # 1. EXTRACT
    print("\n[1/3] EXTRACT: Memulai scraping...")
    raw_data = scrape_main()
    if raw_data is None:
        print("Ekstraksi gagal. Pipeline dihentikan.")
        return

    # 2. TRANSFORM
    print("\n[2/3] TRANSFORM: Memulai transformasi data...")
    clean_df = transform(raw_data)
    if clean_df is None:
        print("Transformasi gagal. Pipeline dihentikan.")
        return

    # 3. LOAD
    print("\n[3/3] LOAD: Menyimpan data...")
    load_to_csv(clean_df, CSV_PATH)
    load_to_google_sheets(clean_df, SPREADSHEET_ID, CREDENTIALS_FILE)
    load_to_postgresql(clean_df, DB_URL)

    print("\n✅ ETL Pipeline selesai!")


if __name__ == "__main__":
    main()