#!/usr/bin/env python3
"""
Strips duplicate author names from titles (e.g. "Uploader - Author - Title.mp4" becomes "Author - Title.mp4")
"""
import argparse
import pathlib
import sys
import os

SEPARATOR = ' - '

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', help='path to read links from')
    args = parser.parse_args()

    path = pathlib.Path(args.path)
    for item in path.iterdir():
        name = str(item)
        split_name = name.split(SEPARATOR)

        newname = ''
        if len(split_name) > 2:
            newname = SEPARATOR.join(split_name[1:])

        if newname:
            print("Renaming %r => %r" % (name, newname), file=sys.stderr)
            os.rename(name, newname)
