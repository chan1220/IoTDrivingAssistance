import requests
import json
from urllib.parse import urljoin


class db_requester():
    def __init__(self, host):
        self.__host = host

    def request(self, path, param):
        url = urljoin(self.__host, path)
        r = requests.post(url, json=param)
        return json.loads(r.text)