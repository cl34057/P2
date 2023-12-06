
#*******************extract_products_categorys_csv_img.py**************************


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
    print(f"Image téléchargée et enregistrée: {filename}")
    
# Fonction pour obtenir un nom de fichier valide
def get_valid_filename(title):
    clean_title = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    return clean_title.strip()

# Base URL du site
base_url = 'http://books.toscrape.com/'
output_folder = 'download/Images'
csv_folder = 'download/CSV'

# Créer un répertoire pour les fichiers CSV
os.makedirs(csv_folder, exist_ok=True)

#convertir des classes de notation textuelles en valeurs numériques correspondantes.
def extract_review_rating(review_rating_class):
    rating_mapping = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    return rating_mapping.get(review_rating_class, None)

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
        number_available_text = soup.find('th', string='Availability').find_next('td').text
        number_available = int(re.search(r'\b(\d+)\b', number_available_text).group())
        product_description = soup.find('meta', {'name': 'description'})['content']
        review_rating_class = soup.find('p', {'class': 'star-rating'})['class'][1]
        review_rating = extract_review_rating(review_rating_class)
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
        print(f'Erreur {response.status_code} pendant la requête{product_url}')
        
# Fonction pour extraire les URLs de tous les produits dans une catégorie
def extract_all_product_urls(category_url):
    all_urls = []
    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Trouver toutes les balises <h3> qui contiennent les liens vers les pages de produits
        product_links = soup.select('h3 a')
        # Construire la liste complète des URLs des produits
        base_url = 'https://books.toscrape.com/catalogue/'
        product_urls = [base_url + link['href'][9:] for link in product_links]
        all_urls.extend(product_urls)
        
        # Extraire l'URL de la page suivante
        next_page = soup.find('li', class_='next')
        if next_page:
            category_url = category_url.rsplit('/', 1)[0] + '/' + next_page.a['href']
        else:
            break
    
    return all_urls
# Obtenir la page d'accueil
response = requests.get(base_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # Trouver toutes les catégories
    categories = soup.select('div.side_categories ul.nav-list li ul li a')
    
    for category in categories:
        category_url = base_url + category['href']
        category_name = category.text.strip()
        print(f'Exploration de la catégorie: {category_name}...')
         # Créer un répertoire pour la catégorie
        os.makedirs(os.path.join(output_folder, category_name), exist_ok=True)
         # Extraire les données de tous les produits de la catégorie
        product_urls = extract_all_product_urls(category_url)

        for product_url in product_urls:
            extract_product_info(product_url, category_name)
else:
    print(f'Erreur {response.status_code} pendant la requête {base_url}')
