import sys
import time
import simplejson
from random import uniform
from libs.ApiHandler import ApiHandler
from libs.Crawler import Crawler
from libs.helper import has_valid_args, get_keyword_key, trim_spaces, remove_duplicates

from crawlers.CrawlerCambridge import CrawlerCambridge
from crawlers.CrawlerMerriam import CrawlerMerriam
from crawlers.CrawlerOxford import CrawlerOxford
from crawlers.CrawlerMacmillan import CrawlerMacmillan
from crawlers.CrawlerCollins import CrawlerCollins


json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


def run_crawler(type_: str, env: str):
    crawler = Crawler()
    logging = crawler.logging
    logging.info("================Crawler started==============")
    api = ApiHandler(logging, config["api"], env)

    for data in api.get_keywords(type_):
        try:
            keyword = data[get_keyword_key(type_)]
            sites = []
            definitions = []
            examples = []
            for site, site_data in config["sites"].items():
                try:
                    if site == "cambridge":
                        crawler = CrawlerCambridge()

                    elif site == "merriam":
                        crawler = CrawlerMerriam()

                    elif site == "oxford":
                        crawler = CrawlerOxford()

                    elif site == "macmillan":
                        crawler = CrawlerMacmillan()

                    elif site == "collins":
                        crawler = CrawlerCollins()

                    logging.info(f"parsing for {keyword} started from {site}")
                    start_time = time.time()
                    crawler.set_keyword(keyword)
                    crawler.set_parse_url(site_data)
                    crawler.load()
                    crawler.parse()
                    end_time = time.time()
                    logging.debug(
                        f"site : {site} parsing finished, parsing time : {end_time - start_time}"
                    )
                    time.sleep(uniform(1, 2))
                    sites.append(site)
                    definitions.extend(crawler.definitions)
                    examples.extend(crawler.examples)
                except Exception as e:
                    _, _, tb = sys.exc_info()
                    logging.error(f"{tb.tb_lineno},  {e.__str__()}")

            api.upload_parsed_data(
                type_,
                keyword,
                sites,
                trim_spaces(remove_duplicates(definitions)),
                trim_spaces(remove_duplicates(examples)),
            )
        except Exception as e:
            _, _, tb = sys.exc_info()
            logging.error(f"{tb.tb_lineno},  {e.__str__()}")

    logging.info("================Crawler finished==============")


if __name__ == "__main__":
    if has_valid_args(sys.argv):
        run_crawler(sys.argv[1], sys.argv[2])
