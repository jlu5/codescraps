#!/usr/bin/env python3
from __future__ import print_function, unicode_literals

import sys
import socket
from time import sleep
import logging
import http.client
from urllib.parse import urljoin, urlparse
from ssl import _create_unverified_context
import pprint

try:
    from bs4 import BeautifulSoup
except ImportError:
    logging.warning("bs4 is not installed. Meta refresh parsing will be disabled.")
    BeautifulSoup = None

class redirectParser():
    def __init__(self, enforce_ssl=False, disable_meta_refresh=False, max_redirs=10, no_check_certificates=False):
        self.nredirs = 0
        self.visited = []  # Store list of URLs passed through

        self.enforce_ssl = enforce_ssl
        self.disable_meta_refresh = disable_meta_refresh
        self.max_redirs = max_redirs
        self.no_check_certificates = no_check_certificates

    def parse(self, url, timeout=4.0):
        """Recursively looks up HTTP and meta refresh redirects."""

        if not url.lower().startswith(("http://", "https://")):
            url = "http://" + url

        addr = urlparse(url, allow_fragments=False)
        target = ''
        site = addr.netloc.encode('idna').decode()

        # Implicitly enable SSL on https:// links, if not already.
        ssl = self.enforce_ssl or addr.scheme == 'https'
        if ssl:
            context = None

            # If certificate checking is disabled, skip both the certificate verification and the hostname checks.
            if self.no_check_certificates:
                context = _create_unverified_context()
                context.check_hostname = False
            httpconn = http.client.HTTPSConnection(site, timeout=timeout, context=context)

        else:
            httpconn = http.client.HTTPConnection(site, timeout=timeout)

        # Preserve query section (e.g. "?abc=def" of //some.site/page.php?abc=def) if applicable.
        fullpath = addr.path
        if addr.query:
            fullpath += '?%s' % addr.query

        # Send a GET request to the desired address.
        httpconn.putrequest("GET", fullpath)

        # This header is needed for some reason; otherwise you get a HTTP 400 on some servers.
        httpconn.putheader("Accept", "*/*")
        httpconn.endheaders()

        # Fetch the response from the GET request.
        data = httpconn.getresponse()
        logging.debug('HTTP headers for %s: %s', url, pprint.pformat(data.getheaders()))

        if data.status == 200 and BeautifulSoup and not self.disable_meta_refresh:
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
            parsed_target = urlparse(target, allow_fragments=False)
            if not parsed_target.netloc:
                target = urljoin(url, target)

        logging.debug("%s %s %s: %s (SSL=%s)" % (url, data.status, data.reason, target, ssl))
        self.visited.append((data, url, target))

        if target:
            if self.nredirs < self.max_redirs:
                self.nredirs += 1
                # Sleep to avoid chewing all the CPU
                sleep(0.1)

                # Recursively lookup redirects for the target URL.
                return self.parse(target, timeout)
            else:
               raise OverflowError("Maximum amount of redirects (%s) reached." % self.max_redirs)

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

    parser = argparse.ArgumentParser(description='Recursively finds for HTTP and meta refresh redirects.')
    parser.add_argument('url', help='the address to access, in the form "web.host:port"')
    parser.add_argument("-v", "--verbose", help="verbose mode, shows the entire HTTP headers list", action='store_true')
    parser.add_argument("-R", "--disable-meta-refresh", help="disable checks for meta refresh tags", action='store_true')
    parser.add_argument("-S", "--ssl", help="use HTTPS to connect to the server", action='store_true')
    parser.add_argument("-m", "--max-redirects", metavar="max_redirs", help="defines the maximum amount of redirects this script will follow", type=int, default=10)
    parser.add_argument("-t", "--timeout", metavar="timeout", help="sets the timeout for accessing a site", type=_positivefloat, default=4.0)
    parser.add_argument("-nc", "--no-check-certificates", help="skips certificate checking for SSL links", action='store_true')
    args = parser.parse_args()

    parser = redirectParser(args.ssl, args.disable_meta_refresh, args.max_redirects, args.no_check_certificates)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        links = parser.parse(args.url, args.timeout)
        parser.print_results(links)
    except KeyboardInterrupt:
        print('Exiting on Ctrl-C.')
