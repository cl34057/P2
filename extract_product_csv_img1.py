#******************************extract_product_csv_img.py********************************

import requests
from bs4 import BeautifulSoup
import os
import csv
import pandas as pd
import re
# Fonction pour extraire la notation d'une revue à partir de la classe CSS
def extract_review_rating(review_rating_class):
    rating_mapping = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    return rating_mapping.get(review_rating_class, None)
# Fonction pour extraire les données d'un produit à partir de son URL
def extract_product_data(url):
    # Effectue une requête HTTP pour obtenir le contenu de la page
    response = requests.get(url)
    # Utilise BeautifulSoup pour analyser le contenu HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraction des informations du produit
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
# Fonction pour télécharger et enregistrer une image
def download_and_save_image(image_url, category, title):
    response = requests.get(image_url)
    if response.status_code == 200:
        # Crée un répertoire pour la catégorie et remplace les caractères spéciaux par '_'
        category_dir = re.sub(r'\W', '_', category)
        os.makedirs('download/'+ category_dir, exist_ok=True)
        # Remplace les caractères spéciaux dans le titre et crée le nom du fichier
        title_without_special_chars = re.sub(r'\W', '_', title.split(':')[0].strip())
        image_filename = os.path.join( 'download/'+category_dir, title_without_special_chars + '.jpeg')
        # Enregistre l'image dans le répertoire
        with open(image_filename, 'wb') as f:
            f.write(response.content)
            
# Saisie de l'URL du produit depuis l'utilisateur
product_url = input("Veuillez saisir l'URL du produit que vous souhaitez extraire : ")
# Extraction des données du produit
product_data = extract_product_data(product_url)

# Création d'un DataFrame pandas avec les données du produit
columns = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
df = pd.DataFrame([product_data], columns=columns)

# Création d'un répertoire "CSV" s'il n'existe pas
csv_folder = "download/CSV"
os.makedirs(csv_folder, exist_ok=True)

# Création d'un nom de fichier CSV à partir du titre du produit
csv_filename = re.sub(r'\W', '_', product_data[2].split(':')[0].strip()) + '.csv'
csv_filepath = os.path.join(csv_folder, csv_filename)
# Écriture des données dans le fichier CSV
df.to_csv(csv_filepath, index=False, encoding='utf-8')

# Téléchargement et enregistrement de l'image associée au produit
download_and_save_image(product_data[-1], product_data[7], product_data[2])

# Affichage de messages indiquant la fin du processus
print(f"Données extraites et enregistrées dans {csv_filepath}.")
print("Image téléchargée et enregistrée dans le répertoire de la catégorie.")

