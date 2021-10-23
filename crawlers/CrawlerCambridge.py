import sys
from libs.Crawler import Crawler


class CrawlerCambridge(Crawler):
    def __init__(self):
        self.site = "Cambridge"
        self.dictionary_cards = [["div", "dictionary"]]
        self.definition_element = ["div", ["def", "ddef_d", "db"]]
        self.example_element = ["span", "eg"]

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
            self.examples = examples
            self.log_parsing_result(len(self.definitions), len(self.examples))

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(f"parse except,  {tb.tb_lineno},  {e.__str__()}")
