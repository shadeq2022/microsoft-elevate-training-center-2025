import pandas as pd


EXCHANGE_RATE = 16000

DIRTY_PATTERNS = {
    "Title": ["Unknown Product"],
    "Rating": ["Invalid Rating / 5", "Not Rated"],
    "Price": ["Price Unavailable", None],
}


def create_dataframe(products):
    """Mengubah list dict menjadi DataFrame."""
    try:
        if not products:
            raise ValueError("Data produk kosong, tidak dapat membuat DataFrame.")
        df = pd.DataFrame(products)
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        return None


def clean_title(df):
    """Menghapus baris dengan title invalid atau null."""
    try:
        df = df[~df["Title"].isin(DIRTY_PATTERNS["Title"])]
        df = df[df["Title"].notna()]
        return df
    except Exception as e:
        print(f"Error cleaning Title: {e}")
        return df


def clean_price(df):
    """Konversi harga dari USD ke IDR, hapus nilai invalid."""
    try:
        # Hapus baris "Price Unavailable" dan null
        df = df[df["Price"] != "Price Unavailable"]
        df = df[df["Price"].notna()]
        # Ekstrak angka dari string seperti "$102.15"
        df["Price"] = df["Price"].str.replace(r"[^\d.]", "", regex=True)
        df = df[df["Price"] != ""]
        df["Price"] = df["Price"].astype(float) * EXCHANGE_RATE
        df["Price"] = df["Price"].round(2)  # ← tambahkan ini
        return df
    except Exception as e:
        print(f"Error cleaning Price: {e}")
        return df


def clean_rating(df):
    """Konversi Rating ke float, hapus nilai invalid."""
    try:
        # Hapus nilai invalid
        for pattern in DIRTY_PATTERNS["Rating"]:
            df = df[~df["Rating"].str.contains(pattern, na=True)]
        df = df[df["Rating"].notna()]
        # Ekstrak angka float dari "Rating: ★ 4.8 / 5"
        df["Rating"] = df["Rating"].str.extract(r"([\d.]+)").astype(float)
        return df
    except Exception as e:
        print(f"Error cleaning Rating: {e}")
        return df


def clean_colors(df):
    """Ekstrak angka dari kolom Colors, contoh: '3 Colors' → 3."""
    try:
        df = df[df["Colors"].notna()]
        df["Colors"] = df["Colors"].str.extract(r"(\d+)").astype(int)
        return df
    except Exception as e:
        print(f"Error cleaning Colors: {e}")
        return df


def clean_size(df):
    """Hapus prefix 'Size: ' dari kolom Size."""
    try:
        df = df[df["Size"].notna()]
        df["Size"] = df["Size"].str.replace(r"Size:\s*", "", regex=True).str.strip()
        return df
    except Exception as e:
        print(f"Error cleaning Size: {e}")
        return df


def clean_gender(df):
    """Hapus prefix 'Gender: ' dari kolom Gender."""
    try:
        df = df[df["Gender"].notna()]
        df["Gender"] = df["Gender"].str.replace(r"Gender:\s*", "", regex=True).str.strip()
        return df
    except Exception as e:
        print(f"Error cleaning Gender: {e}")
        return df


def remove_duplicates(df):
    """Menghapus baris duplikat."""
    try:
        before = len(df)
        df = df.drop_duplicates()
        print(f"Duplikat dihapus: {before - len(df)} baris")
        return df
    except Exception as e:
        print(f"Error removing duplicates: {e}")
        return df


def remove_nulls(df):
    """Menghapus baris dengan nilai null."""
    try:
        before = len(df)
        df = df.dropna()
        print(f"Null dihapus: {before - len(df)} baris")
        return df
    except Exception as e:
        print(f"Error removing nulls: {e}")
        return df


def fix_dtypes(df):
    """Memastikan tipe data sesuai ekspektasi."""
    try:
        df["Title"] = df["Title"].astype(str)
        df["Price"] = df["Price"].astype(float)
        df["Rating"] = df["Rating"].astype(float)
        df["Colors"] = df["Colors"].astype(int)
        df["Size"] = df["Size"].astype(str)
        df["Gender"] = df["Gender"].astype(str)
        return df
    except Exception as e:
        print(f"Error fixing dtypes: {e}")
        return df


def transform(products):
    """Menjalankan seluruh pipeline transformasi."""
    try:
        df = create_dataframe(products)
        if df is None:
            return None

        df = clean_title(df)
        df = clean_price(df)
        df = clean_rating(df)
        df = clean_colors(df)
        df = clean_size(df)
        df = clean_gender(df)
        df = remove_duplicates(df)
        df = remove_nulls(df)
        df = fix_dtypes(df)

        # Reset index
        df = df.reset_index(drop=True)
        print(f"\nTotal data setelah transformasi: {len(df)} baris")
        print(df.info())
        return df

    except Exception as e:
        print(f"Error during transformation: {e}")
        return None