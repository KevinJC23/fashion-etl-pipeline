import unittest
import requests
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from utils.extract import fetching_content, extract_fashion_product_data, scrape_fashion

class TestExtract(unittest.TestCase):
    @patch('utils.extract.requests.Session')
    def test_fetching_content_success(self, mock_session):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>Success</html>"
        
        mock_session_instance = mock_session.return_value
        mock_session_instance.get.return_value = mock_response

        result = fetching_content("http://dummy.url")
        self.assertEqual(result, "<html>Success</html>")


    @patch('utils.extract.requests.Session')
    def test_fetching_content_failure(self, mock_session):
        mock_session_instance = mock_session.return_value
        mock_session_instance.get.side_effect = requests.exceptions.RequestException("Network Error")

        result = fetching_content("http://dummy.url")
        self.assertIsNone(result)


    def test_extract_product_data_valid(self):
        html = """
        <div class="collection-card">
            <h3 class="product-title">Test Product</h3>
            <span class="price">$10.00</span>
            <p>Rating: 4.5 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Men</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div')
        
        result = extract_fashion_product_data(div)
        
        self.assertEqual(result['Title'], "Test Product")
        self.assertEqual(result['Price'], "$10.00")
        self.assertEqual(result['Rating'], "4.5") 
        self.assertEqual(result['Colors'], "3 Colors")
        self.assertEqual(result['Size'], "M")
        self.assertEqual(result['Gender'], "Men")
        self.assertIsNotNone(result['Timestamp'])


    def test_extract_product_data_incomplete(self):
        html = """
        <div class="collection-card">
            <h3 class="product-title">No Price Item</h3>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div')
        
        result = extract_fashion_product_data(div)
        
        self.assertEqual(result['Title'], "No Price Item")
        self.assertEqual(result['Price'], "No Price")
        self.assertIsNone(result['Rating'])

    
    def test_extract_product_data_exception(self):
        result = extract_fashion_product_data(None)
    
        self.assertIsNone(result)


    @patch('utils.extract.fetching_content')
    def test_scrape_fashion_pagination(self, mock_fetch):
        html_page_1 = """
        <html>
            <div class="collection-card"><h3 class="product-title">Prod 1</h3></div>
            <li class="next"><a href="page2">Next</a></li>
        </html>
        """
        
        html_page_2 = """
        <html>
            <div class="collection-card"><h3 class="product-title">Prod 2</h3></div>
            </html>
        """
        
        mock_fetch.side_effect = [html_page_1, html_page_2]
        data = scrape_fashion("http://url/{}", start_page=1, delay=0)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['Title'], "Prod 1")
        self.assertEqual(data[1]['Title'], "Prod 2")

    
    @patch('utils.extract.fetching_content')
    def test_scrape_fashion_content_none(self, mock_fetch):
        mock_fetch.return_value = None
        data = scrape_fashion("http://dummy.url/{}", start_page=1)
        
        self.assertEqual(data, [])