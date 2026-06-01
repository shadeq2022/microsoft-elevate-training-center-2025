import unittest
import pandas as pd
from utils.transform import (
    create_dataframe, clean_title, clean_price, clean_rating,
    clean_colors, clean_size, clean_gender, remove_duplicates,
    remove_nulls, fix_dtypes, transform,
)


SAMPLE_PRODUCTS = [
    {"Title": "T-shirt 2", "Price": "$102.15", "Rating": "Rating: ★ 3.9 / 5",
     "Colors": "3 Colors", "Size": "Size: M", "Gender": "Gender: Women",
     "timestamp": "2025-01-01T00:00:00"},
    {"Title": "Hoodie 3", "Price": "$496.88", "Rating": "Rating: ★ 4.8 / 5",
     "Colors": "3 Colors", "Size": "Size: L", "Gender": "Gender: Unisex",
     "timestamp": "2025-01-01T00:00:00"},
    {"Title": "Unknown Product", "Price": "$100.00", "Rating": "Invalid Rating / 5",
     "Colors": "5 Colors", "Size": "Size: M", "Gender": "Gender: Men",
     "timestamp": "2025-01-01T00:00:00"},
    {"Title": "Pants 4", "Price": "Price Unavailable", "Rating": "Rating: ★ 3.3 / 5",
     "Colors": "3 Colors", "Size": "Size: XL", "Gender": "Gender: Men",
     "timestamp": "2025-01-01T00:00:00"},
    {"Title": "T-shirt 2", "Price": "$102.15", "Rating": "Rating: ★ 3.9 / 5",
     "Colors": "3 Colors", "Size": "Size: M", "Gender": "Gender: Women",
     "timestamp": "2025-01-01T00:00:00"},  # duplikat
]


class TestCreateDataframe(unittest.TestCase):

    def test_returns_dataframe(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        self.assertIsInstance(df, pd.DataFrame)

    def test_correct_columns(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        for col in ["Title", "Price", "Rating", "Colors", "Size", "Gender", "timestamp"]:
            self.assertIn(col, df.columns)

    def test_empty_products_returns_none(self):
        result = create_dataframe([])
        self.assertIsNone(result)


class TestCleanTitle(unittest.TestCase):

    def test_removes_unknown_product(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        df = clean_title(df)
        self.assertNotIn("Unknown Product", df["Title"].values)


class TestCleanPrice(unittest.TestCase):

    def test_converts_to_rupiah(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        df = clean_title(df)  # hapus unknown dulu
        df = clean_price(df)
        # $102.15 * 16000 = 1634400.0
        self.assertIn(1634400.0, df["Price"].values)

    def test_removes_price_unavailable(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        df = clean_price(df)
        self.assertTrue(all(df["Price"] != "Price Unavailable"))


class TestCleanRating(unittest.TestCase):

    def test_rating_is_float(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        df = clean_title(df)
        df = clean_price(df)
        df = clean_rating(df)
        self.assertEqual(df["Rating"].dtype, float)

    def test_removes_invalid_rating(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        df = clean_rating(df)
        self.assertFalse(df["Rating"].str.contains("Invalid", na=False).any()
                         if df["Rating"].dtype == object else False)


class TestCleanColors(unittest.TestCase):

    def test_colors_is_int(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        df = clean_colors(df)
        self.assertTrue(pd.api.types.is_integer_dtype(df["Colors"]))

    def test_colors_value(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        df = clean_colors(df)
        self.assertIn(3, df["Colors"].values)


class TestCleanSize(unittest.TestCase):

    def test_removes_size_prefix(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        df = clean_size(df)
        self.assertFalse(df["Size"].str.startswith("Size:").any())


class TestCleanGender(unittest.TestCase):

    def test_removes_gender_prefix(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        df = clean_gender(df)
        self.assertFalse(df["Gender"].str.startswith("Gender:").any())


class TestRemoveDuplicates(unittest.TestCase):

    def test_removes_duplicates(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        before = len(df)
        df = remove_duplicates(df)
        self.assertLess(len(df), before)


class TestRemoveNulls(unittest.TestCase):

    def test_no_nulls_after(self):
        df = create_dataframe(SAMPLE_PRODUCTS)
        df = remove_nulls(df)
        self.assertFalse(df.isnull().any().any())


class TestTransform(unittest.TestCase):

    def test_full_pipeline_returns_dataframe(self):
        result = transform(SAMPLE_PRODUCTS)
        self.assertIsInstance(result, pd.DataFrame)

    def test_no_unknown_product_after_transform(self):
        result = transform(SAMPLE_PRODUCTS)
        self.assertNotIn("Unknown Product", result["Title"].values)

    def test_price_in_rupiah(self):
        result = transform(SAMPLE_PRODUCTS)
        self.assertTrue((result["Price"] > 1000).all())

    def test_transform_empty_returns_none(self):
        result = transform([])
        self.assertIsNone(result)

    def test_timestamp_column_exists(self):
        result = transform(SAMPLE_PRODUCTS)
        self.assertIn("timestamp", result.columns)