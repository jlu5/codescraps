#!/usr/bin/env python2
from random import shuffle

def scramble(word):
    word = list(word)
    shuffle(word)
    return ''.join(word)
    
if __name__ == "__main__":
    import sys
    try:
        while True:
            s = raw_input("Enter string to scramble: ")
            print scramble(s)
    except KeyboardInterrupt:
         print ""
         sys.exit()
