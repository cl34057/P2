#extraire les données de tous les produits d'une catégorie donnée sur le site 
# "Books to Scrape" et les écrire dans un seul fichier CSV portant le nom de 
# la catégorie. 
#Telecharger le fichier image de chaque livre de la categorie dans un repertoire. Le repertoire aura comme nom, 
# le nom de  la catégorie ou se trouve le livre, et le nom du  fichier image aura comme nom le   titre avant les ':'.jpeg
# parcourir toutes les pages si dans une catégorie il y a +eurs pages par la presence de 'next'
import requests
from bs4 import BeautifulSoup
import csv
import os

# Fonction pour extraire les données d'une page produit
def extract_product_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    upc = soup.select('th')[0].next_sibling.text
    title = soup.select('h1')[0].text.strip()
    price_including_tax = soup.select('th')[3].find_next('td').text.replace('Â','')
    price_excluding_tax = soup.select('th')[2].find_next('td').text.replace('Â','')
    number_available = soup.select('th')[5].find_next('td').text
    product_description = soup.select('meta[name="description"]')[0]['content']
    category = soup.select('ul.breadcrumb li')[2].text.strip()
    review_rating = soup.select('p.star-rating')[0]['class'][1]
    image_url = url.replace('index.html', '') + soup.find('img')['src']

    return upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url

# Fonction pour télécharger et enregistrer l'image
def download_and_save_image(image_url, category, title):
    response = requests.get(image_url)
    if response.status_code == 200:
        category_dir = category.replace(" ", "_")
        os.makedirs(category_dir, exist_ok=True)
        image_filename = os.path.join(category_dir, title.split(':')[0].strip() + '.jpeg')
        with open(image_filename, 'wb') as f:
            f.write(response.content)

# Fonction pour extraire les données de toutes les pages de la catégorie
def scrape_category(category_url, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['universal_product_code (upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

        while True:
            response = requests.get(category_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            product_links = soup.find_all('h3')
            
            for product_link in product_links:
                product_page_url = 'http://books.toscrape.com/catalogue' + product_link.a['href'][8:]
                product_data = extract_product_data(product_page_url)
                csv_writer.writerow(product_data)
                download_and_save_image(product_data[-1], product_data[6], product_data[1])

            next_page = soup.find('li', class_='next')
            if next_page:
               
                category_url = category_url.rsplit('/', 1)[0] + '/' + next_page.a['href']
            else:
                break

# URL de la page de la catégorie que vous souhaitez extraire
category_url = 'https://books.toscrape.com/catalogue/category/books/young-adult_21/page-1.html'

# Créer un fichier CSV avec le nom de la catégorie
category = category_url.split('/')[-3]
csv_filename = category + '.csv'

# Extraire les données de toutes les pages de la catégorie
scrape_category(category_url, csv_filename)

print(f"Données extraites et enregistrées dans {csv_filename}.")
