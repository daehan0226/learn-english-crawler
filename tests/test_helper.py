from libs.helper import *


def test_remove_duplicates():
    list_with_duplicates = ["a", "b", "b"]
    list_unique = ["a", "b"]

    assert sorted(remove_duplicates(list_with_duplicates)) == sorted(list_unique)
    assert remove_duplicates("assf") == False


def test_replace_space_to_hyphen():
    string_with_space = "test helper"
    string_with_hyphen = "test-helper"

    assert replace_space_to_hyphen(string_with_space) == string_with_hyphen


def test_separate_by_space():
    string = "test helper"
    separated = ["test", "helper"]

    assert separate_by_space(string) == separated
    assert separate_by_space("") == False
    assert separate_by_space(None) == False


def test_filter_sentences_if_not_include_keyword():
    sentences = ["as df gh", "qw rt yu"]
    keyword = "as"

    assert filter_sentences_if_not_include_keyword(sentences, keyword) == ["as df gh"]
