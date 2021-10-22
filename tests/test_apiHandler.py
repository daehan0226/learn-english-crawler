def test_get_keywords(apiHandler):
    keywords = apiHandler.get_keywords()

    assert isinstance(keywords, list)


def test_get_token(apiHandler):
    token = apiHandler.token()

    assert isinstance(token, str)
