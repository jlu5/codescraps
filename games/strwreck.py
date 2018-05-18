#!/usr/bin/env python3
"""
Reads a file or text from the command line, displaying a scrambled version to the screen.
"""

ITERMIN = 10
ITERMAX = 50

import fileinput
import random
import string

def _shiftchar(s):
    try:
        value = ord(str(s)[0])
    except IndexError:  # String was already emptied out!
        value = random.randint(1, 255)
    return chr(value)

funcs = [lambda s: s.swapcase(),
         lambda s: ' '*random.randint(1,4),
         lambda s: '',
         lambda s: s * 2,
         _shiftchar,
         lambda s: random.choice(string.printable)
        ]

def strwreck(s, times=0):
    s = list(map(str, s))
    for iterations in range(times or random.randint(ITERMIN, ITERMAX)):
        char = random.randint(0, len(s)-1)
        s[char] = random.choice(funcs)(s[char])
    return ''.join(s)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Scrambles a file and displays it to the screen')
    parser.add_argument("-t", "--times", help="Specifies amount of iterations", type=int, default=0)
    parser.add_argument("-i", "--interactive", help="Interactive mode (text is specified directly on command line)", action='store_true')
    parser.add_argument("source", help="If in interactive mode, specifies the text to corrupt. Otherwise, specifies a filename to read from text from", type=str, nargs='+')
    args = parser.parse_args()

    if args.interactive:
        print(strwreck(' '.join(args.source), times=args.times), end='')
    else:
        with open(args.source[0], encoding='utf-8', errors='replace') as f:
            for line in f.readlines():
                print(strwreck(line, times=args.times), end='')
