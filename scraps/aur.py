#!/usr/bin/env python
try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen
    
import sys, json
from collections import defaultdict
    
baseurl = 'https://aur.archlinux.org/rpc.php?type=search&'
fd = urlopen(baseurl + urlencode({'arg':sys.argv[1]}))
data = json.load(fd)
print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
if data['results']:
    print "Found {} result{}: ".format(data["resultcount"], 
        's' if data["resultcount"] != 1 else '')
    for x in data['results']:
        verboseInfo = " [ID:{} Votes:{}]".format(x['ID'], x['NumVotes'])
        s = "{} - {} ({}{})".format(x['Name'],x['Description'],x['Version'], verboseInfo)
        print s
        
