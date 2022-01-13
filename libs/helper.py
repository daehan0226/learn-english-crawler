def get_keyword_key(type_: str) -> str or bool:
    if type_ == "phrasal_verbs":
        return "phrasal_verb"
    elif type_ == "idioms":
        return "expression"
    return None


def separate_by_space(keyword):
    try:
        if " " in keyword:
            return keyword.split(" ", 1)
        return False
    except:
        return False


def replace_space_to_hyphen(string):
    return string.replace(" ", "-")


# TODO - check sentence is string and not empty string
def trim_spaces(sentences):
    result = []
    for sentence in sentences:
        if sentence.startswith(": "):
            sentence = sentence[2:]
            sentence = " ".join(sentence.splitlines())
        result.append(sentence.strip())

    return result


def remove_duplicates(sentences):
    if isinstance(sentences, list):
        return list(set(sentences)) if sentences else sentences
    return False


def filter_sentences_if_not_include_keyword(sentences, keyword):
    return [sentence for sentence in sentences if keyword in sentence]
