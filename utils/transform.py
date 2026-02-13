import pandas as pd
import re
import datetime

def transform_to_DataFrame(data):
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error converting data to DataFrame: {e}")
        return pd.DataFrame()


def clean_price(price_str):
    if pd.isna(price_str) or 'Unavailable' in price_str:
        return None
    clean_str = re.sub(r'[^\d.]', '', str(price_str))
    try:
        return float(clean_str)
    except:
        return None
    

def clean_rating(rating_str):
    if pd.isna(rating_str) or 'Invalid' in str(rating_str):
        return 0.0
    try:
        clean_str = str(rating_str)
        if '/' in clean_str:
            clean_str = clean_str.split('/')[0]

        clean_str = re.sub(r'[^\d.]', '', clean_str)
        if not clean_str:
            return 0.0
            
        return float(clean_str)
    except:
        return 0.0
    

def transform_data(data, exchange_rate):
    try:
        if data.empty:
            print("Dataframe is empty, skipping transformation.")
            return data

        if 'Timestamp' not in data.columns:
            data['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = data.drop_duplicates()
        data = data[data['Title'] != 'Unknown Product']

        data['price_usd'] = data['Price'].apply(clean_price)
        data = data.dropna(subset=['price_usd'])

        data['price_rp'] = (data['price_usd'] * exchange_rate).astype(float)

        data['Rating'] = data['Rating'].apply(clean_rating)

        data['Colors'] = data['Colors'].astype(str).str.extract(r'(\d+)').astype('int64')

        data['Size'] = data['Size'].astype(str).str.replace('Size: ', '', regex=False)
        
        data['Gender'] = data['Gender'].astype(str).str.replace('Gender: ', '', regex=False)

        data = data.drop(columns=['Price', 'price_usd'])
        data = data.rename(columns={'price_rp': 'Price'})

        return data
        
    except Exception as e:
        print(f"An error occurred during data transformation: {e}")
        return pd.DataFrame()