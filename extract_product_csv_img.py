#************I-Caractéristiques d'un produit d'une page dans un rep pour l'image et repertoire pour le csv******

# Fonction pour extraire les données d'une page de produit
#  Fonction pour télécharger et enregistrer l'image
# URL de la page produit que vous souhaitez extraire
# Créer un DataFrame pandas pour mieux organiser les données
# Créer un répertoire "CSV" s'il n'existe pas
# Créer un fichier CSV avec le nom du titre avant les deux-points (:)
# Écrire les données dans le fichier CSV en ajustant la largeur des colonnes
# Télécharger et enregistrer l'image dans le répertoire de la catégorie

#****************************extract_product_csv_img.py***************************************************

import requests
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd

# Fonction pour extraire les données d'une page produit
def extract_product_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_page_url = url
        
    upc = soup.find('th').find_next('td').text
    title = soup.find('h1').text.strip()
    price_including_tax = soup.find_all('th')[3].find_next('td').text.replace('Â','')
    price_excluding_tax = soup.find_all('th')[2].find_next('td').text.replace('Â','')
    number_available = soup.find_all('th')[5].find_next('td').text
    product_description = soup.find('meta', {'name': 'description'})['content']
    category = soup.select('ul.breadcrumb li')[2].text.strip()
    review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
    image_url = url.replace('index.html', '') + soup.find('img')['src']

    return product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url

# Fonction pour télécharger et enregistrer l'image
def download_and_save_image(image_url, category, title):
    response = requests.get(image_url)
    if response.status_code == 200:
        category_dir = category.replace(" ", "_")
        os.makedirs(category_dir, exist_ok=True)
        image_filename = os.path.join(category_dir, title.split(':')[0].strip() + '.jpeg')
        with open(image_filename, 'wb') as f:
            f.write(response.content)

# URL de la page produit que vous souhaitez extraire
product_url = 'https://books.toscrape.com/catalogue/the-requiem-red_995/index.html'

product_data = extract_product_data(product_url)

# Créer un DataFrame pandas pour mieux organiser les données
columns = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
df = pd.DataFrame([product_data], columns=columns)

# Créer un répertoire "CSV" s'il n'existe pas
csv_folder = "CSV"
os.makedirs(csv_folder, exist_ok=True)

# Créer un fichier CSV avec le nom du titre avant les deux-points (:)
csv_filename = product_data[2].split(':')[0].strip() + '.csv'

# Écrire les données dans le fichier CSV en ajustant la largeur des colonnes
csv_filepath = os.path.join(csv_folder, csv_filename)
df.to_csv(csv_filepath, index=False, encoding='utf-8')

# Télécharger et enregistrer l'image dans le répertoire de la catégorie
download_and_save_image(product_data[-1], product_data[7], product_data[2])

print(f"Données extraites et enregistrées dans {csv_filepath}.")
print("Image téléchargée et enregistrée dans le répertoire de la catégorie.")
