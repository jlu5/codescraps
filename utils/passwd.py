#!/usr/bin/env python
import random
import string
import sys

if sys.version_info[0] >= 3:
    raw_input = input

def passwd(plen=16):
    rg = random.SystemRandom()
    letters = string.ascii_letters + string.digits
    pw = ''.join(rg.choice(letters) for n in range(plen))
    return pw
   
def _fail():
    print("are you kidding me")
    sys.exit(1)
   
if __name__ == "__main__":
    import sys
    try:
        plen = int(sys.argv[1])
    except IndexError:
        plen = 16
    except ValueError:
        _fail()
    if plen <= 0:
        _fail()
    print(passwd(plen))
    try:
        # make it so it doesn't close automatically
        if sys.argv[2] == "--hover":
            raw_input()
    except:
        pass
