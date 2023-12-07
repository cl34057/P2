#*********************II***extract_products_category_csv_img.py************************


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

# Fonction pour extraire les données d'une page produit
def extract_product_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_page_url = url
    upc = soup.find('th').find_next('td').text
    title = soup.find('h1').text.strip()
    price_including_tax = soup.find_all('th')[3].find_next('td').text.replace('Â','')
    price_excluding_tax = soup.find_all('th')[2].find_next('td').text.replace('Â','')
    #umber_available = soup.find_all('th')[5].find_next('td').text
    number_available_text = soup.find_all('th')[5].find_next('td').text
    number_available = int(re.search(r'\b(\d+)\b', number_available_text).group())
    product_description = soup.find('meta', {'name': 'description'})['content']
    category = soup.select('ul.breadcrumb li')[2].text.strip()
    #review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
    review_rating_class = soup.find('p', {'class': 'star-rating'})['class'][1]
    review_rating = extract_review_rating(review_rating_class)
    image_url = url.replace('index.html', '') + soup.find('img')['src']

    return product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url

# Fonction pour télécharger et enregistrer l'image
def download_and_save_image(image_url, category, title):
    response = requests.get(image_url)
    if response.status_code == 200:
        category_dir = re.sub(r'\W', '_', category)  # Remplace les caractères non alphanumériques par '_'
        os.makedirs( 'download/'+category_dir, exist_ok=True)
        title_without_special_chars = re.sub(r'\W', '_', title.split(':')[0].strip())
        image_filename = os.path.join('download/'+category_dir, title_without_special_chars + '.jpeg')
        with open(image_filename, 'wb') as f:
            f.write(response.content)

# Fonction pour extraire les URLs de tous les produits dans une catégorie
def extract_all_product_urls(category_url):
    all_urls = []
    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Trouver toutes les balises <h3> qui contiennent les liens vers les pages de produits
        product_links = soup.find_all('h3')
        
        # Construire la liste complète des URLs des produits
        base_url = 'https://books.toscrape.com/catalogue/'
        product_urls = [base_url + link.a['href'][9:] for link in product_links]
        all_urls.extend(product_urls)

        # Extraire l'URL de la page suivante
        next_page = soup.find('li', class_='next')
        if next_page:
            category_url = category_url.rsplit('/', 1)[0] + '/' + next_page.a['href']
        else:
            break
    
    return all_urls

# Demander à l'utilisateur l'URL de la page de catégorie
category_url = input("Veuillez entrer l'URL de la catégorie que vous souhaitez extraire : ")

# Extraire les URLs de tous les produits dans la catégorie
product_urls = extract_all_product_urls(category_url)

# Liste pour stocker les données de tous les produits
all_product_data = []

# Boucle à travers les URLs des produits et extraire les données
for product_url in product_urls:
    product_data = extract_product_data(product_url)
    all_product_data.append(product_data)
    
    
    

# Créer un DataFrame pandas pour mieux organiser les données
columns = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
df = pd.DataFrame(all_product_data, columns=columns)

# Créer un répertoire "CSV" s'il n'existe pas
csv_folder = "download/CSV"
os.makedirs(csv_folder, exist_ok=True)

# Créer un fichier CSV avec le nom de la catégorie
csv_filename = re.sub(r'\W', '_', category_url.split('/')[-2]) + '.csv'

# Écrire les données dans le fichier CSV en ajustant la largeur des colonnes
csv_filepath = os.path.join(csv_folder, csv_filename)
df.to_csv(csv_filepath, index=False, encoding='utf-8')

# Télécharger et enregistrer les images dans le répertoire de la catégorie
for product_data in all_product_data:
    download_and_save_image(product_data[-1], product_data[7], product_data[2])

print(f"Données extraites et enregistrées dans {csv_filepath}.")
print("Images téléchargées et enregistrées dans le répertoire de la catégorie.")
