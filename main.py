import sys
import time
import simplejson
from random import uniform
import urllib.request

from concurrent.futures import ProcessPoolExecutor, as_completed

from libs.api_handler import ApiHandler
from libs.errors import WrongRunCommandError
from libs.helper import (
    get_keyword_key,
    replace_space_to_hyphen,
    trim_spaces,
    remove_duplicates,
)

from crawlers.CrawlerPhrasalVerb import CrawlerPhrasalVerb
from crawlers.CrawlerIdiom import CrawlerIdiom
from libs.logger import get_logger

json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


def run_crawler(logging, env=None, keyword=None, keyword_type=None):
    ## better way?
    if keyword_type == "phrasal_verbs":
        crawler = CrawlerPhrasalVerb()
    elif keyword_type == "idioms":
        crawler = CrawlerIdiom()
    else:
        raise WrongRunCommandError("keyword_type")

    crawler.logging = logging
    # api = ApiHandler(logging, config["api"], env)

    logging.info("================Crawler started==============")

    for keyword in keyword.split(","):
        try:
            sites = []
            definitions = []
            examples = []

            crawler.keyword = replace_space_to_hyphen(keyword)
            dict_urls = crawler.get_urls(config["sites"])

            for dict_url in dict_urls:
                try:
                    crawler.set_site_elements(dict_url["site"])
                    logging.info(
                        f"parsing for {keyword} started from {dict_url['site']}"
                    )
                    start_time = time.time()
                    crawler.url = dict_url["url"]
                    crawler.load()
                    crawler.parse()
                    end_time = time.time()
                    logging.debug(
                        f"site : {dict_url['site']} parsing finished, parsing time : {end_time - start_time}"
                    )
                    time.sleep(uniform(1, 2))
                    sites.append(dict_url["site"])
                    definitions.extend(crawler.definitions)
                    examples.extend(crawler.examples)
                except Exception as e:
                    _, _, tb = sys.exc_info()
                    logging.error(f"{tb.tb_lineno},  {e.__str__()}")

            print(
                keyword,
                keyword_type,
                sites,
                trim_spaces(remove_duplicates(definitions)),
                trim_spaces(remove_duplicates(examples)),
            )
            # api.upload_parsed_data(
            # type_,
            # keyword,
            # sites,
            # trim_spaces(remove_duplicates(definitions)),
            # trim_spaces(remove_duplicates(examples)),
            # )
        except Exception as e:
            _, _, tb = sys.exc_info()
            logging.error(f"{tb.tb_lineno},  {e.__str__()}")

    logging.info("================Crawler finished==============")


if __name__ == "__main__":
    logging = get_logger(config["log_dir"])
    try:
        try:
            kwargs = dict(arg.split("=") for arg in sys.argv[1:])
            run_crawler(logging, **kwargs)
        except TypeError as e:
            raise WrongRunCommandError(e)
    except Exception as e:
        logging.error(e)
