import sys
from libs.Crawler import Crawler


class CrawlerMacmillan(Crawler):
    def __init__(self):
        self.site = "Macmillan"
        self.definition_element = ["span", "DEFINITION"]
        self.example_element = ["p", "EXAMPLE"]

    def set_parse_url(self, site_data):
        self.url = site_data["url"] + self.keyword.replace(" ", "-")

    def parse(self):
        try:
            definitions = []
            examples = []
            definitions.extend(
                self.find_text_contents(self.doc, self.definition_element)
            )
            examples.extend(self.find_text_contents(self.doc, self.example_element))

            self.definitions = definitions
            self.examples = self.filter_if_not_include_keyword(examples)
            self.log_parsing_result(len(self.definitions), len(self.examples))

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(f"parse except,  {tb.tb_lineno},  {e.__str__()}")
