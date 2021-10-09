import sys

from libs.Crawler import Crawler


class CrawlerCambridge(Crawler):
    def __init__(self):
        self.site = "Cambridge"
        self.dictionary_cards = [["div", "dictionary"]]
        self.definition_element = ["div", ["def", "ddef_d", "db"]]
        self.example_element = ["span", "eg"]

    def set_parse_url(self, site_data):
        self.url = site_data["url"] + self.keyword.replace(" ", "-")

    def parse(self):
        try:
            dictionary_cards = self.find_elements(self.dictionary_cards)
            definitions = []
            examples = []
            for dict_card in dictionary_cards:
                category = dict_card.find("div", class_="pos-header").text
                if "phrasal verb" in category:
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
