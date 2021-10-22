import sys
import requests
from datetime import datetime

from libs.helper import replace_space_to_hyphen


class ApiHandler:
    def __init__(self, logging, config):
        self.logging = logging
        self.api_address = config["address"]
        self.api_endpoints = config["endpoints"]
        self.username = config["username"]
        self.password = config["password"]

    def get_keywords(self):
        try:
            URL = f'{self.api_address}/{self.api_endpoints["keywords"]}'
            res = requests.get(URL)
            phrasal_verbs = res.json()["result"]
            result = [
                f"{phrasal_verb['verb']} {phrasal_verb['particle']}"
                for phrasal_verb in phrasal_verbs
            ]
            self.logging.info(f"{len(phrasal_verbs)} to crawl ")
            return result
        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(f"API get_keywords ERROR {tb.tb_lineno},  {e.__str__()}")
            return []

    def get_token(self):
        try:
            URL = f'{self.api_address}/{self.api_endpoints["token"]}/'
            data = {
                "username": self.username,
                "password": self.password,
            }
            res = requests.post(URL, data=data)
            return res.json()["result"]["session"]

        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(f"API get_token ERROR {tb.tb_lineno},  {e.__str__()}")
            return False

    def upload_parsed_data(self, keyword, sites, definitions, examples):
        try:
            phrasal_verb = replace_space_to_hyphen(keyword)
            URL = f'{self.api_address}/{self.api_endpoints["phrasal_verb"]}/{phrasal_verb}'
            data = {
                "dictionaries": sites,
                "definitions": definitions,
                "examples": examples,
                "datetime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            }
            token = self.get_token()
            if token:
                headers = {"Authorization": token}
                res = requests.put(URL, data=data, headers=headers)
                return True
        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(
                f"API upload_parsed_data ERROR {tb.tb_lineno},  {e.__str__()}"
            )
            return False
