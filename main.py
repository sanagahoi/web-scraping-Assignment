import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}"
def scrape_amazon_products(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    for product in soup.find_all('div', {'class': 's-result-item'}):
        product_info = {}
        try:
            product_info['url'] = "https://www.amazon.in" + product.find('a', {'class': 'a-link-normal'})['href']
            product_info['name'] = product.find('span', {'class': 'a-text-normal'}).text.strip()
            product_info['price'] = product.find('span', {'class': 'a-price-whole'}).text.strip()
            product_info['rating'] = product.find('span', {'class': 'a-icon-alt'}).text.strip()
            product_info['reviews'] = product.find('span', {'class': 'a-size-base'}).text.strip()
            products.append(product_info)
        except Exception as e:
            print("Error:", e)

    return products

total_pages = 20
all_products = []

for page in range(1, total_pages + 1):
    url = URL.format(page)
    products_on_page = scrape_amazon_products(url)
    all_products.extend(products_on_page)

def scrape_product_details(prod_url):
    response = requests.get(prod_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    prod_details = {}

    try:
        asin = soup.find('th', string='ASIN ')
        if asin:
            prod_details['asin'] = asin.find_next('td').text.strip()
        else:
            prod_details['asin'] = ""

        description = soup.find('div', {'id': 'productDescription'})
        prod_details['description'] = description.text.strip() if description else ''

        manufacturer = soup.find('th', string='Manufacturer')
        prod_details['manufacturer'] = manufacturer.find_next('td').text.strip() if manufacturer else ""

        prod_description = soup.find('div', {'id': 'detailBullets_feature_div'})
        prod_details['product_description'] = prod_description.text.strip() if prod_description else ''

    except Exception as e:
        print("Error --> ", e)

    return prod_details


# scrape details
for idx, product in enumerate(all_products, start=1):
    product_url = product['url']
    product_details = scrape_product_details(product_url)
    product.update(product_details)

# CSV file
with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as csvfile:

    fieldnames = list(all_products[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # data to CSV
    for product in all_products:
        writer.writerow(product)












