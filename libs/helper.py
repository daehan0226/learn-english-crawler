import requests


def get_keywords(config):
    result = []
    URL = f'{config["api_address"]}/dictionary-empty'
    res = requests.get(URL)
    result = res.json()["result"]
    return result
