#!/usr/bin/env python

from __future__ import print_function
import sys, argparse, socket
from os.path import basename
from time import sleep
try:
    import httplib
    from HTMLParser import HTMLParser
except ImportError:
    import http.client as httplib
    from html.parser import HTMLParser as HTMLParser
### Look for meta refresh tags
def _format_seconds(n):
    if n < 0: print("Warning, negative integer for meta-refresh delay value!")
    if n == 0: return "instant"
    if n == 1: return "after 1 second"
    return "after {} seconds".format(n)
class metarefreshParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            L = dict(attrs)
            try:
                if L['http-equiv'].lower() == "refresh":
                    ct = L['content'].lower().split("url=", 1)
                    delay = int(ct[0].split(";")[0])
                    print("Meta refresh target: {} ({})".format(ct[1], delay, _format_seconds(delay)))
                    return ct[1]
            except KeyError: pass
            except ValueError: 
                print("Meta-refresh detected, but there was an error parsing it (non-standard HTML?)")
            except IndexError:
                print("Meta-refresh detected: current page ({})".format(_format_seconds(L['content'])))
metaparse = metarefreshParser()
### Handle arguments nicely using argparse
def positivefloat(value):
    ivalue = float(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError("%s is an invalid positive float value." % value)
    return ivalue
parser = argparse.ArgumentParser(description='Shows HTTP Status codes and HTTP redirect paths..')
parser.add_argument('url', help='the address to attempt to access, in the form "web.host:port"')
parser.add_argument("-v", "--verbose", help="show the entire HTTP headers list", action='store_true')
parser.add_argument("-R", "--disable-meta-refresh", help="disable experimental checking for meta refresh tags", action='store_true')
parser.add_argument("-S", "--ssl", help="use HTTPS to connect to the server", action='store_true')
parser.add_argument("-n", "--ignore-loops", help="don't detect redirect loops", action='store_true')
parser.add_argument("-m", "--max-redirects", metavar="max", help="defines the maximum amount of redirects this script will follow", type=int, default=15)
parser.add_argument("-t", "--timeout", metavar="timeout", help="sets the timeout for accessing a site", type=positivefloat, default=5.0)
args = parser.parse_args()

nredirs, metatarget, locations = 0, '', []
t = args.timeout
def _connect(url=args.url):
    addr = url
    try:
        addr = addr.split("://", 1)[1] # Remove any http(s):// elements
    except IndexError: pass
    try:
        addr = addr.split("/", 1) # Split links in half (as in "site.web/index.htm")
    except IndexError: pass
    if args.ssl:
        h1 = httplib.HTTPSConnection(addr[0], timeout=t)
    else:
        h1 = httplib.HTTPConnection(addr[0], timeout=t)
    try:
        h1.putrequest("GET","/"+addr[1])
    except IndexError: h1.putrequest("GET","/")
    # This is needed for some strange reason; otherwise you get a HTTP 400 on some servers.
    h1.putheader("Accept","*/*") 
    try:
       h1.endheaders()
       r1 = h1.getresponse()
    except socket.timeout as e:
       print("Connection timed out.")
       sys.exit(1)
    except socket.error as e:
       if e.errno == -2:
           print("Unresolved host or invalid hostname.")
       else:
           print("Caught unhandled socket.error, aborting: " + str(e))
       sys.exit(1)
    # if r1.status == 200 and args.check_meta_refresh:
        # L = metaparse.feed(r1.read())
    L = metaparse.feed(r1.read()) if r1.status == 200 and not args.disable_meta_refresh else r1.getheader('location') 
    print(r1.status, r1.reason+":", url)
    if args.verbose:
        headers = r1.getheaders()
        for n in headers:
            print("{}: {}".format(n[0], n[1]))
    global nredirs, locations, max, metatarget
    if r1.status in [301, 302] or metatarget:
        print("Target:", L)
        sleep(0.8) # Don't flood the target server!
        if (L not in locations or args.ignoreloops) and nredirs <= max:
            nredirs += 1
            locations += L
            return _connect(L)
        else: print("Maximum amount of redirects ({}) reached. Try running the script with a higher -m limit!".format(max))
_connect()
