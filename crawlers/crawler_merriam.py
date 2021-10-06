import sys

from libs.Crawler import Crawler


class Crawler_merriam(Crawler):
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

            contents = self.parse_by_selectors(
                target="def_boxes", css_selectors=self.dict_boxes
            )

            definitions = []
            examples = []
            for content in contents:
                defnition_elements = self.parse_from_src_by_selector(
                    content,
                    target="definition elements",
                    css_selector=self.definition_element,
                )
                definitions.extend(
                    self.get_text_contents_from_elemets(defnition_elements)
                )

                example_elements = self.parse_from_src_by_selector(
                    content,
                    target="example elements",
                    css_selector=self.example_element,
                )
                examples.extend(self.get_text_contents_from_elemets(example_elements))

            definitions = self.trim_spaces(definitions)
            self.log_parsing_result(len(definitions), len(examples))
            self.upload_parsed_data(self.site, self.keyword, definitions, examples)

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(f"parse except,  {tb.tb_lineno},  {e.__str__()}")
