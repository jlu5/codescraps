#!/usr/bin/env python
import sys



def acba(a, b, c):
    i = sqrt((b**2) - (4*a*c))
    x = (-b + i) / 2*a
    y = (-b - i) / 2*a
    return (x, y)

if __name__ == '__main__':
    from math import sqrt
    from collections import OrderedDict
    
    if sys.version_info[0] >= 3:
        raw_input = input
    print("Calculator for 'ax^2 + bx + c = 0' equations:")
    var = OrderedDict()
    for x in ['a', 'b', 'c']:
        try:
            var[x] = float(raw_input('%s: ' % x))
        except ValueError:
            print("Invalid input.")
            sys.exit(0)
    try:
        print(acba(*var.values()))
    except ValueError:
        print("no real solution.")
