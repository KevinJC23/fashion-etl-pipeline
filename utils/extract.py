import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}


def fetching_content(url):
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making a request to {url}: {e}")
        return None


def extract_fashion_product_data(div):
    try:
        fashion_title = div.find('h3', class_='product-title')
        title = fashion_title.get_text(strip=True) if fashion_title else None

        fashion_price = div.find('span', class_='price')
        price = fashion_price.get_text(strip=True) if fashion_price else "No Price"

        rating = colors = size = gender = None
        tags = div.find_all('p')
        for p in tags:
            text = p.text.strip()
            if 'Rating' in text:
                temp = text.replace('Rating', '').replace(':', '').strip()
                rating = temp.split('/')[0].strip()
            elif 'Colors' in text:
                colors = text
            elif 'Size' in text:
                size = text.split('Size:')[1].strip()
            elif 'Gender' in text:
                gender = text.split('Gender:')[1].strip()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        product = {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,   
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp,
        }

        return product
    
    except Exception as e:
        print(f"Error extracting product data: {e}")
        return None


def scrape_fashion(base_url, start_page=1, delay=2):
    data = []
    page_num = start_page

    while True:
        curr_path = f"page{page_num}" if page_num > 1 else ""

        url = base_url.format(curr_path)
        print(f"Scraping page: {url}")

        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            articles_element = soup.find_all('div', class_='collection-card')
            for article in articles_element:
                product = extract_fashion_product_data(article)
                if product: 
                    data.append(product)

            next_page = soup.find('li', class_='next')
            if next_page and next_page.find('a', href=True):
                page_num += 1
                time.sleep(delay)
            else:
                break
        else:
            break

    return data