import unittest
from unittest.mock import patch, Mock, MagicMock
from utils.extract import fetching_content, extract_fashion_data


class TestExtract(unittest.TestCase):

    @patch("utils.extract.requests.session")
    def test_fetching_content_success(self, mock_session):
        """Test fetching_content dengan respons sukses (200 OK)."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body>Test Content</body></html>"

        mock_session_instance = mock_session.return_value
        mock_session_instance.get.return_value = mock_response
        
        result = fetching_content("http://example.com")
        self.assertIsNotNone(result)
        self.assertEqual(result, b"<html><body>Test Content</body></html>")

    
    @patch("builtins.print")  # Mempatch print untuk menangkap output
    @patch("utils.extract.requests.session")  # Mempatch session
    def test_fetching_content_failure(self, mock_session, mock_print):
        """Test fetching_content ketika terjadi Exception."""
        # Simulasikan error HTTP 404
        from requests.exceptions import HTTPError

        mock_session_instance = mock_session.return_value
        mock_session_instance.get.side_effect = HTTPError("404 Client Error: Not Found")

        result = fetching_content("http://example.com")

        # Periksa apakah print dipanggil dengan pesan yang benar
        mock_print.assert_called_with("Terjadi kesalahan ketika melakukan request terhadap http://example.com: 404 Client Error: Not Found")

        # Pastikan hasilnya adalah None
        self.assertIsNone(result)
    
    def test_extract_fashion_data(self):
        """Test extract_fashion_data dengan konten HTML yang disimulasikan."""
        class MockArticle:
            def find(self, tag, **kwargs):
                if tag == 'h3':
                    return MagicMock(text="Test Product")
                elif tag == 'div' and kwargs.get('class_') == 'price-container':
                    return MagicMock(find=lambda x, **kwargs: MagicMock(text="$100") if x == 'span' else None)
                

            def find_all(self, tag):
                if tag == 'p':
                    return [
                        MagicMock(get_text=lambda strip: "Rating: ⭐ 4.8 / 5"),
                        MagicMock(get_text=lambda strip: "3 Colors"),
                        MagicMock(get_text=lambda strip: "Size: M"),
                        MagicMock(get_text=lambda strip: "Gender: Female"),
                    ]

        article = MockArticle()
        result = extract_fashion_data(article)

        # Assertion
        self.assertEqual(result["Product Title"], "Test Product")
        self.assertEqual(result["Price"], "$100")
        self.assertEqual(result["Rating"], "⭐ 4.8 / 5")
        self.assertEqual(result["Colors"], "3 Colors")
        self.assertEqual(result["Size"], "M")
        self.assertEqual(result["Gender"], "Female")



if __name__ == "__main__":
    unittest.main()
