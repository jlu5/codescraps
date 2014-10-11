#!/usr/bin/env python2
from distutils.version import LooseVersion as lv

def compare(ver1, ver2):
    if ":" in ver1 and ":" in ver2:
        res = lv(ver1.split(":")[0]) > lv(ver2.split(":")[0])
        if not res:
            return lv(ver1.split(":")[1]) > lv(ver2.split(":")[1])
        else: return res
    if ":" in ver1: return 1
    if ":" in ver2: return -1

def _main():
    try:
        ver1, ver2 = raw_input("Input version 1: "), raw_input("Input version 2: ")
    except IndexError:
        print("Error: need at least two values to compare!")
        sys.exit(1)
    else: 
        c = compare(ver1, ver2)
        r = {0:"Versions are the same.",1:ver1,-1:ver2}
        print r[c]

if __name__ == "__main__":
    _main()
