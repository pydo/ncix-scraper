from lxml import html
from lxml.html.clean import Cleaner
import requests
import sqlite3
from time import sleep


def get_categories():
    url = 'http://www.ncix.com/categories/'
    page = requests.get(url)
    tree = html.fromstring(page.text)
    categories = tree.xpath('//blockquote/p/a/@href')
    for category in categories:
        scrape_ncix(category)

def scrape_ncix(category):
    sleep(5)
    page = requests.get(category)
    tree = html.fromstring(page.text)
    titles = tree.xpath('//span[@class="listing"]/a/text()')
    prices = tree.xpath('//td[@class="line"]/font/strong/text()')
    add_to_db(zip(set(titles), set(prices)))

def add_to_db(products):
    conn = sqlite3.connect('products.db')
    with conn:
        c = conn.cursor()
        table = 'CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, titles TEXT, prices FLOAT)'
        c.execute(table)
        c.executemany('''INSERT INTO products (titles, prices) VALUES (?,?)''', products)


if __name__ == '__main__':
    get_categories()