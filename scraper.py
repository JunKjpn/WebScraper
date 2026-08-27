import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin


URL = "https://books.toscrape.com/"


def scrape_books(url: str) -> list[dict]:
    books = []

    while url:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        for article in soup.select("article.product_pod"):
            title = article.select_one("h3 a")
            price = article.select_one(".price_color")
            availability = article.select_one(".availability")

            books.append(
                {
                    "title": title["title"] if title else None,
                    "price": (
                        parse_price(price.get_text(strip=True))
                        if price
                        else None
                    ),
                    "availability": (
                        parse_availability(
                            availability.get_text(" ", strip=True)
                        )
                        if availability
                        else None
                    ),
                    "url": (
                        urljoin(url, title["href"])
                        if title
                        else None
                    ),
                }
            )

        next_link = soup.select_one("li.next a")

        if next_link:
            url = urljoin(url, next_link["href"])
        else:
            url = None

    return books

def parse_price(price: str) -> float:
    return float(price.replace("£", "").replace("Â", "").strip())

def parse_availability(availability: str) -> bool:
    return "In stock" in availability

def main():
    books = scrape_books(URL)

    df = pd.DataFrame(books)

    print(f"取得件数: {len(df)}")
    print(df.head())

    df.to_csv("output/books.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    main()