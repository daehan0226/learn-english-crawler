import pytest
from libs.Crawler import Crawler


@pytest.fixture
def crawler():
    crawler = Crawler()
    crawler.set_keyword("help out")
    crawler.set_parse_url(
        {"url": "https://dictionary.cambridge.org/dictionary/english/"}
    )
    return crawler
