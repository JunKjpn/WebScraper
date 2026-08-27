from urllib.parse import urljoin

import requests
import pandas as pd
from bs4 import BeautifulSoup


URL = "https://books.toscrape.com/"


def scrape_books(url: str) -> list[dict]:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    books = []

    for article in soup.select("article.product_pod"):
        title = article.select_one("h3 a")
        price = article.select_one(".price_color")
        availability = article.select_one(".availability")

        books.append(
            {
                "title": title["title"] if title else None,
                "price": price.get_text(strip=True) if price else None,
                "availability": (
                    availability.get_text(" ", strip=True)
                    if availability
                    else None
                ),
                "url": urljoin(url, title["href"]) if title else None,
            }
        )

    return books


def main():
    books = scrape_books(URL)

    df = pd.DataFrame(books)

    print(df)

    df.to_csv("output/books.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    main()