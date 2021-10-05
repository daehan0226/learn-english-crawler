import time
import simplejson
from libs.Crawler import Crawler

from crawlers.crawler_cambridge import Crawler_cambridge
from crawlers.crawler_freedictionary import Crawler_freedictionary
from crawlers.crawler_merriam import Crawler_merriam
from crawlers.crawler_oxford import Crawler_oxford

json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


def run_crawler(keyword):
    start_time = time.time()
    crawler = Crawler()
    logging = crawler.logging

    for site, site_data in config["sites"].items():
        try:
            logging.info(f"parsing for {keyword} started from {site}")

            if site == "cambridge":
                continue
                cralwer = Crawler_cambridge()

            elif site == "freedictionary":
                continue
                cralwer = Crawler_freedictionary()

            elif site == "merriam":
                cralwer = Crawler_merriam()

            elif site == "oxford":
                continue
                cralwer = Crawler_oxford()

            cralwer.set_parse_url(site_data, keyword)
            cralwer.parse()
            end_time = time.time()
            logging.debug(
                f"site : {site} parsing finished, parsing time : {end_time - start_time}"
            )
        except:
            pass


if __name__ == "__main__":
    keyword = "work out"
    run_crawler(keyword)
