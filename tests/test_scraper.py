from webscraper.scraper import parse_price, parse_availability, parse_rating


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