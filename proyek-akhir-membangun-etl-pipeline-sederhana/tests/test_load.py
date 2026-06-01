import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql


SAMPLE_DF = pd.DataFrame({
    "Title": ["T-shirt 2", "Hoodie 3"],
    "Price": [1634400.0, 7950080.0],
    "Rating": [3.9, 4.8],
    "Colors": [3, 3],
    "Size": ["M", "L"],
    "Gender": ["Women", "Unisex"],
    "timestamp": ["2025-01-01T00:00:00", "2025-01-01T00:00:00"],
})


class TestLoadToCsv(unittest.TestCase):

    @patch("utils.load.pd.DataFrame.to_csv")
    def test_load_csv_success(self, mock_to_csv):
        result = load_to_csv(SAMPLE_DF, "test_products.csv")
        self.assertTrue(result)
        mock_to_csv.assert_called_once()

    def test_load_csv_empty_df_returns_false(self):
        result = load_to_csv(pd.DataFrame(), "test.csv")
        self.assertFalse(result)

    def test_load_csv_none_returns_false(self):
        result = load_to_csv(None, "test.csv")
        self.assertFalse(result)


class TestLoadToGoogleSheets(unittest.TestCase):

    @patch("utils.load.build")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_load_google_sheets_success(self, mock_creds, mock_build):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        (mock_service.spreadsheets().values().update()
         .execute.return_value) = {}

        result = load_to_google_sheets(SAMPLE_DF, "fake_id", "fake_creds.json")
        self.assertTrue(result)

    def test_load_google_sheets_empty_df(self):
        result = load_to_google_sheets(pd.DataFrame(), "fake_id")
        self.assertFalse(result)

    def test_load_google_sheets_none_df(self):
        result = load_to_google_sheets(None, "fake_id")
        self.assertFalse(result)


class TestLoadToPostgreSQL(unittest.TestCase):

    @patch("utils.load.create_engine")
    @patch("utils.load.pd.DataFrame.to_sql")
    def test_load_postgresql_success(self, mock_to_sql, mock_engine):
        mock_engine.return_value = MagicMock()
        result = load_to_postgresql(SAMPLE_DF, "postgresql://fake_url")
        self.assertTrue(result)

    def test_load_postgresql_empty_df(self):
        result = load_to_postgresql(pd.DataFrame(), "postgresql://fake_url")
        self.assertFalse(result)

    def test_load_postgresql_none_df(self):
        result = load_to_postgresql(None, "postgresql://fake_url")
        self.assertFalse(result)