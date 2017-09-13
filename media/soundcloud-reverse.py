#!/usr/bin/env python3
"""
Returns the URL of a SoundCloud track given its ID (reverse lookup).

This requires a SoundCloud Client ID (specified via command line argument --client-id).
Otherwise, it will attempt to fetch a Client ID from youtube-dl, if it is installed.
"""

import urllib.request
import json
import pprint
import logging

BACKUP_CLIENT_ID = None
try:
    import youtube_dl
    BACKUP_CLIENT_ID = youtube_dl.extractor.soundcloud.SoundcloudIE._CLIENT_ID
except ImportError:
    log.exception('Failed to load backup client ID; install youtube-dl to fix this.')
except AttributeError:
    log.exception('Failed to fetch backup client ID from youtube-dl; your version is probably too old or too new.')

def sc_reverse(tid, apiid=None):
    apiid = apiid or BACKUP_CLIENT_ID
    assert apiid, "No Client ID available!"
    url = 'http://api.soundcloud.com/tracks/%s.json?client_id=%s' % (tid, apiid)

    logging.debug('Using URL %s', url)

    data = urllib.request.urlopen(url).read()
    jsondata = json.loads(data.decode('utf-8', 'replace'))

    logging.debug('Full JSON data: %s', pprint.pformat(jsondata))

    return jsondata['permalink_url']

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trackID', help='SoundCloud track ID')
    parser.add_argument('--client-id', '-i', nargs='?', help='sets client ID (defaults to the key provided by youtube-dl)')
    parser.add_argument('--verbose', '-v', action='store_true', help='enables verbose logging')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel('DEBUG')

    print(sc_reverse(args.trackID, args.client_id))