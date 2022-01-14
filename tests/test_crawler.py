def test_set_header(crawler):
    assert crawler._set_header()["User-Agent"]


def test_set_keyword(crawler):
    crawler.keyword = "put up with"

    assert crawler.keyword == "put-up-with"


def test_set_parse_url(crawler):
    crawler.keyword = "put up with"
    crawler.set_parse_url()

    assert (
        crawler.parse_url
        == "https://dictionary.cambridge.org/dictionary/english/put-up-with"
    )


def test_load(crawler):
    crawler.keyword = "put up with"
    crawler.set_parse_url()
    crawler.load()

    assert "html" in crawler._doc
