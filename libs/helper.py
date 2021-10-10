import sys
import simplejson
import requests
from datetime import datetime

json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


def get_keywords(logging):
    try:
        result = []
        URL = f'{config["api_address"]}/{config["api_endpoint_keywords"]}'
        res = requests.get(URL)
        phrasal_verbs = res.json()["result"]

        for phrasal_verb in phrasal_verbs:
            verb = phrasal_verb["verb"]
            particle = phrasal_verb["particle"]
            result.append(f"{verb} {particle}")
        logging.info(f"{len(phrasal_verbs)} to crawl ")
        return result
    except Exception as e:
        _, _, tb = sys.exc_info()
        logging.error(f"API get_keywords ERROR {tb.tb_lineno},  {e.__str__()}")
        return []


def get_sites():
    return config["sites"]


def get_verb_particle_from_keyword(keyword):
    return keyword.split(" ", 1)


def get_token(logging):
    try:
        URL = f'{config["api_address"]}/{config["api_endpoint_token"]}/'
        data = {"username": config["username"], "password": config["password"]}
        res = requests.post(URL, data=data)
        return res.json()["result"]["session"]

    except Exception as e:
        _, _, tb = sys.exc_info()
        logging.error(f"API get_token ERROR {tb.tb_lineno},  {e.__str__()}")
        return False


def set_header():
    headers = requests.utils.default_headers()
    headers.update(
        {
            "User-Agent": "My User Agent 1.0",
        }
    )
    return headers


def upload_parsed_data(logging, keyword, sites, definitions, examples):
    try:
        verb, particle = get_verb_particle_from_keyword(keyword)
        URL = f'{config["api_address"]}/{config["api_endpoint_phreal_verb"]}/{verb}'
        data = {
            "dictionaries": sites,
            "particle": particle,
            "definitions": definitions,
            "examples": examples,
            "datetime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
        }
        token = get_token(logging)
        if token:
            headers = {"Authorization": token}
            res = requests.put(URL, data=data, headers=headers)
            return True
    except Exception as e:
        _, _, tb = sys.exc_info()
        logging.error(f"API upload_parsed_data ERROR {tb.tb_lineno},  {e.__str__()}")
        return False


def trim_spaces(sentences):
    result = []
    for sentence in sentences:
        if sentence.startswith(": "):
            sentence = sentence[2:]
            sentence = " ".join(sentence.splitlines())
        result.append(sentence.strip())

    return result


def remove_duplicates(sentences):
    return list(set(sentences)) if sentences else sentences
