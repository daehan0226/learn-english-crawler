import sys
from crawlers.crawler import Crawler


class CrawlerOxford(Crawler):
    _site = "oxford"
    _url = "https://www.oxfordlearnersdictionaries.com/definition/english/"
    _dictionary_cards = [["ol", "senses_multiple"], ["ol", "sense_single"]]
    _definition_element = ["span", ["def"]]
    _example_element = ["ul", "examples"]

    def __init__(self, logging):
        self._logging = logging
        Crawler.__init__(self, logging)
