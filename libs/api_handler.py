import sys
import requests
import simplejson
from datetime import datetime

json_config = open("./config/config.json").read()
config = simplejson.loads(json_config)
api_config = config["api"]


class ApiHandler:
    _api_address = api_config["address"]
    _api_endpoints = api_config["endpoints"]
    _username = api_config["username"]
    _password = api_config["password"]

    @classmethod
    def get_keywords(cls, env, type_):
        if env == "server":
            try:
                URL = f'{cls._api_address}/{cls._api_endpoints["keyword"][type_]}'
                res = requests.get(URL)
                result = res.json()["result"]
                return result
            except Exception as e:
                _, _, tb = sys.exc_info()
                raise Exception(
                    f"API get_keywords ERROR {tb.tb_lineno},  {e.__str__()}"
                )
        elif env == "dev":
            keywords = {"phrasal_verbs": "put up with", "idioms": "pop the question"}
            return [keywords[type_]]
        else:
            return []

    @classmethod
    def get_token(cls):
        try:
            URL = f'{cls._api_address}/{cls._api_endpoints["token"]}/'
            data = {
                "username": cls._username,
                "password": cls._password,
            }
            res = requests.post(URL, data=data)
            return res.json()["result"]["session"]

        except Exception as e:
            _, _, tb = sys.exc_info()
            raise Exception(f"API get_token ERROR {tb.tb_lineno},  {e.__str__()}")

    @classmethod
    def upload_parsed_data(cls, env, type_, keyword, sites, definitions, examples):
        if env == "dev":
            print(type_, keyword, sites, definitions, examples)
        elif env == "server":
            try:
                URL = f"{cls._api_address}/{cls._api_endpoints[type_]}/{keyword}"
                data = {
                    "dictionaries": sites,
                    "definitions": definitions,
                    "examples": examples,
                    "datetime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                }
                token = cls.get_token()
                if token:
                    requests.put(URL, data=data, headers={"Authorization": token})
            except Exception as e:
                _, _, tb = sys.exc_info()
                raise Exception(f"API get_token ERROR {tb.tb_lineno},  {e.__str__()}")
