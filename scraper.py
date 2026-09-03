import requests
from bs4 import BeautifulSoup


def scrape_books():
    url = "https://books.toscrape.com/"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    for book in soup.select(".product_pod"):
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text
        availability = book.select_one(".availability").text.strip()

        books.append({
            "title": title,
            "price": price,
            "availability": availability
        })

    return books