from libs.api_handler import ApiHandler


def test_get_keywords():

    phrasal_verbs_keywords = ApiHandler.get_keywords("dev", "phrasal_verbs")
    idioms_keywords = ApiHandler.get_keywords("dev", "idioms")

    assert phrasal_verbs_keywords == ["put up with"]
    assert idioms_keywords == ["pop the question"]
    # assert isinstance(idiom_keywords, list)
