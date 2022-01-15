import sys
import simplejson
import asyncio
import aiohttp


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


async def async_load_site(session, crawl):
    await crawl.load(session)


async def load_all_sites(crawlers):
    async with aiohttp.ClientSession() as session:
        load_list = []
        for crawl in crawlers:
            load = asyncio.ensure_future(async_load_site(session, crawl))
            load_list.append(load)

        await asyncio.gather(*load_list, return_exceptions=True)


def run_crawler(logging, env=None, keyword=None, keyword_type=None):
    check_run_cmd(env, keyword_type)

    keywords = (
        ApiHandler.get_keywords(env, keyword_type)
        if keyword is None
        else keyword.split(",")
    )

    crawler_objects = [
        CrawlerCambridge,
        CrawlerCollins,
        CrawlerMacmillan,
        CrawlerMerriam,
        CrawlerOxford,
    ]

    logging.info("=== Setting Crawlers==============")
    crawlers = []
    for keyword in keywords:
        definitions = []
        examples = []

        for crawler_object in crawler_objects:
            crawler = crawler_object(logging)
            crawler.keyword = keyword
            crawler.keyword_type = keyword_type
            logging.debug(f"site: {crawler.site}, keyword : {crawler.keyword}")
            crawler.set_parse_url()
            crawlers.append(crawler)

    logging.debug("async loading sites")
    asyncio.get_event_loop().run_until_complete(load_all_sites(crawlers))

    logging.debug("parsing definitions and examples")
    for crawler in crawlers:
        crawler.parse()
        definitions.extend(crawler.definitions)
        examples.extend(crawler.examples)

        # crawler.print_data()

    logging.info("==Crawlers finished==============")

    # Upload


if __name__ == "__main__":
    logging = get_logger(config["log_dir"])
    try:
        kwargs = dict(arg.split("=") for arg in sys.argv[1:])
        run_crawler(logging, **kwargs)
    except Exception as e:
        logging.error(e)
