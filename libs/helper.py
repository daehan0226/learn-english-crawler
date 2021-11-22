def get_keyword_key(type_: str) -> str or bool:
    if type_ == "phrasal_verb":
        return type_
    elif type_ == "idiom":
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


def has_valid_args(args):
    types = ["phrasal_verb", "idiom"]
    envs = ["sever", "dev"]
    help_message = f"""
        Please enter
        `python ./main.py type env`
        type must be one of {", ".join(types)}
        env must be one of {", ".join(envs)}
    """
    try:
        if args[1] in types and args[2] in envs:
            return True
        else:
            raise Exception
    except:
        print(help_message)
