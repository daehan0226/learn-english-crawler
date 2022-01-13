import simplejson
import pytest
from crawlers.crawler_cambridge import CrawlerCambridge
from libs.logger import get_logger


json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


@pytest.fixture
def crawler():
    logging = get_logger(config["log_dir"])
    crawler = CrawlerCambridge(logging)
    return crawler
