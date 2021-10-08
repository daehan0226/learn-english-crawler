import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from libs.Crawler import Crawler


class Crawler_oxford(Crawler):
    def __init__(self):
        self.site = "Oxford"
        self.dict_boxes = ["ol.senses_multiple", "ol.sense_single"]
        self.definition_element = "span.def"
        self.example_element = "ul.examples > li > span"

    def set_parse_url(self, site_data):
        self.url = site_data["url"] + self.keyword.replace(" ", "-")

    def parse(self):
        try:
            self.logging.debug("parsing started from this url : " + self.url)
            self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, self.dict_boxes[0])
                )
            )
            # self.driver.get(self.url)
            # self.driver.execute_script("location.reload()")

            dict_boxes = self.parse_by_selectors(
                target="def_boxes",
                css_selectors=self.dict_boxes,
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
