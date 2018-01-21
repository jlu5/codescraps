#!/usr/bin/env python3
"""Expands and returns IP addresses encoded in hex."""

import sys
import ipaddress

def unhexip(hexstring):
    ipbytes = b''
    # Get bytes from the hex string 4 at a time for IPv6.
    while hexstring:
        ipbytes += bytearray.fromhex(hexstring[:4])
        hexstring = hexstring[4:]
    ipobj = ipaddress.ip_address(ipbytes)
    return ipobj.compressed

if __name__ == '__main__':
    try:
        hexstring = sys.argv[1]
    except IndexError:
        print("ERROR: missing command line argument (hexadecimal string).")
        sys.exit(1)

    print(unhexip(hexstring))
