def test_get_keywords(apiHandler):
    phrasal_verb_keywords = apiHandler.get_keywords("phrasal_verb")
    # idiom_keywords = apiHandler.get_keywords("idiom")

    assert isinstance(phrasal_verb_keywords, list)
    # assert isinstance(idiom_keywords, list)


def test_get_token(apiHandler):
    token = apiHandler.get_token()

    assert isinstance(token, str)
