#!/usr/bin/env python3
import sys, random, string
from time import sleep

irccolors = ['\x03'+str(x).zfill(2) for x in range(16)]
_UNICODE_PRINTABLE = []

def _setup_unicode():
    global _UNICODE_PRINTABLE
    _UNICODE_PRINTABLE = [chr(char) for char in range(1, 0x2FA1F)]

def randomjunk(nbytes, colored=False, no_delay=True, no_whitespace=False,
    no_digits=False, no_symbols=False, irccolor=False, use_unicode=False):
    """Generates random junk."""
    amount_of_bytes = 0

    chars = string.ascii_letters + (" \n" if not no_whitespace else '')

    if not no_symbols:
        chars += string.punctuation
    if not no_digits:
        chars += string.digits

    if colored:
        try:
            from colorama import init, Fore
        except ImportError:
            raise ImportError("Error: The color option requires the colorama"
            " module to be installed, get it from "
            "http://pypi.python.org/pypi/colorama\n")
        else:
            init()

    if irccolor:  # If in IRC mode, print a colour to start
        print(random.choice(irccolors), end='')

    while amount_of_bytes < nbytes:

        # print the random bytes, without a trailing newline
        if random.random() > 0.8 and use_unicode:
            try:
                print(random.choice(_UNICODE_PRINTABLE), end='')
            except UnicodeError:
                continue
        else:
            print(random.choice(chars), end='')

        if not no_delay:
            # Delay text output to make it seem like a flowing wall of gibberish
            sleep(random.uniform(0.0005, 0.01))

        amount_of_bytes += 1
        if irccolor and random.random() >= 0.75:
            print(random.choice(irccolors), end='')
        elif colored and random.random() >= 0.8:
            print(random.choice(([getattr(Fore, x) for x in
                  ('BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN',
                   'WHITE', 'RESET')])), end='')

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
    parser.add_argument("-i", "--irc", help="Use IRC color codes in output"
        " (this overrides the --color option", action='store_true')
    parser.add_argument("-u", "--unicode", help="Enable generating UTF-8 garbage", action='store_true')
    args = parser.parse_args()

    if args.unicode:
        _setup_unicode()

    try:
        randomjunk(args.bytes, args.color, args.no_delay,
                   args.no_whitespace, args.no_digits, args.no_symbols, args.irc,
                   args.unicode)
    except KeyboardInterrupt:
        sys.exit()
