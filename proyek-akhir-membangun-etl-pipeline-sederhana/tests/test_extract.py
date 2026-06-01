import unittest
from unittest.mock import patch, Mock, MagicMock
from utils.extract import fetch_page, parse_products, scrape_main


MOCK_HTML = b"""
<html><body>
  <div class="collection-card">
    <div class="product-details">
      <h3 class="product-title">T-shirt 2</h3>
      <div class="price-container">
        <span class="price">$102.15</span>
      </div>
      <p style="font-size: 14px; color: #777;">Rating: &#9733; 3.9 / 5</p>
      <p style="font-size: 14px; color: #777;">3 Colors</p>
      <p style="font-size: 14px; color: #777;">Size: M</p>
      <p style="font-size: 14px; color: #777;">Gender: Women</p>
    </div>
  </div>
</body></html>
"""


class TestFetchPage(unittest.TestCase):

    @patch("utils.extract.requests.Session")
    def test_fetch_page_success(self, mock_session_class):
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html></html>"
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        result = fetch_page("https://example.com")
        self.assertEqual(result, b"<html></html>")

    @patch("utils.extract.requests.Session")
    def test_fetch_page_request_exception(self, mock_session_class):
        import requests
        mock_session = Mock()
        mock_session.get.side_effect = requests.exceptions.RequestException("Connection error")
        mock_session_class.return_value = mock_session

        result = fetch_page("https://example.com")
        self.assertIsNone(result)

    @patch("utils.extract.requests.Session")
    def test_fetch_page_with_session(self, mock_session_class):
        mock_session = Mock()
        mock_response = Mock()
        mock_response.content = b"<html>ok</html>"
        mock_session.get.return_value = mock_response

        result = fetch_page("https://example.com", session=mock_session)
        self.assertEqual(result, b"<html>ok</html>")


class TestParseProducts(unittest.TestCase):

    def test_parse_products_returns_list(self):
        result = parse_products(MOCK_HTML, "2025-01-01T00:00:00")
        self.assertIsInstance(result, list)

    def test_parse_products_correct_fields(self):
        result = parse_products(MOCK_HTML, "2025-01-01T00:00:00")
        self.assertTrue(len(result) > 0)
        product = result[0]
        self.assertIn("Title", product)
        self.assertIn("Price", product)
        self.assertIn("Rating", product)
        self.assertIn("Colors", product)
        self.assertIn("Size", product)
        self.assertIn("Gender", product)
        self.assertIn("timestamp", product)

    def test_parse_products_empty_html(self):
        result = parse_products(b"<html></html>", "2025-01-01T00:00:00")
        self.assertEqual(result, [])

    def test_parse_products_title_value(self):
        result = parse_products(MOCK_HTML, "2025-01-01T00:00:00")
        self.assertEqual(result[0]["Title"], "T-shirt 2")


class TestScrapeMain(unittest.TestCase):

    @patch("utils.extract.fetch_page")
    @patch("utils.extract.parse_products")
    def test_scrape_main_returns_list(self, mock_parse, mock_fetch):
        mock_fetch.return_value = b"<html></html>"
        mock_parse.return_value = [{"Title": "T-shirt", "Price": "$10.00",
                                    "Rating": "4.0 / 5", "Colors": "3 Colors",
                                    "Size": "M", "Gender": "Men",
                                    "timestamp": "2025-01-01"}]
        result = scrape_main(total_pages=1)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    @patch("utils.extract.fetch_page")
    def test_scrape_main_fetch_returns_none(self, mock_fetch):
        mock_fetch.return_value = None
        result = scrape_main(total_pages=1)
        # Tetap mengembalikan list kosong (halaman dilewati)
        self.assertIsInstance(result, list)