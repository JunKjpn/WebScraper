import logging
import time
from datetime import datetime
from pathlib import Path

import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

URL = "https://books.toscrape.com/"
OUTPUT_DIR = Path("../output")
REQUEST_TIMEOUT = 10
REQUEST_INTERVAL = 1
USER_AGENT = "Mozilla/5.0"
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}
COLUMNS = [
    "title",
    "price",
    "availability",
    "rating",
    "url",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

def scrape_books(url: str) -> list[dict]:
    books = []
    page_number = 1

    while url:
        session = requests.Session()

        session.headers.update({"User-Agent": USER_AGENT})

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        session.mount("https://", adapter)
        session.mount("http://", adapter)

        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"取得に失敗しました: {url} - {e}")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        page_books = soup.select("article.product_pod")

        logger.info(
            f"{page_number}ページ目を取得中... "
            f"{len(page_books)}冊"
        )

        for article in soup.select("article.product_pod"):
            title = article.select_one("h3 a")
            price = article.select_one(".price_color")
            availability = article.select_one(".availability")
            rating = article.select_one(".star-rating")

            rating_value = None

            if rating:
                rating_classes = rating.get("class", [])

                for class_name in rating_classes:
                    if class_name in RATING_MAP:
                        rating_value = RATING_MAP[class_name]
                        break

            books.append(
                {
                    "title": title["title"] if title else None,
                    "price": (parse_price(price.get_text(strip=True)) if price else None),
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
                    "rating": rating_value,
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

def validate_books(books: list[dict]) -> list[dict]:
    valid_books = []

    for book in books:
        if not book["title"]:
            logger.warning("タイトルが取得できないデータを除外しました")
            continue

        if book["price"] is None:
            logger.warning(
                f"価格が取得できないデータを除外しました: {book['title']}"
            )
            continue

        if book["price"] < 0:
            logger.warning(
                f"不正な価格のデータを除外しました: {book['title']}"
            )
            continue

        if book["rating"] is None:
            logger.warning(
                f"評価が取得できないデータを除外しました: "
                f"{book['title']}"
            )
            continue

        if not 1 <= book["rating"] <= 5:
            logger.warning(
                f"不正な評価のデータを除外しました: "
                f"{book['title']}"
            )
            continue

        if not isinstance(book["availability"], bool):
            logger.warning(
                f"在庫情報が不正なデータを除外しました: "
                f"{book['title']}"
            )
            continue

        if not book["url"]:
            logger.warning(
                f"URLが取得できないデータを除外しました: {book['title']}"
            )
            continue

        valid_books.append(book)

    return valid_books

def parse_price(price: str) -> float:
    return float(price.replace("£", "").replace("Â", "").strip() )

def parse_availability(availability: str) -> bool:
    return "In stock" in availability

def create_dataframe(books: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(books, columns=COLUMNS)

    df["price"] = df["price"].astype(float)
    df["rating"] = df["rating"].astype(int)
    df["availability"] = df["availability"].astype(bool)

    return df

def save_to_csv(df: pd.DataFrame, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(filepath, index=False, encoding="utf-8-sig")

    logger.info(f"CSVを保存しました: {filepath}")

def main():
    books = scrape_books(URL)
    books = validate_books(books)

    df = create_dataframe(books)

    logger.info(f"取得件数: {len(df)}")
    print(df.head())

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"books_{timestamp}.csv"
    save_to_csv(df, output_file)


if __name__ == "__main__":
    main()