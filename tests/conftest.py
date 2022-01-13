import simplejson
import pytest
from libs.api_handler import ApiHandler
from crawlers.crawler import Crawler
from libs.logger import get_logger


json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


@pytest.fixture
def crawler():
    crawler = Crawler()
    crawler.set_keyword("help out")
    crawler.set_parse_url(
        {"url": "https://dictionary.cambridge.org/dictionary/english/"}
    )
    return crawler


@pytest.fixture
def apiHandler():
    apiHandler = ApiHandler(get_logger(config["log_dir"]), config["api"])
    return apiHandler
