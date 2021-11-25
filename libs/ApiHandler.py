import sys
import requests
from datetime import datetime


class ApiHandler:
    def __init__(self, logging, config, env):
        self.logging = logging
        self.api_address = config["address"]
        self.api_endpoints = config["endpoints"]
        self.username = config["username"]
        self.password = config["password"]
        self.env = env

    def get_keywords(self, type_):
        if self.env == "dev":
            keywords = {
                "phrasal_verbs": [{"phrasal_verb": "put up with"}],
                "idioms": [{"expression": "pop the question"}],
            }
            return keywords[type_]
        try:
            URL = f'{self.api_address}/{self.api_endpoints["keyword"][type_]}'
            res = requests.get(URL)
            result = res.json()["result"]
            self.logging.info(f"{len(result)} to crawl ")
            return result
        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(f"API get_keywords ERROR {tb.tb_lineno},  {e.__str__()}")
            return None

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
            return None

    def upload_parsed_data(self, type_, keyword, sites, definitions, examples):
        if self.env == "dev":
            return True
        try:
            print(type_, keyword, sites, len(definitions), len(examples))
            URL = f"{self.api_address}/{self.api_endpoints[type_]}/{keyword}"
            data = {
                "dictionaries": sites,
                "definitions": definitions,
                "examples": examples,
                "datetime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            }
            token = self.get_token()
            if token:
                res = requests.put(URL, data=data, headers={"Authorization": token})
                return True
        except Exception as e:
            _, _, tb = sys.exc_info()
            self.logging.error(
                f"API upload_parsed_data ERROR {tb.tb_lineno},  {e.__str__()}"
            )
            return None
