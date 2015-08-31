from lxml import html
from lxml.html.clean import Cleaner
import requests
import sqlite3
from time import sleep
from datetime import datetime


def get_categories():
    url = 'http://www.ncix.com/categories/'
    page = requests.get(url)
    tree = html.fromstring(page.text)
    categories = tree.xpath('//blockquote/p/a/@href')
    for category in categories:
        scrape_ncix(category)

def scrape_ncix(category):
    sleep(2)
    page = requests.get(category)
    tree = html.fromstring(page.text)
    titles = tree.xpath('//span[@class="listing"]/a/text()')
    prices = tree.xpath('//td[@class="line"]/font/strong/text()')
    add_to_db(zip(titles, prices, [datetime.now()]*len(titles)))

def add_to_db(products):
    conn = sqlite3.connect('products.db')
    with conn:
        c = conn.cursor()
        table = 'CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, titles TEXT, prices FLOAT, date_added TIMESTAMP)'
        c.execute(table)
        c.executemany('''INSERT INTO products (titles, prices, date_added) VALUES (?,?,?)''', products)


if __name__ == '__main__':
    get_categories()
    # print(datetime.now())
