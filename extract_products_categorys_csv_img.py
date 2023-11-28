#******III-Extraction des caracteristiques de tous les produits de toutes les categories*****************
#*************************et Telechargement et enregistrement des fichiers images de tout ces produits***

#****************************extract_products_categorys_csv_img.py***************************************

# Fonction pour télécharger et enregistrer une image
# Fonction pour obtenir un nom de fichier valide
# URL de base du site 
# Créer un répertoire pour les fichiers CSV
# Fonction pour extraire les informations produit d'une page produit
    # Créez un DataFrame avec les informations sur le produit
    # Écrivez le DataFrame dans un fichier CSV dans le répertoire "CSV"
    # Téléchargez et enregistrez l'image dans le répertoire des catégories
# Obtenir la page d'accueil
     # Trouver toutes les catégories
        # Créer un répertoire pour la catégorie
        # Accéder à la page catégorie
        # Retrouvez tous les produits de la catégorie
        
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

# Fonction pour télécharger et enregistrer une image
def download_image(url, folder_path, title):
    response = requests.get(url, stream=True)
    filename = os.path.join(folder_path, get_valid_filename(title) + ".jpeg")
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    print(f"Image downloaded and saved: {filename}")

# Fonction pour obtenir un nom de fichier valide
def get_valid_filename(title):
    clean_title = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    return clean_title.strip()

# Base URL du site
base_url = 'http://books.toscrape.com/'
output_folder = 'output'
csv_folder = 'CSV'

# Créer un répertoire pour les fichiers CSV
os.makedirs(csv_folder, exist_ok=True)


# Fonction pour extraire les informations produit d'une page produit
def extract_product_info(product_url, category):
    response = requests.get(product_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        product_page_url = product_url
        upc = soup.find('th', string='UPC').find_next('td').text
        title = soup.find('h1').text
        price_including_tax = soup.find('th', string='Price (incl. tax)').find_next('td').text.replace('Â','')
        price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next('td').text.replace('Â','')
        number_available = soup.find('th', string='Availability').find_next('td').text
        product_description = soup.find('meta', {'name': 'description'})['content']
        review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
        image_url = base_url + soup.find('img')['src']

       
        # Créez un DataFrame avec les informations sur le produit
        df = pd.DataFrame({
            'product_page_url': [product_page_url],
            'upc': [upc],
            'title': [title],
            'price_including_tax': [price_including_tax],
            'price_excluding_tax': [price_excluding_tax],
            'number_available': [number_available],
            'product_description': [product_description],
            'category': [category],
            'review_rating': [review_rating],
            'image_url': [image_url]
        })

        # Écrivez le DataFrame dans un fichier CSV dans le répertoire "CSV"
        csv_filename = os.path.join(csv_folder, f'{category}.csv')
        df.to_csv(csv_filename, index=False, mode='a', header=not os.path.exists(csv_filename), encoding='utf-8')

        # Téléchargez et enregistrez l'image dans le répertoire des catégories
        download_image(image_url, os.path.join(output_folder, category), title)
    else:
        print(f'Error {response.status_code} while requesting {product_url}')


# Obtenir la page d'accueil
response = requests.get(base_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trouver toutes les catégories
    categories = soup.select('div.side_categories ul.nav-list li ul li a')
    
    for category in categories:
        category_url = base_url + category['href']
        category_name = category.text.strip()
        print(f'Exploring category: {category_name}...')
        
        # Créer un répertoire pour la catégorie
        os.makedirs(os.path.join(output_folder, category_name), exist_ok=True)

        # Accéder à la page catégorie
        category_response = requests.get(category_url)
        
        if category_response.status_code == 200:
            category_soup = BeautifulSoup(category_response.text, 'html.parser')
            
            # Retrouvez tous les produits de la catégorie
            product_links = category_soup.select('h3 a')
            
            for product_link in product_links:
                product_url = base_url + 'catalogue' + product_link['href'][8:]
                extract_product_info(product_url, category_name)
        
        else:
            print(f'Error {category_response.status_code} while requesting {category_url}')
else:
    print(f'Error {response.status_code} while requesting {base_url}')