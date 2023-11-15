#Coder en python. Sur le site Books to scrape, parcourir 
# toutes les pages du site. Dans chaque categorie on retrouve des produits. 
# Créer donc un repertoire pour chaque catégorie rencontrée. 
# Chaque repertoire aura comme nom le nom de la categorie. 
# Ensuite, Telecharger et enregistrer dans chacun des catégories 
# les fichiers images  de chaque produits appartenant  à la catégorie.
# Le nom de chaque fichier image correspondrait au titre du livre.jpeg. 
# Au cas ou il y a des titres avec des caractères speciaux, ne recuperer que 
# le titre qu'en dehors des caractère spéciaux.jpeg. 
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import re

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
    # Utiliser une expression régulière pour extraire le titre sans caractères spéciaux
    clean_title = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    return clean_title.strip()

# URL du site "Books to scrape"
base_url = "http://books.toscrape.com/"
output_folder = "output"

# Télécharger la page d'accueil
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Trouver toutes les catégories
categories = soup.select('div.side_categories ul li ul li a')

# Parcourir chaque catégorie
for category in categories:
    category_name = category.text.strip()
    category_folder = os.path.join(output_folder, category_name)

    # Créer un répertoire pour la catégorie
    os.makedirs(category_folder, exist_ok=True)

    # Construire l'URL de la catégorie
    category_url = urljoin(base_url, category.get('href'))

    # Télécharger la première page de la catégorie
    category_response = requests.get(category_url)
    category_soup = BeautifulSoup(category_response.text, 'html.parser')

    # Parcourir toutes les pages de la catégorie
    while True:
        # Trouver tous les produits dans la page
        products = category_soup.select('h3 a')

        # Parcourir chaque produit
        for product in products:
            product_url = urljoin(category_url, product.get('href'))
            product_response = requests.get(product_url)
            product_soup = BeautifulSoup(product_response.text, 'html.parser')

            # Trouver le titre du produit
            title = product_soup.h1.text.strip()

            # Trouver l'URL de l'image du produit
            img_url = urljoin(product_url, product_soup.select_one('div.item img')['src'])

            # Télécharger et enregistrer l'image dans le répertoire de la catégorie
            download_image(img_url, category_folder, title)

        # Trouver le lien vers la page suivante (si elle existe)
        next_page = category_soup.find('li', class_='next')
        if next_page:
            next_page_url = urljoin(category_url, next_page.a['href'])
            category_response = requests.get(next_page_url)
            category_soup = BeautifulSoup(category_response.text, 'html.parser')
        else:
            break
