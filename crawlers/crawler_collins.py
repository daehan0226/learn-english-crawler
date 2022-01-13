import sys
from crawlers.crawler import Crawler


class CrawlerCollins(Crawler):
    _site = "Collins"
    _url = "https://www.collinsdictionary.com/dictionary/english/"
    _dictionary_cards = [["div", "hom"]]
    _definition_element = ["div", "def"]
    _example_element = ["span", "quote"]

    def __init__(self, logging):
        Crawler.__init__(self, logging)
