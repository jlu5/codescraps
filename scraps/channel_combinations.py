#!/usr/bin/env python2
import itertools
from sys import argv

try:
    items = range(int(argv[1]))
except:
    items = "#overdrive@athemenet ##GLolol@freenode #rand@randomnetwork #chat@overdrive-irc #dev@overdrive-irc".split()

def _pause(): raw_input("\nPress Enter to continue.")

# basic itertools, a test of permutations
n = 0
p = itertools.permutations(items, 2)
for c in p:
    if n >= 1000:
        print("Too many combinations to handle! Exiting!")
        break
    print c
    n += 1
print "Total of {} combinations processed.".format(n)
# _pause()
