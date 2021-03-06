#!/usr/bin/env python

from sys import version_info
from math import sqrt
def factors(n):
    """<number>
    
    Returns all factors of <number>."""
    if version_info[0] >= 3:
        xr = range
    else:
        xr = xrange
    n = int(n)
    if n <= 0:
        raise ValueError("cannot find factors of non-positive integers")
    if n > 1000000000000000:
        raise ValueError("number too big to calculate")
    _factors = []
    for i in xr(int(sqrt(n))):
        i += 1
        if n % i == 0:
            _factors.extend((i, int(n/i)))
    return sorted(set(_factors))
    
if __name__ == '__main__':
    from sys import argv, exit
    try:
        try:
            num = int(argv[1])
        except (IndexError, ValueError):
            if version_info[0] >= 3:
                raw_input = input
            num = raw_input("Enter a number to factor: ")
        try:
            res = factors(int(num))
        except ValueError as e:
            print("ValueError: %s" % e)
        else:
            print(res)
    except KeyboardInterrupt:
        print("\nExiting on Ctrl+C...")
