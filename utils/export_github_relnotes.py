#!/usr/bin/env python3
"""
Converts GitHub Release Notes into Markdown text, printing the results to STDOUT.
"""

import argparse
import requests
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', help='the repository to access, in the form "author/repository"')
    # Verbose mode is not implemented yet
    #parser.add_argument("-v", "--verbose", help="verbose mode", action='store_true')
    parser.add_argument("-u", "--username", help="sets username to auth as", type=str)
    parser.add_argument("-k", "--oauth-key", help="sets OAuth key to use alongside the username", type=str)
    args = parser.parse_args()

    url = 'https://api.github.com/repos/%s/releases' % args.repo

    auth = None
    if args.username and args.oauth_key:
        auth = (args.username, args.oauth_key)
    elif args.oauth_key or args.username:
        # Only one of username / key was specified. Bail.
        parser.error("Only one of -u/--username and -k/--oauth_key was given.")

    data = requests.get(url, auth=auth)
    jsondata = data.json()

    for release in jsondata:
        is_draft = release['draft']

        # Use the tag name & link as the <h1> heading, if the release is not a draft
        if is_draft:
            print('# %s' % release['name'])
        else:
            print('# [%s](%s)' % (release['name'], release['html_url']))

        # On the next line, write the author and time of the release.
        print('Tagged as **%s** by [%s](%s)' % (release['tag_name'],
              release['author']['login'], release['author']['html_url']), end='')

        # Write the published date if one exists
        if not is_draft:
            print(' on %s' % release['published_at'])
        else:
            print()

        print()

        # Print the release notes body, with leading / trailing whitespace removed.
        for line in release['body'].strip().splitlines():
            print(line)
        print()  # Extra newline between releases