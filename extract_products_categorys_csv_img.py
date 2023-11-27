# Fonction pour télécharger une image et l'enregistrer
    # Extraire le nom de fichier de l'URL de l'image
    # Enregistrement de l'image
# Fonction pour obtenir un nom de fichier valide
# URL de la page d'accueil du site "Books to Scrape"
# URL de la page d'accueil du site "Books to Scrape"
# Créer un répertoire pour les fichiers CSV
# Fonction pour extraire les informations d'une page de produit
    # Créer un DataFrame pandas avec les informations du produit
    # Écrire les informations dans le fichier CSV du répertoire "CSV"
        # Ajouter la ligne au fichier CSV existant
        # Créer un nouveau fichier CSV avec l'en-tête
    # Télécharger et enregistrer l'image dans le répertoire de la catégorie
# Récupérez la page d'accueil
    # Trouvez toutes les catégories
        # Créez un répertoire pour la catégorie
        # Accédez à la page de la catégorie
            # Trouvez tous les produits dans la catégorie
            
#*************extract_products_categorys_csv_img.py*********************
import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd

# Fonction pour télécharger une image et l'enregistrer
def download_image(url, folder_path, title):
    response = requests.get(url, stream=True)
    
    # Extraire le nom de fichier de l'URL de l'image
    filename = os.path.join(folder_path, get_valid_filename(title) + ".jpeg")
    
    # Enregistrement de l'image
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)
    print(f"Image téléchargée et enregistrée : {filename}")

# Fonction pour obtenir un nom de fichier valide
def get_valid_filename(title):
    clean_title = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    return clean_title.strip()

# URL de la page d'accueil du site "Books to Scrape"
base_url = 'http://books.toscrape.com/'
output_folder = 'output'
csv_folder = 'CSV'

# Créer un répertoire pour les fichiers CSV
os.makedirs(csv_folder, exist_ok=True)

# Fonction pour extraire les informations d'une page de produit
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

        # Créer un DataFrame pandas avec les informations du produit
        columns = [
            'product_page_url', 'upc', 'title', 'price_including_tax',
            'price_excluding_tax', 'number_available', 'product_description',
            'category', 'review_rating', 'image_url'
        ]
        product_data = pd.DataFrame([[
            product_page_url, upc, title, price_including_tax,
            price_excluding_tax, number_available, product_description,
            category, review_rating, image_url
        ]], columns=columns)

        # Écrire les informations dans le fichier CSV du répertoire "CSV"
        csv_filename = os.path.join(csv_folder, f'{category}.csv')
        if os.path.exists(csv_filename):
            # Ajouter la ligne au fichier CSV existant
            product_data.to_csv(csv_filename, mode='a', index=False, header=False, encoding='utf-8')
        else:
            # Créer un nouveau fichier CSV avec l'en-tête
            product_data.to_csv(csv_filename, index=False, encoding='utf-8')

        # Télécharger et enregistrer l'image dans le répertoire de la catégorie
        download_image(image_url, os.path.join(output_folder, category), title)
    else:
        print(f'Erreur {response.status_code} lors de la requête vers {product_url}')

# Récupérez la page d'accueil
response = requests.get(base_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trouvez toutes les catégories
    categories = soup.select('div.side_categories ul.nav-list li ul li a')
    
    for category in categories:
        category_url = base_url + category['href']
        category_name = category.text.strip()
        print(f'Exploration de la catégorie {category_name}...')
        
        # Créez un répertoire pour la catégorie
        os.makedirs(os.path.join(output_folder, category_name), exist_ok=True)

        # Accédez à la page de la catégorie
        category_response = requests.get(category_url)
        
        if category_response.status_code == 200:
            category_soup = BeautifulSoup(category_response.text, 'html.parser')
            
            # Trouvez tous les produits dans la catégorie
            product_links = category_soup.select('h3 a')
            
            for product_link in product_links:
                product_url = base_url + 'catalogue' + product_link['href'][8:]
                extract_product_info(product_url, category_name)
        
        else:
            print(f'Erreur {category_response.status_code} lors de la requête vers {category_url}')
else:
    print(f'Erreur {response.status_code} lors de la requête vers {base_url}')
