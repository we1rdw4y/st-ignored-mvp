import os
from os import path
from itertools import chain
from argparse import ArgumentParser

ap = ArgumentParser()
# ap.add_agrument("folder", action='append')
ap.add_argument("folder")

IGNORES = [
    '.git',
    '.svn',
    '.stfolder'
]

def main(folder=".", **kwargs):
    print("Hello")
    ignores = []
    # current dir check
    current = path.realpath(folder)
    first = (path.dirname(current), [path.basename(current)], None)
    for parent, dirs, _ in chain((first, ), os.walk(folder)):
        if parent in ignores:
            continue
        for directory in dirs:
            #print("dir", directory)
            fullpath = path.join(parent, directory)
            #print("Checking", fullpath)
            for ignore in IGNORES:
                if fullpath.lower().endswith(ignore):
                    ignores.append(fullpath)
                    #print("is itself", ignore)
                    continue
                subpath = path.join(fullpath, ignore)
                if path.dirname(subpath) in ignores:
                    continue
                if path.isdir(subpath):
                    ignores.append(fullpath)
                    #print("has child", ignore)
    # print("Ignores:")
    # for ignore in ignores:
        # print(ignore)
    print("Relpath:")
    for ignore in ignores:
        print(path.relpath(ignore, folder))
    print("Bye.")

if __name__ == "__main__":
    argv = ap.parse_args()
    main(**vars(argv))
