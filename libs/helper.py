import simplejson
import requests
from datetime import datetime


json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)


def get_keywords():
    result = []
    URL = f'{config["api_address"]}/phrasal-verbs/dictionary-empty'
    res = requests.get(URL)

    for phrasal_verb in res.json()["result"]:
        result.append(f"{phrasal_verb['verb']} {phrasal_verb['particle']}")

    return result


def get_sites():
    return config["sites"]


def get_verb_particle_from_keyword(keyword):
    return keyword.split(" ", 1)


def get_token():
    URL = f'{config["api_address"]}/sessions/'
    data = {"username": config["username"], "password": config["password"]}
    res = requests.post(URL, data=data)
    return res.json()["result"]


def upload_parsed_data(keyword, sites, definitions, examples):
    try:
        verb, particle = get_verb_particle_from_keyword(keyword)
        URL = f'{config["api_address"]}/phrasal-verbs/{verb}'
        data = {
            "dictionaries": sites,
            "particle": particle,
            "definitions": definitions,
            "examples": examples,
            "datetme": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
        }
        headers = {"Authorization": get_token()}
        res = requests.put(URL, data=data, headers=headers)
        return True
    except:
        return False
