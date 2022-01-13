import simplejson
import requests
from bs4 import BeautifulSoup

from libs.helper import replace_space_to_hyphen

json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


class Crawler:
    def __init__(self, logging):
        self._logging = logging
        self._parse_url = ""
        self._doc = None
        self._definitions = []
        self._examples = []

    def _set_header(self):
        headers = requests.utils.default_headers()
        headers.update({"User-Agent": "My User Agent 1.0"})
        return headers

    @property
    def definitions(self):
        return self._definitions

    @property
    def examples(self):
        return self._examples

    @property
    def site(self):
        return self._site

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, val):
        try:
            self._keyword = replace_space_to_hyphen(val)
        except:
            raise ValueError(f"Please check the given keyword : {val}")

    @property
    def parse_url(self):
        return self._parse_url

    def set_parse_url(self):
        if not self._keyword:
            raise ValueError("Please set keyword first")
        self._parse_url = f"{self._url}{self._keyword}"

    def load(self):
        try:
            self._logging.debug("parsing started from this url : " + self._parse_url)
            r = requests.get(self._parse_url, headers=self._set_header())
            self.doc = BeautifulSoup(r.text, "lxml")
        except Exception as e:
            self._logging.error(f"get request error {e.__str__()}")

    def parse(self):
        dictionary_cards = self.find_elements(self._dictionary_cards)
        for dict_card in dictionary_cards:
            self._examples.extend(
                self.find_text_contents(dict_card, self._example_element)
            )
            self._definitions.extend(
                self.find_text_contents(dict_card, self._definition_element)
            )
        self._logging.info(
            f"parsed from {self._site}, count : definition {len(self._definitions)}, example {len(self._examples)}"
        )

    def find_text_contents(self, src, selector):
        result = []
        tag, class_ = selector
        elements = src.find_all(tag, class_=class_)
        for element in elements:
            result.append(element.text)

        return result

    def find_elements(self, selectors):
        result = []
        for selector in selectors:
            tag, class_ = selector
            result.extend(self.doc.find_all(tag, class_=class_))
        return result
