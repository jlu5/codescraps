#!/usr/bin/env python3
"""
Fetches a newline-separated list of audio links from a file, and downloads them using youtube-dl.

If no arguments are given, this program will try to fetch files from dlthis.txt, in the folder where the script was executed.
"""

import argparse
import youtube_dl
import sys

ydl_opts = {
    # Fetch only audio
    'format': 'bestaudio/best',
    'ignoreerrors': True,
    # Workaround for SSL certificate verification failing on Windows?!
    'nocheckcertificate': True,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('textfile', nargs='?', help='text file to read links from', default='dlthis.txt')
    parser.add_argument('--encoding', '-e', nargs='?', help='sets the file encoding', default='utf-8')
    args = parser.parse_args()

    with open(args.textfile, 'r', encoding=args.encoding) as f:
        files = [link.strip() for link in f.readlines()]
        print("Downloading: %s" % files, file=sys.stderr)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(files)