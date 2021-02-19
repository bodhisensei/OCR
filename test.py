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
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.title.string.strip().strip("| Books to Scrape - Sandbox")
    url = r.url
    upc = soup.find_all('td')[0].text
    # upc2 = soup.find_all("article", attrs={"class": "product_page"})

    print(title)
    print(url)
    print(upc)

with open('misery.csv', 'w') as filecsv:
    scrapwriter = csv.writer(filecsv, delimiter=";")
    scrapwriter.writerow(["Title", "Url", "UPC_Code", "Category", "Price_Inctax", "Price_Exctax", "Nb", "Description", "Rating"])
    scrapwriter.writerow([title, url, upc])