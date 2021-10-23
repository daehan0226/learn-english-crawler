def test_set_header(crawler):
    assert crawler.set_header()["User-Agent"]


def test_load(crawler):
    crawler.load()

    assert "html" in crawler.doc


def test_set_keyword(crawler):
    crawler.set_keyword("test out")

    assert crawler.keyword == "test-out"


def test_set_url(crawler):
    crawler.set_keyword("test out")
    crawler.set_parse_url({"url": "http://test.com/"})

    assert crawler.url == "http://test.com/test-out"
