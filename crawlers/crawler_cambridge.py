import sys
from crawlers.crawler import Crawler


class CrawlerCambridge(Crawler):
    _site = "Cambridge"
    _url = "https://dictionary.cambridge.org/dictionary/english/"
    _dictionary_cards = [["div", "dictionary"]]
    _definition_element = ["div", ["def", "ddef_d", "db"]]
    _example_element = ["span", "eg"]

    def __init__(self, logging):
        super().__init__(logging)

    def print_data(self):
        print(f"site: {type(self)._site}")
        super().print_data()
