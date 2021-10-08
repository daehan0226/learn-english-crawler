import time
from libs.Crawler import Crawler
from libs.helper import get_keywords, get_sites, upload_parsed_data

from crawlers.crawler_cambridge import Crawler_cambridge
from crawlers.crawler_merriam import Crawler_merriam
from crawlers.crawler_oxford import Crawler_oxford


def run_crawler(keyword):
    crawler = Crawler()
    logging = crawler.logging
    keywords = [keyword] if keyword else get_keywords()
    dictionary_sites = get_sites()
    for keyword in keywords:
        sites = []
        definitions = []
        examples = []
        for site, site_data in dictionary_sites.items():
            try:
                if site == "cambridge":
                    cralwer = Crawler_cambridge()

                elif site == "merriam":
                    cralwer = Crawler_merriam()

                elif site == "oxford":
                    cralwer = Crawler_oxford()

                logging.info(f"parsing for '{keyword}' started from {site}")
                start_time = time.time()
                cralwer.set_keyword(keyword)
                cralwer.set_parse_url(site_data)
                cralwer.parse()
                end_time = time.time()
                logging.debug(
                    f"site : {site} parsing finished, parsing time : {end_time - start_time}"
                )
                sites.append(site)
                definitions.extend(cralwer.definitions)
                examples.extend(cralwer.examples)
            except:
                pass
        upload_parsed_data(keyword, sites, definitions, examples)


if __name__ == "__main__":
    keyword = None
    run_crawler(keyword)
