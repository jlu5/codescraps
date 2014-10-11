#!/usr/bin/env python
### BEGIN CONFIGURATION ###
arch = "i386,amd64,source,all"
baseurl = "http://qa.debian.org/madison.php?text=on&"
### END CONFIGURATION ###

from collections import OrderedDict
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen

# A reimplementation of the 'rmadison' utility from Debian's devscripts,
# this fetches package information from Debian and Ubuntu's repositories
# using the publicly accessible API @ http://qa.debian.org/madison.php
def madison(pkg, dist, codenames='', suite=''):
    """Fetches package versions from Debian and Ubuntu's repositories,
    using the publicly accessible API at http://qa.debian.org/madison.php'"""
    arg = urlencode({'package':pkg,'table':dist,'a':arch,
                     'c':codenames,'s':suite})
    d = OrderedDict()
    fd = urlopen(baseurl+arg)
    for line in fd.readlines():
        L = line.decode().split("|")
        d[L[2].strip()] = (L[1].strip(),L[3].strip())
    return d

if __name__ == "__main__":
    import sys
    try:
        d = madison(sys.argv[1], 'all')
    except IndexError:
        print("Need package name as argument! Usage: rmadison.py <packagename>")
    else:
        print("Found {} results:".format(len(d)))
        for (k, v) in d.items():
            print("{} ({} [{}])".format(k,v[0],v[1]))