import sys
from crawlers.crawler import Crawler


class CrawlerMacmillan(Crawler):
    _site = "Macmillan"
    _url = "https://www.macmillandictionary.com/dictionary/british/"
    _dictionary_cards = [["div", "SENSE-CONTENT"]]
    _definition_element = ["span", ["DEFINITION"]]
    _example_element = ["p", "EXAMPLE"]

    def __init__(self, logging):
        self._logging = logging
        Crawler.__init__(self, logging)
