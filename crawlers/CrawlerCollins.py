import sys
from libs.Crawler import Crawler


class CrawlerCollins(Crawler):
    def __init__(self):
        self.site = "Collins"
        self.dictionary_cards = [["div", "hom"]]
        self.definition_element = ["div", "def"]
        self.example_element = ["span", "quote"]

    def set_parse_url(self, site_data):
        self.url = site_data["url"] + self.keyword.replace(" ", "-")

    def parse(self):
        try:
            dictionary_cards = self.find_elements(self.dictionary_cards)
            definitions = []
            examples = []
            for dict_card in dictionary_cards:
                definitions.extend(
                    self.find_text_contents(dict_card, self.definition_element)
                )
                examples.extend(
                    self.find_text_contents(dict_card, self.example_element)
                )

            self.definitions = definitions
            self.examples = self.filter_if_not_include_keyword(examples)
            self.log_parsing_result(len(self.definitions), len(self.examples))

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(f"parse except,  {tb.tb_lineno},  {e.__str__()}")
