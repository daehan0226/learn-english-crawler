def test_load(crawler):
    crawler.load()

    assert "html" in crawler.doc
