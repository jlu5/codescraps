#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import sys
import argparse
import socket
from time import sleep
try:
    import httplib
    from HTMLParser import HTMLParser
    from urlparse import urljoin
except ImportError:
    import http.client as httplib
    from urllib.parse import urljoin
    from html.parser import HTMLParser as HTMLParser

def _format_seconds(n):
    if n < 0: print("Warning, negative integer for meta-refresh delay value!")
    if n == 0: return "instant"
    if n == 1: return "after 1 second"
    return "after {} seconds".format(n)
class metarefreshParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            attrs = dict(attrs)
            try:
                if attrs['http-equiv'].lower() == "refresh":
                    ct = attrs['content'].lower().split("url=", 1)
                    delay = int(ct[0].split(";")[0])
                    print("Meta refresh target: {} ({})".format(ct[1], _format_seconds(delay)))
                    global L, metatarget
                    L = ct[1]
                    metatarget = True
            except KeyError: pass
            except ValueError: 
                print("Meta-refresh detected, but there was an error parsing it (non-standard HTML?)")
            except IndexError:
                print("Meta-refresh detected: current page ({})".format(_format_seconds(attrs['content'])))
metaparse = metarefreshParser()

nredirs, metatarget, locations = 1, False, []
def redirectParse(url):
    """Recursively looks up HTTP/meta refresh redirects."""
    addr = url.lower()
    global L, nredirs, locations, maxredirs, metatarget, ignoreloops
    L = metatarget = 0
    try:
        addr = addr.split("://", 1)[1] # Remove any http(s):// elements
    except IndexError: pass
    try:
        addr = addr.split("/", 1) # Split links in half (as in "site.web/index.htm")
    except IndexError: pass
    if args.ssl or url.lower().startswith("https"):
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
    print(r1.status, r1.reason+":", url)
    if r1.status == 200 and not args.disable_meta_refresh:
        metaparse.feed(r1.read().decode("utf-8", "replace"))
    else: L = r1.getheader('location') 
    if args.verbose:
        headers = r1.getheaders()
        for n in headers:
            print("{}: {} / Target: {}".format(n[0], n[1], metatarget or L))
    if L:
        if L in locations and not ignoreloops:
            print("Redirect loop detected, aborting! (run with -n argument to ignore this)")
            sys.exit(2)
        sleep(0.1)
        if nredirs < maxredirs:
            nredirs += 1
            locations.append(L)
            return redirectParse(urljoin(url, L))
        else: print("Maximum amount of redirects ({}) reached. Try running the script with a higher -m limit!".format(maxredirs))

if __name__ == "__main__": 
    ### Handle arguments nicely using argparse
    def _positivefloat(value):
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
    parser.add_argument("-m", "--max-redirects", metavar="maxredirs", help="defines the maximum amount of redirects this script will follow", type=int, default=10)
    parser.add_argument("-t", "--timeout", metavar="timeout", help="sets the timeout for accessing a site", type=_positivefloat, default=4.0)
    args = parser.parse_args()

    t = args.timeout
    maxredirs = args.max_redirects
    ignoreloops = args.ignore_loops
    redirectParse(args.url)
