import os
import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect("heb_prices.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS prices (id INTEGER PRIMARY KEY, item TEXT, price REAL, date DATE)")

# Scrape H-E-B website for prices on staple foods
def scrape_prices():
    cache_key = "heb_prices"
    cache_value = cache.get(cache_key)
    if cache_value:
        return cache_value

    response = requests.get("https://www.heb.com/")

    soup = BeautifulSoup(response.text, "html.parser")

    prices = []
    for item in ["Fresh", "H-E-B Chicken", "H-E-B Turkey", "H-E-B Beef", "H-E-B Pork", "H-E-B Ground", "H-E-B Eggs"]:
        price_elements = soup.find_all(class_="heb-price__name", text=lambda t: t and item in t)
        for element in price_elements:
            price = float(element.find_next(class_="heb-price__price").text[1:])
            name = element.text
            date = datetime.datetime.now().date()
            prices.append((name, price, date))

    cursor.executemany("INSERT INTO prices (item, price, date) VALUES (?, ?, ?)", prices)
    conn.commit()

    cache.set(cache_key, prices, timeout=86400)

# daily
while True:
    scrape_prices()
    time.sleep(86400)

conn.close()