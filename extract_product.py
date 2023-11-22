# Fonction pour extraire les données d'une page de produit
# Ecrire les données dans un fichier csv. Le nom du fichier csv correspondrait au titre avant les ':'.csv. 
# Telecharger le fichier image dans un repertoire. Le repertoire aura
# comme nom la catégorie ou se trouve le livre, et le nom du  fichier image aura comme nom le   titre avant les ':'.jpeg
import requests
from bs4 import BeautifulSoup
import os
import csv

# Fonction pour extraire les données d'une page produit
def extract_product_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_page_url = url
    
    upc = soup.select('th')[0].next_sibling.text
    title = soup.select('h1')[0].text.strip()
    price_including_tax = soup.select('th')[3].find_next('td').text.replace('Â','')
    price_excluding_tax = soup.select('th')[2].find_next('td').text.replace('Â','')
    number_available = soup.select('th')[5].find_next('td').text
    product_description = soup.select('meta[name="description"]')[0]['content']
    category = soup.select('ul.breadcrumb li')[2].text.strip()
    review_rating = soup.select('p.star-rating')[0]['class'][1]
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

# Créer un fichier CSV avec le nom du titre avant les deux-points (:)
csv_filename = product_data[2].split(':')[0].strip() + '.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
    csv_writer.writerow(product_data)

# Télécharger et enregistrer l'image dans le répertoire de la catégorie
download_and_save_image(product_data[-1], product_data[7], product_data[2])

print(f"Données extraites et enregistrées dans {csv_filename}.")
print("Image téléchargée et enregistrée dans le répertoire de la catégorie.")


