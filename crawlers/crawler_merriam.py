import sys
from crawlers.crawler import Crawler


class CrawlerMerriam(Crawler):
    _site = "Merriam"
    _url = "https://www.merriam-webster.com/dictionary/"
    _dictionary_cards = [["div", "left-content"]]
    _definition_element = ["span", ["dtText"]]
    _example_element = ["span", ["ex-sent", "t"]]

    def __init__(self, logging):
        super().__init__(logging)
