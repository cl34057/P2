import requests
from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import csv

books=[]
# par rapport aux pages choisies
for i in range(1,3):
    url = f"https://books.toscrape.com/catalogue/page-{i}.html"
    response=requests.get(url)
    response=response.content
    soup=BeautifulSoup(response, 'html.parser')
    #print(soup)
    ol= soup.find('ol')
    #print(ol)
    articles = ol.find_all('article', class_='product_pod')
    #print(articles)

    for article in articles:
        image = article.find('img')
        #print(image)
        title= image.attrs['alt']
        #print(title)
        star = article.find('p')
        star = star['class'][1]
        #print(star)
        price = article.find('p', class_='price_color').text
        price = float(price[1:])
        #print(price)
        books.append([title,price,star])
        #print(books)
    df = pd.DataFrame(books, columns=['Title', 'Price', 'Star Rating'])
    df.to_csv('mutipagebooks.csv')
    print("Données extraites avec succès et enregistrées dans mutipagebooks.csv")