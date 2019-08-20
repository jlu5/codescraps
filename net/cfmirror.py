#!/usr/bin/env python3
"""
Downloads a static web page protected by Cloudflare.
This can be used to unblock, for example, RSS feeds behind its anti-bot page.
"""

import argparse
import cfscrape

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('source', help='source URL')
parser.add_argument('target', help='target file')
parser.add_argument('--delay', type=int, help="time to wait during Cloudflare's challenge page", default=5)
parser.add_argument('--cookie-file', type=str, help="location (relative to cwd) to save Cloudflare cookie", default='cloudflare-cookie')

args = parser.parse_args()

sess = cfscrape.create_scraper(delay=args.delay)

print('Waiting for %s ...' % args.source)

site = sess.get(args.source)
with open(args.target, 'wb') as outf:
    count = outf.write(site.content)
    print('Wrote %d bytes to %s' % (count, args.target))
