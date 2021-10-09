import sys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from libs.Crawler import Crawler


class CrawlerMerriam(Crawler):
    def __init__(self):
        self.site = "Merriam"
        self.dict_boxes = ["div.left-content"]
        self.definition_element = "span.dtText"
        self.example_element = "span.ex-sent.t"

    def set_parse_url(self, site_data):
        self.url = site_data["url"] + self.keyword.replace(" ", "-")

    def trim_spaces(self, sentences):
        result = []
        for sentence in sentences:
            if sentence.startswith(": "):
                sentence = sentence[2:]
            sentence = sentence.strip()
            result.append(sentence)
        return result

    def parse(self):
        try:
            self.logging.debug("parsing started from this url : " + self.url)
            self.driver.get(self.url)
            self.driver.execute_script("location.reload()")
            contents = self.parse_by_selectors(
                target="def_boxes", css_selectors=self.dict_boxes
            )

            definitions = []
            examples = []
            for content in contents:
                defnition_elements = self.get_elements_by_selector(
                    content,
                    target="definition elements",
                    css_selector=self.definition_element,
                )
                definitions.extend(
                    self.get_text_contents_from_elemets(defnition_elements)
                )

                example_elements = self.get_elements_by_selector(
                    content,
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
