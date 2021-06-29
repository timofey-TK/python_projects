from io import BytesIO

from urllib.request import urlopen
import pandas as pd
import requests as req
from bs4 import BeautifulSoup
import lxml
page = 1
parsed_books = []
while page <= 20:
    r = req.get(f'http://books.toscrape.com/catalogue/page-{page}.html')
    soup = BeautifulSoup(r.text, 'lxml')
    books = soup.select('article.product_pod')
    for book in books:
        image = book.select_one('.image_container a .thumbnail')[
            "src"].replace("../", "http://books.toscrape.com/")
        a_tag = book.select_one("h3 a")
        name = a_tag["title"]
        link = "http://books.toscrape.com/catalogue/" + a_tag["href"]
        cost = book.select_one(
            ".product_price p.price_color").text.replace("Â", "")
        parsed_books.append({
            "name": name,
            "link": link,
            "cost": cost,
            "image": image
        })
    page += 1

df = pd.DataFrame({'Name': [x["name"] for x in parsed_books],
                   'Cost': [x["cost"] for x in parsed_books],
                   'Link': [x["link"] for x in parsed_books],
                   'Image': [x["image"] for x in parsed_books]
                   })
df.to_excel('pandas_image.xlsx')
