#!/usr/bin/env python2
import random, string, sys
from os.path import basename

def gen(length=10, amount=5, type="all"):
    """Generates a list of random (IRC-style) channels."""
    type = string.ascii_letters + string.digits
    if length < 1 or amount < 1:
        if __name__ == "__main__":
            _usage()
        else:
            raise ValueError("Value for length or amount too not in range (1-100)")
    L = ",".join("#"+("".join((random.choice(type)) for _ in xrange(length))) for _ in xrange(amount))
    return L

def _usage():
    print("Usage: {} <length> <amount>\n\narguments: \n  length        The length of each channel name to be generated. \n  amount        The amount of names to generate.".format(basename(__file__)))
    sys.exit()

def _main():
    if len(sys.argv) > 3:
        _usage()
    try:
        length, amount = int(sys.argv[1]), int(sys.argv[2])
    except IndexError:
        print(gen())
    except ValueError:
        _usage()
    else:
        print(gen(length, amount))

if __name__ == "__main__":
    _main()
