#Pour parcourir toutes les pages du site "Books to Scrape", 
# récupérer toutes les catégories, créer un répertoire pour chaque catégorie,
# télécharger et enregistrer les images de chaque produit dans le répertoire 
# correspondant (en utilisant le titre du produit avant les deux
# points ":" ou avant un slash "/") comme nom de fichier, 

import requests
from bs4 import BeautifulSoup
import csv

# URL de la page d'accueil du site "Books to Scrape"
base_url = 'http://books.toscrape.com/'

# Fonction pour extraire les informations d'une page de produit
def extract_product_info(product_url, category, csv_writer):
    response = requests.get(product_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        product_page_url = product_url
        upc = soup.select_one('th:contains("UPC") + td').text
        title = soup.select_one('h1').text
        price_including_tax = soup.select_one('th:contains("Price (incl. tax)") + td').text.replace('Â','')
        price_excluding_tax = soup.select_one('th:contains("Price (excl. tax)") + td').text.replace('Â','')
        number_available = soup.select_one('th:contains("Availability") + td').text
        product_description = soup.select_one('meta[name="description"]')['content']
        review_rating = soup.select_one('p.star-rating')['class'][1]
        image_url = base_url + soup.select_one('img')['src']

        # Écrivez les informations dans le fichier CSV
        csv_writer.writerow([
            product_page_url, upc, title, price_including_tax,
            price_excluding_tax, number_available, product_description,
            category, review_rating, image_url
        ])
        
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
        
        # Créez un fichier CSV pour la catégorie
        csv_filename = f'{category_name}.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Écrivez l'en-tête du fichier CSV
            csv_writer.writerow([
                'product_page_url', 'upc', 'title', 'price_including_tax',
                'price_excluding_tax', 'number_available', 'product_description',
                'category', 'review_rating', 'image_url'
            ])
            
            # Accédez à la page de la catégorie
            category_response = requests.get(category_url)
            
            if category_response.status_code == 200:
                category_soup = BeautifulSoup(category_response.text, 'html.parser')
                
                # Trouvez tous les produits dans la catégorie
                product_links = category_soup.select('h3 a')
                
                for product_link in product_links:
                    product_url = base_url + 'catalogue' + product_link['href'][8:]
                    extract_product_info(product_url, category_name, csv_writer)
            
            else:
                print(f'Erreur {category_response.status_code} lors de la requête vers {category_url}')
else:
    print(f'Erreur {response.status_code} lors de la requête vers {base_url}')
