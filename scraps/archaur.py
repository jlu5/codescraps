try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen
    
import sys, json
from collections import defaultdict
    
baseurl = 'http://www.archlinux.org/packages/search/json/?'
fd = urlopen(baseurl + urlencode({'name':sys.argv[1]}))
data = json.load(fd)
print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
if data['valid'] and data['results']:
    f = set()
    archs = defaultdict(list)
    for x in data['results']:
        s = "{} - {} ({}".format(x['pkgname'],x['pkgdesc'],x['pkgver'])
        f.add(s)
        archs[s].append(x['arch'])
    for s in f:
        print "{} [{}])".format(s, ', '.join(archs[s]))