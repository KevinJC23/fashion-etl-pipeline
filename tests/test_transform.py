import unittest
import pandas as pd
import numpy as np
from utils.transform import transform_to_DataFrame, clean_price, clean_rating, transform_data

class TestTransform(unittest.TestCase):
    def test_transform_to_dataframe(self):
        data = [{'Title': 'A', 'Price': '10'}]
        df = transform_to_DataFrame(data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        
        df_error = transform_to_DataFrame(None)
        self.assertTrue(df_error.empty)

    
    def test_transform_to_dataframe_exception(self):
        res = transform_to_DataFrame(12345)
        self.assertTrue(res.empty)


    def test_clean_price(self):
        self.assertEqual(clean_price("$10.50"), 10.5)
        self.assertEqual(clean_price("IDR 100000"), 100000.0)
        self.assertIsNone(clean_price("Unavailable"))
        self.assertIsNone(clean_price(None))
        self.assertIsNone(clean_price(np.nan))


    def test_clean_price_exception(self):
        self.assertIsNone(clean_price("10.5.5"))
        self.assertIsNone(clean_price("."))


    def test_clean_rating(self):
        self.assertEqual(clean_rating("Rating: 4.5 / 5"), 4.5)
        self.assertEqual(clean_rating("4.8"), 4.8)
        self.assertEqual(clean_rating("Invalid Rating"), 0.0)
        self.assertEqual(clean_rating(None), 0.0)
        self.assertEqual(clean_rating("Rating: / 5"), 0.0) 
    

    def test_clean_rating_exception(self):
        self.assertEqual(clean_rating("Rating: ."), 0.0)


    def test_transform_data_logic(self):
        raw_data = [
            {
                'Title': 'Valid Product', 
                'Price': '$10.00', 
                'Rating': 'Rating: 5.0 / 5', 
                'Colors': '3 Colors', 
                'Size': 'Size: M', 
                'Gender': 'Gender: Men', 
                'Timestamp': '2026-01-01'
            },
            {
                'Title': 'Unknown Product', 
                'Price': '$100.00', 
                'Rating': 'Invalid', 
                'Colors': '5 Colors', 
                'Size': 'M', 
                'Gender': 'Men', 
                'Timestamp': '2026-01-01'
            },
            {
                'Title': 'No Price', 
                'Price': 'Unavailable', 
                'Rating': '4.0', 
                'Colors': '1', 
                'Size': 'S', 
                'Gender': 'Women', 
                'Timestamp': '2026-01-01'
            }
        ]
        
        df_raw = pd.DataFrame(raw_data)
        df_clean = transform_data(df_raw, exchange_rate=16000)

        self.assertEqual(len(df_clean), 1)
        
        self.assertEqual(df_clean.iloc[0]['Price'], 160000.0)
        
        self.assertEqual(df_clean.iloc[0]['Colors'], 3.0) 
        self.assertEqual(df_clean.iloc[0]['Size'], 'M')
        self.assertEqual(df_clean.iloc[0]['Gender'], 'Men')
        
        self.assertIn('Timestamp', df_clean.columns)


    def test_transform_data_empty(self):
        df = transform_data(pd.DataFrame(), 16000)
        self.assertTrue(df.empty)

    
    def test_transform_data_missing_column_exception(self):
        df_bad = pd.DataFrame([{'Title': 'Shirt', 'Rating': '5.0'}]) 
        
        res = transform_data(df_bad, 16000)
        self.assertTrue(res.empty)