import sys

from libs.Crawler import Crawler


class CrawlerCollins(Crawler):
    def __init__(self):
        self.site = "Collins"
        self.dict_boxes = ["div.hom"]
        self.definition_element = "div.def"
        self.example_element = "div.type-example span.quote"

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
                category_element = self.get_an_element_by_selector(dict_box, target="category", css_selector="span.gramGrp.pos")
                category = self.get_text_content_from_elemet(category_element) if category_element else None
                
                if "phrasal verb" == category:
                    defnition_elements = self.get_elements_by_selector(
                        dict_box,
                        target="definition elements",
                        css_selector=self.definition_element,
                    )
                    definitions.extend(
                        self.get_text_contents_from_elemets(defnition_elements)
                    )

                    example_elements = self.get_elements_by_selector(
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
