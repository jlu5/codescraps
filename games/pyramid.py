#!/usr/bin/env python
def pyramid(s):
    """Creates pyramid text from input."""
    n, l = 1, 0
    while n < len(s) and l < 5000:
        print(s[:n])
        n += 1
        l += 1
    else:
        while n > 0 and l < 5000:
            print(s[:n])
            n -= 1
            l += 1
        
if __name__ == "__main__":
    from sys import argv
    s = ' '.join(argv[1:])
    if s: 
        pyramid(s)
    else:
        print("usage: %s <text>" % __file__)
