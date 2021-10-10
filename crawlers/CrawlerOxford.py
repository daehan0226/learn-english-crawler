import sys
from libs.Crawler import Crawler


class CrawlerOxford(Crawler):
    def __init__(self):
        self.site = "Oxford"
        self.dictionary_cards = [["ol", "senses_multiple"], ["ol", "sense_single"]]
        self.definition_element = ["span", "def"]
        self.example_element = ["ul", "examples"]

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
