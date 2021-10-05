import sys

from libs.Crawler import Crawler


class Crawler_oxford(Crawler):
    def set_parse_url(self, site_data, phrasal_verb):
        self.url = site_data["url"] + phrasal_verb.replace(" ", "-")

    def parse(self):
        try:
            self.logging.debug("parsing started from this url : " + self.url)
            self.driver.get(self.url)

            dict_boxes = self.parse_by_selectors(
                target="def_boxes", css_selectors=["div.def-block.ddef_block"]
            )
            definitions = []
            examples = []
            for dict_box in dict_boxes:
                defnition_elements = self.parse_from_src_by_selector(
                    dict_box,
                    target="definition elements",
                    css_selector="div.def.ddef_d",
                )
                definitions.extend(
                    self.get_text_contents_from_elemets(defnition_elements)
                )

                example_elements = self.parse_from_src_by_selector(
                    dict_box, target="example elements", css_selector="span.eg.deg"
                )
                examples.extend(self.get_text_contents_from_elemets(example_elements))

            print(definitions, examples)

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(f"parse except,  {tb.tb_lineno},  {e.__str__()}")
