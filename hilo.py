#!/usr/bin/env python2
import random
import argparse
import sys
# Silly HiLo v2, now with Argument parsing (so you can set ranges and stuff)! \o/
parser = argparse.ArgumentParser()
parser.add_argument("--min", type=int, default=1, help="minimum number for hilo (default=1)")
parser.add_argument("--max", type=int, default=100, help="maximum number for hilo (default=100)")
args = parser.parse_args()
min, max = args.min, args.max

# Always remember to check if your numbers are sane.
if min >= max:
    sys.stderr.write('\nERROR: Minimum value supplied is larger than or equal to maximum value!\n')
    sys.exit()
elif max - min < 10:
    sys.stderr.write('\nERROR: Range too small, numbers must be at least 10 apart.\n')
    sys.exit()

t, n = 1, random.randint(min, max)
print("Let's play HiLo!\n")

while True:
    try:
        try:
            g = int(raw_input("Pick an integer between %s and %s: "% (min, max)))
        except ValueError:
            print("That's not even an integer!\n")
            t = t + 1
            continue
        if g > max or g < min:
            print("Value not in range!")
            t = t + 1
        elif g > n:
            print "Lower!"
            t = t + 1
        elif g < n:
            print "Higher!"
            t = t + 1
        else:
            print('\nYou win! The correct number was {}, and it took you {} tries to'
                 ' find it!'.format(n, t))
            raw_input()
            break
    except KeyboardInterrupt:
        print('\nExiting...')
        break
