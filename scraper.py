import time

import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin


URL = "https://books.toscrape.com/"
OUTPUT_FILE = "output/books.csv"
REQUEST_TIMEOUT = 10
REQUEST_INTERVAL = 1
USER_AGENT = "Mozilla/5.0"

def scrape_books(url: str) -> list[dict]:
    books = []
    page_number = 1

    while url:
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})

        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"取得に失敗しました: {url}")
            print(f"エラー: {e}")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        page_books = soup.select("article.product_pod")

        print(
            f"{page_number}ページ目を取得中... "
            f"{len(page_books)}冊"
        )

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
            page_number += 1
        else:
            url = None

        time.sleep(REQUEST_INTERVAL)

    return books

def create_dataframe(books: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(books)

def save_to_csv(df: pd.DataFrame, filepath: str) -> None:
    df.to_csv(filepath, index=False, encoding="utf-8-sig")

def main():
    books = scrape_books(URL)
    df = create_dataframe(books)

    print(f"取得件数: {len(df)}")
    print(df.head())

    save_to_csv(df, OUTPUT_FILE)


if __name__ == "__main__":
    main()