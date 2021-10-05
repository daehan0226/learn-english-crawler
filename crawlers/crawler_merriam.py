import sys

from libs.Crawler import Crawler


class Crawler_merriam(Crawler):
    def set_parse_url(self, site_data, phrasal_verb):
        self.url = site_data["url"] + phrasal_verb.replace(" ", "-")

    def trim_sentences(self, sentences):
        result = []
        for sentence in sentences:
            if sentence.startswith(": "):
                sentence = sentence[2:]
            result.append(sentence)
        return result

    def parse(self):
        try:
            self.logging.debug("parsing started from this url : " + self.url)
            self.driver.get(self.url)

            contents = self.parse_by_selectors(
                target="def_boxes", css_selectors=["div.left-content"]
            )

            definitions = []
            examples = []
            for content in contents:
                defnition_elements = self.parse_from_src_by_selector(
                    content,
                    target="definition elements",
                    css_selector="span.dtText",
                )
                definitions.extend(
                    self.get_text_contents_from_elemets(defnition_elements)
                )

                example_elements = self.parse_from_src_by_selector(
                    content,
                    target="example elements",
                    css_selector="span.ex-sent.t",
                )
                examples.extend(self.get_text_contents_from_elemets(example_elements))

            definitions = self.trim_sentences(definitions)
            print(definitions, examples)

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(f"parse except,  {tb.tb_lineno},  {e.__str__()}")
