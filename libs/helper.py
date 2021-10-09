import simplejson
import requests
from datetime import datetime
import re


json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


def get_keywords():
    result = []
    URL = f'{config["api_address"]}/{config["api_endpoint_keywords"]}'
    res = requests.get(URL)

    for phrasal_verb in res.json()["result"]:
        result.append(f"{phrasal_verb['verb']} {phrasal_verb['particle']}")

    return result


def get_sites():
    return config["sites"]


def get_verb_particle_from_keyword(keyword):
    return keyword.split(" ", 1)


def get_token():
    URL = f'{config["api_address"]}/{config["api_endpoint_token"]}/'
    data = {"username": config["username"], "password": config["password"]}
    res = requests.post(URL, data=data)
    return res.json()["result"]["session"]


def set_header():
    headers = requests.utils.default_headers()
    headers.update(
        {
            "User-Agent": "My User Agent 1.0",
        }
    )
    return headers


def upload_parsed_data(keyword, sites, definitions, examples):
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
        headers = {"Authorization": get_token()}
        res = requests.put(URL, data=data, headers=headers)
        return True
    except Exception as e:
        print(e)
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
