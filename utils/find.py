#!/usr/bin/env python
import time, glob, argparse
parser = argparse.ArgumentParser()
parser.add_argument("globname", help="a filename glob to search for")
parser.add_argument("--limit", "-l", default=50, type=int, 
    help="the max. number of results to output (defaults to 50)")
args = parser.parse_args()

globname = args.globname
n = 0
limit = args.limit

print('Looking for glob: %s' % globname)
for item in glob.glob(globname):
    if n >= limit:
        print('\nMaximum result output (%s) exceeded, stopping...' % n)
        break
    print('Found matching item: %s' % item)
    n = n + 1
else:
    if n == 0:
        print('\nNo matching items found!')
    else:
        print('\nFinished, a total of %s items found!' % n)
