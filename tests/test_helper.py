from libs.helper import *


def test_get_keyword_key():
    assert get_keyword_key("phrasal_verb") == "phrasal_verb"
    assert get_keyword_key("idiom") == "expression"


def test_remove_duplicates():
    assert sorted(remove_duplicates(["a", "b", "b"])) == sorted(["a", "b"])
    assert remove_duplicates("assf") == False


def test_replace_space_to_hyphen():
    assert replace_space_to_hyphen("test helper") == "test-helper"


def test_separate_by_space():
    assert separate_by_space("test helper") == ["test", "helper"]
    assert separate_by_space("") == False
    assert separate_by_space(None) == False


def test_filter_sentences_if_not_include_keyword():
    assert filter_sentences_if_not_include_keyword(["as df gh", "qw rt yu"], "as") == [
        "as df gh"
    ]
