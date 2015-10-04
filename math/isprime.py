#!/usr/bin/env python

from factors import factors

def isPrime(n):
    """Returns whether the given number is prime."""
    return n > 1 and len(factors(n)) == 2

if __name__ == '__main__':
    from sys import argv, exit, version_info
    try:
        try:
            num = int(argv[1])
        except (IndexError, ValueError):
            if version_info[0] >= 3:
                raw_input = input
            num = raw_input("Check if a number is prime: ")
        try:
            res = isPrime(int(num))
        except ValueError as e:
            print("ValueError: %s" % e)
        else:
            print(res)
    except KeyboardInterrupt:
        print("\nExiting on Ctrl+C...")