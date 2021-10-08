import sys

from libs.Crawler import Crawler


class Crawler_cambridge(Crawler):
    def __init__(self):
        self.site = "Cambridge"
        self.dict_boxes = ["div.def-block.ddef_block"]
        self.definition_element = "div.def.ddef_d"
        self.example_element = "span.eg.deg"

    def set_parse_url(self, site_data):
        self.url = site_data["url"] + self.keyword.replace(" ", "-")

    def parse(self):
        try:
            self.logging.debug("parsing started from this url : " + self.url)
            self.driver.get(self.url)

            dict_boxes = self.parse_by_selectors(
                target="def_boxes", css_selectors=self.dict_boxes
            )
            definitions = []
            examples = []
            for dict_box in dict_boxes:
                defnition_elements = self.parse_from_src_by_selector(
                    dict_box,
                    target="definition elements",
                    css_selector=self.definition_element,
                )
                definitions.extend(
                    self.get_text_contents_from_elemets(defnition_elements)
                )

                example_elements = self.parse_from_src_by_selector(
                    dict_box,
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
