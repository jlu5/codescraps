#!/usr/bin/env python2
import sys, random, string
from time import sleep

class RJError(Exception):
    pass
def randomjunk(bytes, colored=False, no_delay=True, no_whitespace=False,
    no_digits=False, no_symbols=False):
    """Generates random junk."""
    b = 0
    s = string.ascii_letters + (" \n" if not no_whitespace else '')
    if not no_symbols: s += string.punctuation
    if not no_digits: s += string.digits
    if colored:
        try: 
            from colorama import init, Fore
        except ImportError:
            raise RJError("Error: The color option requires the colorama"
            " module to be installed, get it from "
            "http://pypi.python.org/pypi/colorama\n")
        else:
            init()
            color = True
    while b < bytes:
        sys.stdout.write(random.choice(s))
        if not no_delay: sleep(random.uniform(0.0005, 0.01))
        b += 1
        if colored and random.random() >= 0.8:
            sys.stdout.write(random.choice(([getattr(Fore, x) for x in 
            ('BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN',
            'WHITE', 'RESET')])))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generates random junk, with'
        ' optional ANSI colors! (using the colorama module)')
    parser.add_argument("-c", "--color", help="Generate random colors, using"
        " the colorama module (if present)", action='store_true')
    parser.add_argument("-nd", "--no-delay", help="Turns off the delay used "
        "to prettify terminal output, useful if you want to generate "
        "random junk to files", action='store_true')
    parser.add_argument("-nw", "--no-whitespace", help="Disables generating "
        "whitespace", action='store_true')
    parser.add_argument("-ns", "--no-symbols", help="Disables generating "
        "random symbols", action='store_true')
    parser.add_argument("-nn", "--no-digits", help="Disables generating "
        "random digits", action='store_true')
    parser.add_argument("bytes", help="Sets the amount of random junk (in "
        "bytes) this script will dump, excluding newlines and colors",
        type=int)
    args = parser.parse_args()
    try: randomjunk(args.bytes, args.color, args.no_delay, 
        args.no_whitespace, args.no_digits, args.no_symbols)
    except KeyboardInterrupt: sys.exit()
    except RJError as e: sys.stderr.write(str(e))
    else: sys.stderr.write("\n\nDone!\n")