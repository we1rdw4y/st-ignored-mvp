import os
import json
from os import path
from pprint import pp
from urllib.parse import urljoin

import requests as rq

BASE_URL = "http://localhost:8384/rest/"
TOKEN = os.getenv('STAPIKEY') or ""
FOLDER = os.getenv('STFOLDERID') or ""

REPOS = [
    ".git",
    ".svn",
    ".cvs",
    ".hg",
    ",v"
]

def repo_root(fpath):
    pass

def repo_under(fpath):
    while fpath:
        if repo_is(fpath):
            return True
        fpath = path.dirname(fpath)
    return False

def repo_is(fpath):
    for repo in REPOS:
        if path.basename(fpath) != repo and pathrefpath.endswith(repo):
            return True
    return False

def relative(repos, to):
    for repo in repos:
        yield path.relpath(repo, start=to)

def folder_repos(sess, root):
    # folders = []
    repos = []
    r = sess.get(urljoin(BASE_URL, "system/browse"), params={'current': root + "/"})
    fl = r.json()
    for f in fl:
        # print("f:", f, "bn:", path.basename(f), "dn:", path.dirname(f))
        if path.basename(f) != ".git" and f.endswith(".git"):
            repos.append(f)
            # print("is host-repo")
            continue
        if path.basename(f) == ".git":
            repos.append(path.dirname(f))
            # print("contains repo")
            continue
        # folders.append(f)
        cr = folder_repos(sess, f)
        # folders.extend(cf)
        repos.extend(cr)
    return repos

IGNORES = []

def main():
    print("Starting...")
    with rq.Session() as s:
        s.headers = {
            "Content-type": "text/json",
            "Authorization": "Bearer " + TOKEN
        }
        r = s.get(urljoin(BASE_URL, "config/folders/" + FOLDER))
        o = r.json()
        root = o.get('path', "/")
        repos = folder_repos(s, root)
        IGNORES.extend(relative(repos, root))
        lastid = 0
        while True:
            pp(IGNORES)
            r = s.get(
                urljoin(BASE_URL, "events/disk"),
                params={'folder': FOLDER, 'since': lastid},
                stream=True
            )
            for piece in r.iter_content(chunk_size=None, decode_unicode=True):            
                if not piece:
                    continue
                events = []
                try:
                    events = json.loads(piece)
                except json.JsonDecodeError as e:
                    print("Decoding err", e)
                for event in events:
                    lastid = max(event.get('id', 0), lastid)
                    if event['type'] != "LocalChangeDetected":
                        continue
                    data = event['data']
                    if data['action'] != "modified":
                        # ignore deletions
                        continue
                    if data['path'] in IGNORES:
                        print("Already ignored")
                        continue
                    print("Bullshittery started")
                    # ev_path = data['path']
                    # addition = False
                    # while ev_path:
                        # if path.basename(ev_path).endswith(".git"):
                            # addition = True
                            # print("seems vcs folder")
                            # break
                        # ev_path = path.dirname(ev_path)
                    ev_path = repo_path(data['path'])
                    if not addition:
                        print("abort, not vcs")
                        continue
                    for ignore in IGNORES:
                        if path.commonpath((data['path'], ignore)) == ignore:
                            addition = False
                            print("already ignored")
                            break
                    if addition:
                        print("Adding to ignores", data['path'])
                        IGNORES.append(data['path'])

if __name__ == "__main__":
    main()
