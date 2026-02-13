import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import store_to_csv, store_to_postgre, store_to_googlesheets

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})


    @patch('utils.load.pd.DataFrame.to_csv')
    def test_store_to_csv(self, mock_to_csv):
        store_to_csv(self.df, 'dummy.csv')
        mock_to_csv.assert_called_once_with('dummy.csv', index=False)


    @patch('utils.load.create_engine')
    def test_store_to_postgre(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn
        
        store_to_postgre(self.df, 'postgresql://dummy')
        
        mock_engine.assert_called_once_with('postgresql://dummy')


    @patch('utils.load.build')
    @patch('utils.load.Credentials')
    def test_store_to_googlesheets(self, mock_build):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        store_to_googlesheets(self.df, 'dummy_key.json', 'dummy_spreadsheet_id')
        
        mock_service.spreadsheets.return_value.values.return_value.update.return_value.execute.assert_called_once()

    
    @patch('builtins.print') 
    @patch('utils.load.pd.DataFrame.to_csv')
    def test_store_to_csv_exception(self, mock_to_csv, mock_print):
        mock_to_csv.side_effect = Exception("Permission Denied")
        
        store_to_csv(self.df, 'dummy.csv')
        
        mock_print.assert_called_with("An error occurred while saving data to CSV: Permission Denied")

    
    @patch('builtins.print')
    @patch('utils.load.create_engine')
    def test_store_to_postgre_exception(self, mock_engine, mock_print):
        mock_engine.side_effect = Exception("Connection Failed")
        
        store_to_postgre(self.df, 'postgresql://dummy')
        
        mock_print.assert_called_with("An error occurred while saving data to PostgreSQL: Connection Failed")

    
    @patch('builtins.print')
    @patch('utils.load.build')
    @patch('utils.load.Credentials')
    def test_store_to_googlesheets_exception(self, mock_build, mock_print):
        mock_build.side_effect = Exception("API Error")
        
        store_to_googlesheets(self.df, 'dummy_key.json', 'dummy_spreadsheet_id')
    
        mock_print.assert_called_with("An error occurred while saving data to Google Sheets: API Error")
