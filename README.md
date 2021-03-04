# Script scrap.py pour le projet P2

Site de Books to Scrape:
http://books.toscrape.com/

**Écrivez un script Python qui visite cette page et en extrait les informations suivantes :**

* product_page_url
* universal_ product_code (upc)
* title
* price_including_tax
* price_excluding_tax
* number_available
* product_description
* category
* review_rating
* image_url

**Écrivez les données dans un fichier CSV qui utilise les champs ci-dessus comme en-têtes de colonnes.**
**Enregistrer le fichier image de chaque page Produit que vous consultez.**

> Pour créer un environnement virtuel, utiliser la commande:
python -m venv <environment name>

> Pour activer l'environnement virtuel:
source env/bin/activate
> Pour répliquer une installation d’un environnement avec le fichier requirements, taper la commande depuis votre environnement virtuel crée:
pip install -r requirements

>Pour quitter l'environnement virtuel:
deactivate

> Pour lancer le script:
> python scrap.py
