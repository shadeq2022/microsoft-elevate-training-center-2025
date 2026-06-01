import pandas as pd
from sqlalchemy import create_engine
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


# ── CSV ──────────────────────────────────────────────────────────────────────

def load_to_csv(df, filepath="products.csv"):
    """Menyimpan DataFrame ke berkas CSV."""
    try:
        if df is None or df.empty:
            raise ValueError("DataFrame kosong, tidak dapat disimpan ke CSV.")
        df.to_csv(filepath, index=False)
        print(f"Data berhasil disimpan ke CSV: {filepath}")
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False


# ── Google Sheets ─────────────────────────────────────────────────────────────

def load_to_google_sheets(df, spreadsheet_id, credentials_file="google-sheets-api.json"):
    """Menyimpan DataFrame ke Google Sheets."""
    try:
        if df is None or df.empty:
            raise ValueError("DataFrame kosong, tidak dapat disimpan ke Google Sheets.")

        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        service = build("sheets", "v4", credentials=creds)

        # Siapkan data: header + rows
        values = [df.columns.tolist()] + df.astype(str).values.tolist()
        body = {"values": values}

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A1",
            valueInputOption="RAW",
            body=body,
        ).execute()

        print(f"Data berhasil disimpan ke Google Sheets (ID: {spreadsheet_id})")
        return True
    except Exception as e:
        print(f"Error saving to Google Sheets: {e}")
        return False


# ── PostgreSQL ────────────────────────────────────────────────────────────────

def load_to_postgresql(df, db_url, table_name="products"):
    """Menyimpan DataFrame ke PostgreSQL."""
    try:
        if df is None or df.empty:
            raise ValueError("DataFrame kosong, tidak dapat disimpan ke PostgreSQL.")

        engine = create_engine(db_url)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"Data berhasil disimpan ke PostgreSQL (tabel: {table_name})")
        return True
    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")
        return False