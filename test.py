from sys import path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os.path



global urls_books, infos_books
urls_books, infos_books = [], []

cat_url = "https://books.toscrape.com/catalogue/the-bridge-to-consciousness-im-writing-the-bridge-between-science-and-our-old-and-new-beliefs_840/index.html"
# cat_url = "https://books.toscrape.com/catalogue/red-hoodarsenal-vol-1-open-for-business-red-hoodarsenal-1_729/index.html"
cat_r = requests.get(cat_url)
cat_soup = BeautifulSoup(cat_r.content, 'lxml')

title = cat_soup.h1.text.lower()
characters_to_remove = "#/*!@"
pattern = "[" + characters_to_remove + "]"
new_string = re.sub(pattern, " ", title)
print(new_string)
txt = ""
for c in new_string:
    if c != '(':
        txt += c
    else:
        txt = txt[:-1]
        break    
print(txt)

try:
    description = cat_soup.select('.product_page > p')[0].text
except:
    description = "zzz"
    print(description)
    
print(description)


def scrap_book(urls):

    for link in urls:
        # infos_book = []
        book = requests.get(link)
        book_soup = BeautifulSoup(book.content, 'lxml')

        title = book_soup.h1.text.lower()
        txt = ""
        for c in title:
            if c != '(':
                txt += c
            else:
                txt = txt[:-1]
                break    
        # characters_to_remove = "#/!()@"
        # pattern = "[" + characters_to_remove + "]"
        # new_string = re.sub(pattern, "", txt)

        url = book.url
        upc = book_soup.select('td')[0].text

        description = book_soup.select('.product_page > p')[0].ext
        # description = description[0].text

        infos = book_soup.select('td')
        price_enctax = infos[2].text
        price_inctax = infos[3].text

        stock_avail = infos[5].text
        stock = "".join([x for x in book_soup.select('td')[5].text if x in "0123456789"])
        print(stock)


        category = book_soup.select('li > a')[2].text
        image_url = book_soup.select('img')[0]
        image_url = urljoin(link, image_url.get('src'))
        rating = book_soup.select('.star-rating')[0].get('class')[1]

