import sys
import time
import simplejson
from random import uniform
from libs.ApiHandler import ApiHandler
from libs.Crawler import Crawler
from libs.helper import (
    filter_sentences_if_not_include_keyword,
    separate_by_space,
    trim_spaces,
    remove_duplicates,
)

from crawlers.CrawlerCambridge import CrawlerCambridge
from crawlers.CrawlerMerriam import CrawlerMerriam
from crawlers.CrawlerOxford import CrawlerOxford
from crawlers.CrawlerMacmillan import CrawlerMacmillan
from crawlers.CrawlerCollins import CrawlerCollins


json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


def run_crawler():
    crawler = Crawler()
    logging = crawler.logging
    logging.info("================Crawler started==============")
    api = ApiHandler(logging, config["api"])
    for keyword in api.get_keywords():
        sites = []
        definitions = []
        examples = []
        _, particle = separate_by_space(keyword)
        for site, site_data in config["sites"].items():
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

                logging.info(f"parsing for {keyword} started from {site}")
                start_time = time.time()
                cralwer.set_keyword(keyword)
                cralwer.set_parse_url(site_data)
                cralwer.load()
                cralwer.parse()
                end_time = time.time()
                logging.debug(
                    f"site : {site} parsing finished, parsing time : {end_time - start_time}"
                )
                time.sleep(uniform(1, 2))
                sites.append(site)
                definitions.extend(cralwer.definitions)
                examples.extend(
                    filter_sentences_if_not_include_keyword(cralwer.examples, particle)
                )
            except Exception as e:
                _, _, tb = sys.exc_info()
                logging.error(f"{tb.tb_lineno},  {e.__str__()}")
        api.upload_parsed_data(
            keyword,
            sites,
            trim_spaces(remove_duplicates(definitions)),
            trim_spaces(remove_duplicates(examples)),
        )

    logging.info("================Crawler finished==============")


if __name__ == "__main__":
    run_crawler()
