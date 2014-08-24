#!/usr/bin/env python2
import random, string, sys
from os.path import basename

def _gettype(input):
    if input == "all": return string.ascii_letters + string.digits
    elif input == "letters": return string.ascii_letters
    elif input == "numbers": return string.digits
    elif input == "upper": return string.ascii_uppercase
    elif input == "lower": return string.ascii_lowercase
    else: 
        if __name__ == "__main__":
            _usage()
        else:
            raise ValueError("Unknown string type: " + input)

def gen(length=10, amount=5, type="all", chanify=False):
    type = _gettype(type)
    if length not in range(1, 101) or amount not in range(1, 101):
        if __name__ == "__main__":
            _usage()
        else:
            raise ValueError("Value for length or amount too not in range (1-100)")
    L = []
    for n in range(amount):
        L.append("".join(random.choice(type) for blah in range(length)))
    if chanify:
        return ",".join(["#" + item for item in L])
    return L
    
def _usage():
    print "Usage: {} <length> <amount>\n\narguments: \n  length        The length of each channel name to be generated. \n  amount        The amount of names to generate.".format(basename(__file__))
    sys.exit()
    
def _main():
    if len(sys.argv) > 3:
        _usage()
    try:
        length, amount = int(sys.argv[1]), int(sys.argv[2])
    except IndexError:
        print gen(chanify=True)
    except ValueError:
        _usage()
    else:
        print gen(length, amount, chanify=True)
    
if __name__ == "__main__":
    _main()
