import requests
from bs4 import BeautifulSoup
import csv

"""Scraping du livre Misery
    Écrivez un script Python qui visite cette page et en extrait les informations
    dans un fichier CSV qui utilise les champs ci-dessus comme en-têtes de colonnes:
    product_page_url
    universal_ product_code (upc)
    title
    price_including_tax
    price_excluding_tax
    number_available
    product_description
    category
    review_rating
    image_url"""

# Faire une requette de la page http
url = "http://books.toscrape.com/catalogue/misery_332/index.html"

r = requests.get(url)

if r.ok:
    soup = BeautifulSoup(r.content, 'lxml')
    title = soup.h1.text.lower()
    url = r.url
    upc = soup.select('td')[0].text

    description = soup.select('.product_page > p')
    description = description[0].text
     
    infos = soup.select('td')
    price_enctax = infos[2].text
    price_inctax = infos[3].text

    num_avail = infos[5].text
    num = "".join([x for x in num_avail if x in "0123456789"])
    category = soup.select('li > a')[2].text
    image_url = soup.select('img')[0]
    image_url = ("https://books.toscrape.com/" + image_url.get('src')[5:])
    rating = soup.select('.star-rating')[0].get('class')[1]
    print(rating)

with open('misery.csv', 'w', encoding = 'utf-8-sig') as filecsv:
    scrapwriter = csv.writer(filecsv, delimiter=";")
    scrapwriter.writerow(["Title", "UPC_Code", "Category", "Price_Inctax", "Price_Exctax", "Stock", "Description", "Rating", "Image_url", "Book_url"])
    scrapwriter.writerow([title, upc, category, price_inctax, price_enctax, num, description, rating, image_url, url])

