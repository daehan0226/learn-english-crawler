from libs.helper import *


def test_remove_duplicates():
    list_with_duplicates = ["a", "b", "b"]
    list_uinuqe = ["a", "b"]

    assert sorted(remove_duplicates(list_with_duplicates)) == sorted(list_uinuqe)


def test_replace_space_to_hyphen():
    string_with_space = "test helper"
    string_with_hyphen = "test-helper"

    assert replace_space_to_hyphen(string_with_space) == string_with_hyphen


def test_separate_by_space():
    string = "test helper"
    separated = ["test", "helper"]

    empty_string = ""

    assert separate_by_space(string) == separated
    assert separate_by_space(empty_string) == False
    assert separate_by_space(None) == False
