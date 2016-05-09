#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import sys
import socket
from time import sleep
import logging
try:
    import httplib
    from HTMLParser import HTMLParser
    from urlparse import urljoin, urlparse
except ImportError:
    import http.client as httplib
    from urllib.parse import urljoin, urlparse
    from html.parser import HTMLParser as HTMLParser

try:
    from bs4 import BeautifulSoup
except ImportError:
    logging.warning("bs4 is not installed. Meta refresh parsing will be disabled.")
    BeautifulSoup = None

class redirectParser():
    def __init__(self):
        self.nredirs = 0
        self.visited = []  # Store list of URLs passed through

    def parse(self, url, timeout, ssl=False, disable_meta_refresh=False, verbose=False, maxredirs=10):
        """Recursively looks up HTTP and meta refresh redirects."""
        assert not url.startswith(('/', '\\')) # Trying to lookup "/" will freeze the app?!

        addr = urlparse(url)
        target = ''
        site = addr.netloc.encode('idna').decode()
        assert site, "Invalid URL %s" % url

        # Implicitly enable SSL on https:// links, if not already.
        if ssl or addr.scheme == 'https':
            http = httplib.HTTPSConnection(site, timeout=timeout)
        else:
            http = httplib.HTTPConnection(site, timeout=timeout)

        # Send a GET request to the desired address.
        try:
            http.putrequest("GET", "/"+addr.path)
        except IndexError:
            # addr[1] may be empty if we're requesting a root domain (e.g. "github.com").
            http.putrequest("GET", "/")

        # This header is needed for some reason; otherwise you get a HTTP 400 on some servers.
        http.putheader("Accept", "*/*")
        http.endheaders()

        # Fetch the response from the GET request.
        data = http.getresponse()

        if data.status == 200 and BeautifulSoup and not disable_meta_refresh:
            # If the code was a 200 OK, parse meta refresh links if enabled.
            html = BeautifulSoup(data.read(), "html.parser")
            for tag in html.find_all('meta'):
                # A meta refresh tag looks something like this:
                #     <meta http-equiv="refresh" content="5; url=http://example.com/">
                # or without a redirect:
                #     <meta http-equiv="refresh" content="5">
                if tag.get("http-equiv"):
                    content = tag.get("content", '')
                    content = content.lower()
                    try:
                        target = content.split("url=", 1)[1]
                        break
                    except IndexError:
                        # Not a valid redirect, ignore this.
                        continue

        else:  # Get the target location for 30x redirects
            target = data.getheader('location')

        # The resulting target was a relative link. Format this appropriately by joining the target
        # with the requested URL.
        if target:
            parsed_target = urlparse(target)
            if not parsed_target.netloc:
                target = urljoin(url, target)

        self.visited.append((data, url, target))

        if target:
            if self.nredirs < maxredirs:
                self.nredirs += 1
                # Sleep to avoid chewing all the CPU
                sleep(0.1)

                # Recursively lookup redirects for the target URL.
                return self.parse(target, timeout, ssl, disable_meta_refresh, verbose, maxredirs)
            else:
               raise OverflowError("Maximum amount of redirects (%s) reached." % maxredirs)

        return self.visited

    def print_results(self, visited):
        for datapair in visited:
            data, url, target = datapair
            reason = data.reason or "Unknown Status Code"
            if target:
                print("%s %s: %s => %s" % (data.status, reason, url, target))
            else:
                print("%s %s: %s" % (data.status, reason, url))

if __name__ == "__main__":
    ### Handle arguments nicely using argparse
    import argparse

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
    parser.add_argument("-m", "--max-redirects", metavar="maxredirs", help="defines the maximum amount of redirects this script will follow", type=int, default=10)
    parser.add_argument("-t", "--timeout", metavar="timeout", help="sets the timeout for accessing a site", type=_positivefloat, default=4.0)
    args = parser.parse_args()

    parser = redirectParser()
    try:
        links = parser.parse(args.url, args.timeout, args.ssl, args.disable_meta_refresh, args.verbose, args.max_redirects)
        parser.print_results(links)
    except KeyboardInterrupt:
        print('Exiting on Ctrl-C.')
