
import requests
from bs4 import BeautifulSoup as bs
import urllib.request
import os

url="https://books.toscrape.com/catalogue/soumission_998/index.html"
response = requests.get(url)

if response.ok:
    soup = bs(response.text,'lxml')
    image = soup.find('div', class_="item active").find('img')
    
    print(image)
    #<img alt="A Light in the Attic" src="../../media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg"/>
    
def recup_chemin_image(soup):
    target_link_image = soup.find('div', class_="item active").find('img')['src']
    print( target_link_image)
    #../../media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg
    base_url="https://books.toscrape.com/"
    complete_link = base_url + target_link_image
    return complete_link.replace("../../",'')

    print(recup_chemin_image(soup))
 #https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg
 
image_url = recup_chemin_image(soup)

def sauv_image(image_url,fichier):
  
    
    my_path=os.path.dirname(__file__)+ '\img1' 
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    fullfilename = os.path.join(my_path, fichier)
    urllib.request.urlretrieve(image_url,fullfilename)
     
    
sauv_image(image_url,'sauvefichier22.jpeg')
print("création du dossier 'img1' ou est enregistré le fichier 'sauvefichier22.jpeg'")