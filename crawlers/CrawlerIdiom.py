import sys
from libs.Crawler import Crawler


class CrawlerIdiom(Crawler):
    def __init__(self):
        self.definitions = []
        self.examples = []

    def _extract_dictionary_url(self, string):
        return string.replace("/url?q=", "").split("&")[0]

    def _filter_dictionary_urls(self, sites, links):
        result = []
        for link in links:
            if any(ele in link["href"] for ele in sites.keys()):
                result.append(self._extract_dictionary_url(link["href"]))
        return result

    def _set_url_if_includes_all_eles_in_keyword(self, sites, links):
        reuslt = []
        for link in links:
            keyword_in_link = link.split("/")[-1]
            for site, site_data in sites.items():
                if site in link and all(
                    ele in keyword_in_link for ele in self.keyword.split("-")
                ):
                    reuslt.append(
                        {"site": site, "url": f"{site_data['url']}{keyword_in_link}"}
                    )
        return reuslt

    def _remove_duplicates_site_url(self, site_urls):
        sites = []
        result = []
        for site_data in site_urls:
            if site_data["site"] in sites:
                pass
            else:
                sites.append(site_data["site"])
                result.append(site_data)
        return result

    def _get_candidate_urls(self, candidate_count=50):
        url_crawler = Crawler()
        url_crawler.url = f"https://www.google.com/search?q=idiom {self.keyword} dictionary meaning&num={candidate_count}"
        url_crawler.load()
        return url_crawler.doc.find_all("a")

    def _get_urls(self, sites):
        candidate_urls = self._get_candidate_urls()
        dictionary_urls = self._filter_dictionary_urls(sites, candidate_urls)
        urls_with_keyword = self._set_url_if_includes_all_eles_in_keyword(
            sites, dictionary_urls
        )
        return self._remove_duplicates_site_url(urls_with_keyword)

    def get_urls(self, sites):
        return self._get_urls(sites)

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
