#!/usr/bin/env python
### BEGIN CONFIGURATION ###
arch = "i386,amd64,source,all"
### END CONFIGURATION ###

import json
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
    pkg, dist = map(str.lower, (pkg, dist))
    arg = urlencode({'package':pkg,'table':dist,'a':arch,
                     'c':codenames,'s':suite})
    d = OrderedDict()
    fd = urlopen("https://qa.debian.org/madison.php?text=on&"+arg)
    for line in fd.readlines():
        L = line.decode().split("|")
        d[L[2].strip()] = (L[1].strip(),L[3].strip())
    return d

def archaur(pkg):
    pkg = pkg.lower()
    baseurl = 'https://aur.archlinux.org/rpc.php?type=info&'
    fd = urlopen(baseurl + urlencode({'arg':sys.argv[1]}))
    data = json.load(fd)
    try:
        return data['results'][0]
    except IndexError:
        return

if __name__ == "__main__":
    import sys
    from os.path import basename
    try:
        d = madison(sys.argv[1], 'all')
    except IndexError:
        print("Need package name as argument! Usage: %s <packagename>" % 
            basename(__file__))
        sys.exit(1)
    else:
        for (k, v) in d.items():
            print("{} ({} [{}])".format(k,v[0],v[1]))
    aurs = archaur(sys.argv[1])
    if aurs:
        print("Arch Linux AUR ({}): [ID:{} Votes:{}]".format(aurs["Version"], 
            aurs['ID'], aurs['NumVotes']))
