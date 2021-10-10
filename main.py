import sys
import time
from libs.Crawler import Crawler
from libs.helper import (
    get_keywords,
    get_sites,
    trim_spaces,
    upload_parsed_data,
    remove_duplicates,
)

from crawlers.CrawlerCambridge import CrawlerCambridge
from crawlers.CrawlerMerriam import CrawlerMerriam
from crawlers.CrawlerOxford import CrawlerOxford
from crawlers.CrawlerMacmillan import CrawlerMacmillan
from crawlers.CrawlerCollins import CrawlerCollins


def run_crawler(keyword):
    crawler = Crawler()
    logging = crawler.logging
    keywords = [keyword] if keyword else get_keywords(logging)
    dictionary_sites = get_sites()
    for keyword in keywords:
        sites = []
        definitions = []
        examples = []
        for site, site_data in dictionary_sites.items():
            try:
                if site == "cambridge":
                    cralwer = CrawlerCambridge()

                elif site == "merriam":
                    cralwer = CrawlerMerriam()

                elif site == "oxford":
                    cralwer = CrawlerOxford()

                elif site == "macmillan":
                    cralwer = CrawlerMacmillan()

                elif site == "collins":
                    cralwer = CrawlerCollins()

                logging.info(f"parsing for '{keyword}' started from {site}")
                start_time = time.time()
                cralwer.set_keyword(keyword)
                cralwer.set_parse_url(site_data)
                cralwer.load()
                cralwer.parse()
                end_time = time.time()
                logging.debug(
                    f"site : {site} parsing finished, parsing time : {end_time - start_time}"
                )
                sites.append(site)
                definitions.extend(cralwer.definitions)
                examples.extend(cralwer.examples)

            except Exception as e:
                _, _, tb = sys.exc_info()
                logging.error(f"{tb.tb_lineno},  {e.__str__()}")
        upload_parsed_data(
            logging,
            keyword,
            sites,
            trim_spaces(remove_duplicates(definitions)),
            trim_spaces(remove_duplicates(examples)),
        )


if __name__ == "__main__":
    keyword = None
    run_crawler(keyword)
