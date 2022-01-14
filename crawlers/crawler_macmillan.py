import sys
from crawlers.crawler import Crawler


class CrawlerMacmillan(Crawler):
    _site = "Macmillan"
    _url = "https://www.macmillandictionary.com/dictionary/british/"
    _dictionary_cards = [["div", "SENSE-CONTENT"]]
    _definition_element = ["span", ["DEFINITION"]]
    _example_element = ["p", "EXAMPLE"]

    def __init__(self, logging):
        super().__init__(logging)

    def print_data(self):
        print(f"site: {type(self)._site}")
        super().print_data()
