from webscraper.scraper import parse_price
from webscraper.scraper import parse_availability


def test_parse_price():
    assert parse_price("£51.77") == 51.77
    assert parse_price("£100.00") == 100.0

def test_parse_availability():
    assert parse_availability("In stock") is True
    assert parse_availability("Out of stock") is False