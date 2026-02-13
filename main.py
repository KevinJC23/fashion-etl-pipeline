from utils.extract import scrape_fashion
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import store_to_csv, store_to_postgre, store_to_googlesheets

def main():
    BASE_URL = "https://fashion-studio.dicoding.dev/{}"
    all_fashion_product_data = scrape_fashion(BASE_URL)

    if all_fashion_product_data:
        try:
            df = transform_to_DataFrame(all_fashion_product_data)
            df_clean = transform_data(df, exchange_rate=16000)

            if not df_clean.empty:
                store_to_csv(df_clean, 'products.csv') 

                db_url = 'postgresql+psycopg2://developer:secretpassword@localhost:5432/fashion_db'
                store_to_postgre(df_clean, db_url)

                SPREADSHEET_ID = '1QQJRRQBveHhZbHXBmI-7rrbntI96tihOYoR5GYrTcIE'
                store_to_googlesheets(df_clean, 'google-sheets-api.json', SPREADSHEET_ID)
            else:
                print("No data available after transformation to store")

        except Exception as e:
            print(f"An error occurred in the ETL process: {e}")
    else:
        print("No data extracted from the source")

if __name__ == "__main__":
    main()