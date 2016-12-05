#!/usr/bin/env python3
"""Returns an IP address in hexadecimal format."""

import ipaddress
import sys

try:
	ip = sys.argv[1]
except IndexError:
	print("ERROR: missing command line argument (IP address).")
	sys.exit(1)

def hexip(ip):
	ipobj = ipaddress.ip_address(ip)
	ipbytes = ipobj.packed
	# Return the hex-formatted version of each byte, zfilled to 2 chars.
	return ''.join(format(b, 'x').zfill(2) for b in ipbytes)

print(hexip(ip))
