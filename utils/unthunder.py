#!/usr/bin/env python3
import sys
import base64
import binascii

def unthunder(link):
    """Decodes Base64-based thunder:// URI links.

    Example: unthunder("thunder://QUFodHRwOi8vaGkuYmFpZHUuY29tL3lqc3dvcmQvWlo=")
    """
    try:
        b64data = link.split("thunder://")[1]
    except IndexError:
        raise ValueError('Invalid link (must begin with "thunder://")')

    try:
        s = base64.b64decode(b64data)[2:-2]
    except binascii.Error:
        raise ValueError("Invalid link (bad base64 data)")

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