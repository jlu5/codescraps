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

class metarefreshParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            attrs = dict(attrs)
            try:
                if attrs['http-equiv'].lower() == "refresh":
                    ct = attrs['content'].lower().split("url=", 1)
                    delay = int(ct[0].split(";")[0])
                    print("Meta refresh target: {} ({})".format(ct[1], self._format_seconds(delay)))
                    global L, metatarget
                    L = ct[1]
                    metatarget = True
            except KeyError:
                pass
            except ValueError: 
                print("Meta-refresh detected, but there was an error parsing it (non-standard HTML?)")
            except IndexError:
                print("Meta-refresh detected: current page ({})".format(self._format_seconds(attrs['content'])))

 
    def _format_seconds(self, n):
        if n < 0: print("Warning, negative integer for meta-refresh delay value!")
        if n == 0: return "instant"
        if n == 1: return "after 1 second"
        return "after {} seconds".format(n)
class redirectParser():
    def __init__(self):
        self.nredirs = 0
        self.metatarget = False
        self.locations = []

    def parse(self, url, timeout, ssl=False, disable_meta_refresh=False, verbose=False, maxredirs=10, ignoreloops=False):
        """Recursively looks up HTTP/meta refresh redirects."""
        addr = url
        L = []
        try:
            addr = addr.split("://", 1)[1] # Remove any http(s):// elements
        except IndexError:
            pass
        try:
            addr = addr.split("/", 1) # Split links in half (as in "site.web/index.htm")
        except IndexError: pass
        if ssl or url.lower().startswith("https"):
            h1 = httplib.HTTPSConnection(addr[0], timeout=t)
        else:
            h1 = httplib.HTTPConnection(addr[0], timeout=t)
        try:
            h1.putrequest("GET", "/"+addr[1])
        except IndexError:
            h1.putrequest("GET", "/")
        # This is needed for some strange reason; otherwise you get a HTTP 400 on some servers.
        h1.putheader("Accept","*/*") 
        h1.endheaders()
        r1 = h1.getresponse()
        reason = (r1.reason or "(Unknown)") + ":"
        print(r1.status, reason, url)
        if r1.status == 200 and not disable_meta_refresh:
            metaparse = metarefreshParser()
            metaparse.feed(r1.read().decode("utf-8", "replace"))
        else:
            L = r1.getheader('location') 
        if verbose:
            headers = r1.getheaders()
            for n in headers:
                print("{}: {} / Target: {}".format(n[0], n[1], metatarget or L))
        if L:
            if L in self.locations and not ignoreloops:
                raise ValueError("Redirect loop detected, aborting! (run with -n argument to ignore this)")
            sleep(0.1)
            if self.nredirs < maxredirs:
                self.nredirs += 1
                self.locations.append(L)
                return self.parse(urljoin(url, L), timeout, ssl, disable_meta_refresh, verbose, maxredirs, ignoreloops)
            else:
               raise OverflowError("Maximum amount of redirects ({}) reached. Try running the script with a higher -m limit!".format(maxredirs))

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
    
    parser = redirectParser()
    parser.parse(args.url, args.timeout, args.ssl, args.disable_meta_refresh, args.verbose, args.max_redirects, args.ignore_loops)
