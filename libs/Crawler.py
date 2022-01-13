import simplejson
import requests
from bs4 import BeautifulSoup

from libs.helper import replace_space_to_hyphen
from libs.logger import get_logger

json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


class Crawler:
    doc = None

    def __init__(
        self,
    ):
        self._url = ""
        self._keyword = ""

    def set_header(self):
        headers = requests.utils.default_headers()
        headers.update({"User-Agent": "My User Agent 1.0"})
        return headers

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, val):
        try:
            self._keyword = val
        except:
            raise ValueError("The input you have provided is not string")

    def set_urls(self):
        pass

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, val):
        try:
            self._url = val
        except:
            raise ValueError("The input you have provided is not valid url form")

    def load(self):
        try:
            self.logging.debug("parsing started from this url : " + self.url)
            r = requests.get(self.url, headers=self.set_header())
            self.doc = BeautifulSoup(r.text, "lxml")

        except Exception as e:
            self.logging.error(f"get request error {e.__str__()}")

    def parse(self):
        pass

    def log_parsing_result(self, definition_count, example_count):
        self.logging.info(
            f"parsed definition {str(definition_count)}, example {str(example_count)}"
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
