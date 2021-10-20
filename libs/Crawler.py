import simplejson
import requests
from bs4 import BeautifulSoup

from libs.helper import get_verb_particle_from_keyword
from libs.logger import get_logger

json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


class Crawler:
    logging = get_logger(config)
    doc = None

    def set_header(self):
        headers = requests.utils.default_headers()
        headers.update({"User-Agent": "My User Agent 1.0"})
        return headers

    def load(self):
        try:
            self.logging.debug("parsing started from this url : " + self.url)
            r = requests.get(self.url, headers=self.set_header())
            self.doc = BeautifulSoup(r.text, "lxml")

        except Exception as e:
            self.logging.error(f"get request error {e.__str__()}")

    def set_parse_url(self, site_data):
        self.url = site_data["url"] + self.keyword.replace(" ", "-")

    def set_keyword(self, keyword):
        self.keyword = keyword

    def filter_if_not_include_keyword(self, sentences):
        result = []
        verb, particle = get_verb_particle_from_keyword(self.keyword)

        for sentence in sentences:
            if verb in sentence or particle in sentence:
                result.append(sentence)

        return result

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
