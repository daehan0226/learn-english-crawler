import sys
import simplejson


from libs.api_handler import ApiHandler
from libs.helper import (
    check_run_cmd,
    trim_spaces,
    remove_duplicates,
)

from crawlers.crawler_cambridge import CrawlerCambridge
from crawlers.crawler_collins import CrawlerCollins
from crawlers.crawler_macmillan import CrawlerMacmillan
from crawlers.crawler_merriam import CrawlerMerriam
from crawlers.crawler_oxford import CrawlerOxford

from libs.logger import get_logger

json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


def run_crawler(logging, env=None, keyword=None, keyword_type=None):
    check_run_cmd(env, keyword_type)

    SiteCrawlers = [
        CrawlerCambridge,
        CrawlerCollins,
        CrawlerMacmillan,
        CrawlerMerriam,
        CrawlerOxford,
    ]

    try:
        keywords = (
            ApiHandler.get_keywords(env, keyword_type)
            if keyword is None
            else keyword.split(",")
        )

        for keyword in keywords:
            definitions = []
            examples = []
            for SiteCrawler in SiteCrawlers:
                crawler = SiteCrawler(logging)
                crawler.keyword = keyword
                logging.debug(
                    f"site: {crawler.get_site()}, keyword : {crawler.keyword}"
                )
                crawler.set_url()
                logging.debug(f"Loading {crawler.get_parse_url()} for {keyword}")
                crawler.load()
                crawler.parse()

                definitions.extend(crawler.get_definitions())
                examples.extend(crawler.get_examples())

            print(definitions, examples)
        logging.info("==Crawler finished==============")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    logging = get_logger(config["log_dir"])
    try:
        kwargs = dict(arg.split("=") for arg in sys.argv[1:])
        run_crawler(logging, **kwargs)
    except Exception as e:
        logging.error(e)
