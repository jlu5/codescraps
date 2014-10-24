#!/usr/bin/env python

from sys import version_info
from math import sqrt
def factors(n):
    """<number>
    
    Returns all factors of <number>."""
    if version_info >= 3:
        xrange = range
    n = int(n)
    if n <= 0:
        raise ValueError("cannot find factors of neon-positive integers")
    if n >= 1000000000:
        raise ValueError("number too big to calculate")
    _factors = set()
    for i in xrange(int(sqrt(n))):
        i += 1
        if n % i == 0:
            _factors.add(i)
            _factors.add(n/i)
    return sorted(_factors)
    
if __name__ == '__main__':
    from sys import argv
    try:
        num = int(argv[1])
    except (IndexError, ValueError):
        if version_info >= 3:
            raw_input = input
        num = raw_input("Enter a number to factor: ")
    try:
        res = factors(int(num))
    except ValueError as e:
        print("ValueError: %s" % e)
    else:
        print(res)
