#******************************extract_product_csv_img.py********************************

import requests
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import re

def extract_review_rating(review_rating_class):
    rating_mapping = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    return rating_mapping.get(review_rating_class, None)

def extract_product_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_page_url = url
    upc = soup.find('th').find_next('td').text
    title = soup.find('h1').text.strip()
    price_including_tax = float(soup.find_all('th')[3].find_next('td').text.replace('Â','').replace('£', ''))
    price_excluding_tax = float(soup.find_all('th')[2].find_next('td').text.replace('Â','').replace('£', ''))
    number_available_text = soup.find_all('th')[5].find_next('td').text
    number_available = int(re.search(r'\b(\d+)\b', number_available_text).group())
    product_description = soup.find('meta', {'name': 'description'})['content']
    category = soup.select('ul.breadcrumb li')[2].text.strip()
    review_rating_class = soup.find('p', {'class': 'star-rating'})['class'][1]
    review_rating = extract_review_rating(review_rating_class)
    image_url = url.replace('index.html', '') + soup.find('img')['src']

    return product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url

def download_and_save_image(image_url, category, title):
    response = requests.get(image_url)
    if response.status_code == 200:
        category_dir = re.sub(r'\W', '_', category)
        os.makedirs('download/'+ category_dir, exist_ok=True)
        title_without_special_chars = re.sub(r'\W', '_', title.split(':')[0].strip())
        image_filename = os.path.join( 'download/'+category_dir, title_without_special_chars + '.jpeg')
        with open(image_filename, 'wb') as f:
            f.write(response.content)

product_url = input("Veuillez saisir l'URL du produit que vous souhaitez extraire : ")
product_data = extract_product_data(product_url)

columns = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
df = pd.DataFrame([product_data], columns=columns)

csv_folder = "download/CSV"
os.makedirs(csv_folder, exist_ok=True)

csv_filename = re.sub(r'\W', '_', product_data[2].split(':')[0].strip()) + '.csv'
csv_filepath = os.path.join(csv_folder, csv_filename)
df.to_csv(csv_filepath, index=False, encoding='utf-8')

download_and_save_image(product_data[-1], product_data[7], product_data[2])

print(f"Données extraites et enregistrées dans {csv_filepath}.")
print("Image téléchargée et enregistrée dans le répertoire de la catégorie.")

