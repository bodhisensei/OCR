from sys import path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os.path
import re
import csv

"""Scraping du site books.toscrape.com
    Script Python qui visite une page html et en extrait les informations
    dans un fichier CSV, qui utilise les champs ci-dessus comme en-têtes de colonnes:
    product_page_url / universal_ product_code (upc) / title / price_including_tax
    price_excluding_tax / number_available / product_description / category
    review_rating / image_url"""

# Définition des variables globales pour stocker les urls des livres et stocker les infos
global urls_books, infos_books
urls_books, infos_books = [], []

# Fonction pour lancer le script et l'analyse du site
def start_scrap():
    cat_url = "https://books.toscrape.com/index.html"

    test_next(cat_url)
    print("Il y a {nb} livres à scraper".format(nb = len(urls_books)))
    scrap_book(urls_books)
    scrap_csv()

# Fonction qui appel le scraping d'un livre et test si page suivante
def test_next(test_url):
    url_cat = []
    while True:
        cat_r = requests.get(test_url)
        cat_soup = BeautifulSoup(cat_r.content, 'lxml')
        # appel de la fonction de scrap
        scrap_cat(cat_soup, test_url)

        # On test si il y a une page suivante
        if cat_soup.select('.next > a'):
            for next in cat_soup.select('.next > a'):
                test_url = urljoin(test_url, next.get('href'))
            url_cat.append(test_url)
        else:
            break

# Fonction pour scrap toutes les urls de la page en cours
def scrap_cat(cat_soup, cat_url):
    for link in cat_soup.select('h3 > a'):
        url = urljoin(cat_url, link.get('href'))
        urls_books.append(url)

# Fonction pour scraper les infos d'un livre
def scrap_book(urls):
    for link in urls:
        book = requests.get(link)
        book_soup = BeautifulSoup(book.content, 'lxml')

        # Titre du livre et netoyage de la chaine
        txt = book_soup.h1.text.lower()
        characters_to_remove = "#/*!()@"
        pattern = "[" + characters_to_remove + "]"
        new_txt = re.sub(pattern, "", txt)
        # On coupe le titre au caractere (
        title = ""
        for c in new_txt:
            if c != '(':
                title += c
            else:
                title = title[:-1]
                break

        # Url du livre
        url = book.url

        # Code UPC
        upc = book_soup.select('td')[0].text

        # Description du livre
        try:
            description = book_soup.select('.product_page > p')[0].text
        except:
            description = ""

        # Prix et stock dispo
        infos = book_soup.select('td')
        price_enctax = infos[2].text
        price_inctax = infos[3].text
        stock = "".join([x for x in book_soup.select('td')[5].text if x in "0123456789"])

        # Catégorie du livre et le nombre d'étoile
        category = book_soup.select('li > a')[2].text
        rating = book_soup.select('.star-rating')[0].get('class')[1]

        # Url de l'image et on appel la fonction d'enregistrement
        image_url = book_soup.select('img')[0]
        image_url = urljoin(link, image_url.get('src'))
        reps_img(title, category, image_url)
        
        # On ajoute les infos dans la liste globale infos_books
        infos_books.append([title, upc, category, price_inctax, price_enctax, stock, description, rating, image_url, url])

# Fonction qui va créer les répertoires par catégorie et nom de livre et enregistrer l'image
def reps_img(title, category, img_url):
    chemin_dossier = os.path.join(os.path.dirname(__file__),"Images", category, title)
    os.makedirs(chemin_dossier, exist_ok=True)
    url_img = requests.get(img_url)
    img_name = title+".jpg"
    # On télécharge et renomme l'image 
    with open(os.path.join(chemin_dossier, img_name), "wb") as file:
        file.write(url_img.content) 

#Fonction pour créer le fichier CSV
def scrap_csv():
    print("Ecriture du fichier csv")
    with open('books_infos.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["Title", "UPC_Code", "Category", "Price_IncluTax", "Price_ExcluTax", "Stock", "Description", "Rating", "Image_url", "Book_url"])
        writer.writerows(infos_books)

if __name__ == "__main__":
    print("Début du scraping du site")
    start_scrap()
    print("Fin !")