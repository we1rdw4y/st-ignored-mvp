import os
import json
from pprint import pp
from urllib.parse import urljoin

import requests as rq

BASE_URL = "http://localhost:8384/rest/"
TOKEN = "" or os.getenv('STAPIKEY')
FOLDER = "" or os.getenv('STFOLDERID')

def folders_read(session):
    pass

def folder_walk(session, folder):
    pass

def folder_is_unwanted(folder, path):
    pass

def main():
    print("Starting...")
    with rq.Session() as s:
        s.headers = {
            "Content-type": "text/json",
            "Authorization": "Bearer " + TOKEN
        }
        r = s.get(urljoin(BASE_URL, "db/ignores"), params={'folder': FOLDER})
        pprint(r.json())

if __name__ == "__main__":
    main()
