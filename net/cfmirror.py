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

args = parser.parse_args()

scraper = cfscrape.create_scraper(delay=args.delay)
site = scraper.get(args.source)
print('Got Cloudflare cookies: %s' % cfscrape.get_tokens())

with open(args.target, 'wb') as outf:
    count = outf.write(site.content)
    print('Wrote %d bytes to %s' % (count, args.target))
