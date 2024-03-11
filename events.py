import os
import json
from pprint import pp
from urllib.parse import urljoin

import requests as rq

BASE_URL = "http://localhost:8384/rest/"
TOKEN = "" or os.getenv('STAPIKEY')

EVENTS = [
    # "FolderCompletion",
    # "FolderScanProgress",
    # "FolderSummary",
    # "FolderWatchStateChanged",
    "LocalChangeDetected",
    # "LocalIndexUpdated",
    "RemoteChangeDetected",
    # "RemoteIndexUpdated"
]

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
        event_id_last = 0
        while True:
            # print("Starting with EventId", event_id_last)
            r = s.get(
                urljoin(BASE_URL, "events"),
                params={
                    'since': event_id_last,
                    'events': ",".join(EVENTS)
                },
                stream=True
            )
            if r.encoding is None:
                r.encoding = "utf-8"
            for part in r.iter_content(chunk_size=None, decode_unicode=True):
                if not part:
                    continue # skip keepalive
                events = []
                try:
                    events = json.loads(part)
                except json.JsonDecodeError as e:
                    print("Decoding error", e)
                for event in events:
                    pp(event)
                    event_id_last = max(event.get('id', 0), event_id_last)
                    # if event['data']: pass
                    print()

if __name__ == "__main__":
    main()
