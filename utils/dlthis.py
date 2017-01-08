#!/usr/bin/env python3
"""
Fetches a newline-separated list of audio links from a file, and downloads them using youtube-dl.

If no arguments are given, this program will try to fetch files from dlthis.txt, in the folder where the script was executed.
"""
from __future__ import print_function

import argparse
import youtube_dl
import sys

if sys.version_info[0] < 3:
	# Use io.open() on Python 2 for encoding support.
	from io import open

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
    parser.add_argument('--playlist', '-p', action='store_true', help='downloads in playlist mode (output in separate folder, with item number and author in filenames)')
    parser.add_argument('--author', '-a', action='store_true', help='stores author name in output filename')
    args = parser.parse_args()

    if args.playlist:
        ydl_opts['outtmpl'] = '%(uploader)s - %(playlist_title)s/%(playlist_index)s %(uploader)s - %(title)s-%(id)s.%(ext)s'
    elif args.author:
        ydl_opts['outtmpl'] = '%(uploader)s - %(title)s-%(id)s.%(ext)s'

    with open(args.textfile, 'r', encoding=args.encoding) as f:
        files = [link.strip() for link in f.readlines()]
        print("Downloading: %s" % files, file=sys.stderr)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(files)
