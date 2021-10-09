import sys

from libs.Crawler import Crawler


class crawlerMacmillan(Crawler):
    def __init__(self):
        self.site = "Macmillan"
        self.definition_element = "span.DEFINITION"
        self.example_element = "p.EXAMPLE"

    def set_parse_url(self, site_data):
        self.url = site_data["url"] + self.keyword.replace(" ", "-")

    def parse(self):
        try:
            self.logging.debug("parsing started from this url : " + self.url)
            self.driver.get(self.url)

            definitions = []
            examples = []
            defnition_elements = self.parse_from_src_by_selector(
                self.driver,
                target="definition elements",
                css_selector=self.definition_element,
            )
            definitions.extend(
                self.get_text_contents_from_elemets(defnition_elements)
            )

            example_elements = self.parse_from_src_by_selector(
                self.driver,
                target="example elements",
                css_selector=self.example_element,
            )
            examples.extend(self.get_text_contents_from_elemets(example_elements))

            self.definitions = self.remove_duplicates(definitions)
            self.examples = self.filter_if_not_include_keyword(examples)
            self.log_parsing_result(len(self.definitions), len(self.examples))

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(f"parse except,  {tb.tb_lineno},  {e.__str__()}")
