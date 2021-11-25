import sys
import time
import simplejson
from random import uniform
from libs.ApiHandler import ApiHandler
from libs.helper import (
    has_valid_args,
    get_keyword_key,
    replace_space_to_hyphen,
    trim_spaces,
    remove_duplicates,
)

from crawlers.CrawlerPhrasalVerb import CrawlerPhrasalVerb
from crawlers.CrawlerIdiom import CrawlerIdiom

json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


def run_crawler(type_: str, env: str):
    crawler = CrawlerPhrasalVerb() if type_ == "phrasal_verb" else CrawlerIdiom()
    logging = crawler.logging
    logging.info("================Crawler started==============")
    api = ApiHandler(logging, config["api"], env)

    for data in api.get_keywords(type_):
        try:
            keyword = data[get_keyword_key(type_)]
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
