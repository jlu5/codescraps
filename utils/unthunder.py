#!/usr/bin/env python3
import sys
import base64
import binascii
from urllib.parse import urlparse

SUPPORTED_URIS = ['thunder', 'flashget', 'qqdl', 'fs2you']

def unthunder(link):
    """Decodes Base64-based thunder://, flashget://, qqdl://, and fs2you:// URI links.

    Examples:
    unthunder("thunder://QUFodHRwOi8vaGkuYmFpZHUuY29tL3lqc3dvcmQvWlo=")
    unthunder("flashget://W0ZMQVNIR0VUXWh0dHA6Ly9iMS5ncHh6Lm5ldC8yMDE1MDYvemlwMldpblJBUl9ncHh6LnJhcltGTEFTSEdFVF0=")
    unthunder("qqdl://aHR0cDovL2IxLmdweHoubmV0LzIwMTUwNi96aXAyV2luUkFSX2dweHoucmFy")
    """
    parse_object = urlparse(link)
    scheme = parse_object.scheme.lower()
    b64data = parse_object.netloc

    if scheme not in SUPPORTED_URIS:
        raise ValueError("Unsupported link type (must be one of %s)" % ', '.join(SUPPORTED_URIS))

    try:
        s = base64.b64decode(b64data)
    except binascii.Error:
        raise ValueError("Invalid link (bad base64 data)")

    if scheme == 'thunder':
        # Cut first 2 and last 2 characters: thunder:// links are padded with "AA" at the left and "ZZ" at the right
        s = s[2:-2]
    elif scheme == 'flashget':
        # flashget:// links are prefixed and suffixed with "[FLASHGET]"
        s = s[10:-10]

    # Other links (qqdl://, fs2you://) have no padding.

    # Cycle through a few encodings
    try:
        return s.decode("gb2312")
    except ValueError:
        return s.decode("utf-8", "replace")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Decodes Base64-based thunder:// URI links.')
    parser.add_argument('url', help='the address to decode')
    args = parser.parse_args()

    print(unthunder(args.url))