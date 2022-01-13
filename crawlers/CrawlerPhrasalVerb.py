import sys
from libs.crawler import Crawler


class CrawlerPhrasalVerb(Crawler):
    def __init__(self):
        self.definitions = []
        self.examples = []

    def get_urls(self, sites):
        urls = []
        for site, site_data in sites.items():
            urls.append({"site": site, "url": f"{site_data['url']}{self.keyword}"})
        return urls

    def parse(self):
        try:
            dictionary_cards = self.find_elements(
                self.site_elements["dictionary_cards"]
            )
            definitions = []
            examples = []
            for dict_card in dictionary_cards:
                definitions.extend(
                    self.find_text_contents(
                        dict_card, self.site_elements["definition_element"]
                    )
                )
                examples.extend(
                    self.find_text_contents(
                        dict_card, self.site_elements["example_element"]
                    )
                )

            self.definitions = definitions
            self.examples = examples
            self.log_parsing_result(len(self.definitions), len(self.examples))

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(f"parse except,  {tb.tb_lineno},  {e.__str__()}")

    def set_site_elements(self, site):
        sites_elements = {
            "cambridge": {
                "dictionary_cards": [["div", "dictionary"]],
                "definition_element": ["div", ["def", "ddef_d", "db"]],
                "example_element": ["span", "eg"],
            },
            "collins": {
                "dictionary_cards": [["div", "hom"]],
                "definition_element": ["div", "def"],
                "example_element": ["span", "quote"],
            },
            "macmillan": {
                "dictionary_cards": [["div", "SENSE-CONTENT"]],
                "definition_element": ["span", "DEFINITION"],
                "example_element": ["p", "EXAMPLE"],
            },
            "merriam": {
                "dictionary_cards": [["div", "left-content"]],
                "definition_element": ["span", "dtText"],
                "example_element": ["span", ["ex-sent", "t"]],
            },
            "oxford": {
                "dictionary_cards": [["ol", "senses_multiple"], ["ol", "sense_single"]],
                "definition_element": ["span", "def"],
                "example_element": ["ul", "examples"],
            },
        }
        self.site_elements = sites_elements[site]
