from unittest.mock import patch, Mock

import requests

from webscraper.scraper import parse_price, parse_availability, parse_rating, scrape_books

TEST_HTML = """
<html>
<body>
<article class="product_pod">
    <h3>
        <a href="catalogue/test-book_1/index.html"
           title="Test Book">
            Test Book
        </a>
    </h3>

    <p class="price_color">£19.99</p>

    <p class="instock availability">
        In stock
    </p>

    <p class="star-rating Three"></p>
</article>
</body>
</html>
"""

TEST_HTML_PAGE_1 = """
<html>
<body>
<article class="product_pod">
    <h3>
        <a href="catalogue/book_1/index.html"
           title="Book One">
            Book One
        </a>
    </h3>
    <p class="price_color">£10.00</p>
    <p class="instock availability">In stock</p>
    <p class="star-rating One"></p>
</article>

<ul class="pager">
    <li class="next">
        <a href="page-2.html">next</a>
    </li>
</ul>
</body>
</html>
"""

TEST_HTML_PAGE_2 = """
<html>
<body>
<article class="product_pod">
    <h3>
        <a href="catalogue/book_2/index.html"
           title="Book Two">
            Book Two
        </a>
    </h3>
    <p class="price_color">£20.00</p>
    <p class="instock availability">In stock</p>
    <p class="star-rating Five"></p>
</article>
</body>
</html>
"""


def test_parse_price():
    assert parse_price("£51.77") == 51.77
    assert parse_price("£100.00") == 100.0

def test_parse_availability():
    assert parse_availability("In stock") is True
    assert parse_availability("Out of stock") is False

def test_parse_rating():
    assert parse_rating(["star-rating", "One"]) == 1
    assert parse_rating(["star-rating", "Three"]) == 3
    assert parse_rating(["star-rating", "Five"]) == 5
    assert parse_rating(["star-rating", "Unknown"]) is None

@patch("webscraper.scraper.session.get")
def test_scrape_books(mock_get):
    mock_response = Mock()
    mock_response.content = TEST_HTML.encode("utf-8")
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    books = scrape_books("https://books.toscrape.com/")

    assert len(books) == 1

    assert books[0]["title"] == "Test Book"
    assert books[0]["price"] == 19.99
    assert books[0]["availability"] is True
    assert books[0]["rating"] == 3

@patch("webscraper.scraper.session.get")
def test_scrape_books_pagination(mock_get):
    response_page_1 = Mock()
    response_page_1.content = TEST_HTML_PAGE_1.encode("utf-8")
    response_page_1.raise_for_status.return_value = None

    response_page_2 = Mock()
    response_page_2.content = TEST_HTML_PAGE_2.encode("utf-8")
    response_page_2.raise_for_status.return_value = None

    mock_get.side_effect = [response_page_1, response_page_2]

    books = scrape_books("https://books.toscrape.com/")

    assert len(books) == 2

    assert books[0]["title"] == "Book One"
    assert books[0]["price"] == 10.00
    assert books[0]["rating"] == 1

    assert books[1]["title"] == "Book Two"
    assert books[1]["price"] == 20.00
    assert books[1]["rating"] == 5

    assert mock_get.call_count == 2

@patch("webscraper.scraper.session.get")
def test_scrape_books_request_error(mock_get):
    mock_get.side_effect = requests.RequestException("Connection timeout")

    books = scrape_books("https://books.toscrape.com/")

    assert books == []
    assert mock_get.call_count == 1
