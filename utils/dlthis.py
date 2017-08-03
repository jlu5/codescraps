#!/usr/bin/env python3
"""
Fetches a newline-separated list of audio links from a file, and downloads them using youtube-dl.

If no arguments are given, this program will try to fetch files from dlthis.txt, in the folder where the script was executed.
"""
from __future__ import print_function

import argparse
import youtube_dl
import sys
import os
try:
    import concurrent
    import concurrent.futures
except ImportError:
    concurrent = None

if sys.version_info[0] < 3:
    # Use io.open() on Python 2 for encoding support.
    from io import open

YTDL_OPTS = {
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
    parser.add_argument("-j", "--jobs", help="amount of threads to use (requires Python 3, defaults to amount of CPU cores)", type=int, default=os.cpu_count() or 1)
    args = parser.parse_args()

    if args.playlist:
        if args.author:
            YTDL_OPTS['outtmpl'] = '%(playlist_title)s/%(playlist_index)s %(uploader)s - %(title)s-%(id)s.%(ext)s'
        else:
            YTDL_OPTS['outtmpl'] = '%(playlist_title)s/%(playlist_index)s %(title)s-%(id)s.%(ext)s'
    elif args.author:
        YTDL_OPTS['outtmpl'] = '%(uploader)s - %(title)s-%(id)s.%(ext)s'

    with open(args.textfile, 'r', encoding=args.encoding) as f:
        files = [link.strip() for link in f.readlines()]
        # Filter out empty lines and those starting with # (comments)
        files = [link for link in files if link and not link.startswith('#')]

        print("Downloading: %s" % files, file=sys.stderr)
        with youtube_dl.YoutubeDL(YTDL_OPTS) as ydl:
            if concurrent is not None and args.jobs > 1:
                import threading
                def download_wrapper(link):
                    print('Downloading file %s in thread %s' % (link, threading.current_thread().name), file=sys.stderr)
                    return ydl.download([link])

                with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
                    for future in pool.map(download_wrapper, files):
                        # We need to iterate over the map() object for it to actually run.
                        pass
            else:
                print('Disabling multithreading mode (needs Python 3 and job count > 1')
                ydl.download(files)
