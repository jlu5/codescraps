#!/usr/bin/env python3
"""
Generates a git-svn authors file using usernames from https://alioth.debian.org.
"""

import subprocess
import re
import bs4
import urllib.request
import sys

AUTHORS_LINE_RE = re.compile(r'r\d+ \| (.*?) \|')
def get_svn_authors(url):
    """
    Returns a list of committer usernames given a URL (for svn log).
    """
    authors = set()

    data = subprocess.check_output(['svn', 'log', url])
    for line in data.decode('utf-8').splitlines():
        match = AUTHORS_LINE_RE.search(line)
        if match:
            authors.add(match.group(1))

    return authors

def _fetch_userdata_page(username):
    data = urllib.request.urlopen('https://alioth.debian.org/users/%s' % username)
    soup = bs4.BeautifulSoup(data)

    return soup.find(id='user-profile-personal-info')

def fetch_name_email(username):
    """
    Returns the name and email of an https://alioth.debian.org SVN user.
    """
    userdata = _fetch_userdata_page(username)
    if (not userdata) and '-guest' in username:
        # Possibly missing user - it might be a guest account that got replaced by a regular one?
        new_username = username.replace('-guest', '')
        print('Note: trying %s instead of %s (username missing)' % (new_username, username), file=sys.stderr)
        userdata = _fetch_userdata_page(new_username)

    if userdata:
        trs = userdata.find_all('tr')
        name = trs[2].find_all('td')[1].text.strip()
        email = trs[3].find_all('td')[1].text.replace('@nospam', '').replace(' ', '').strip()
    else:
        return (username, "unknown-email@localhost")

    return (name, email)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url', nargs='?', help='Subversion repository to read')
    args = parser.parse_args()

    authors = get_svn_authors(args.url)
    print('svn authors:', authors, file=sys.stderr)

    for author in authors:
        name, email = fetch_name_email(author)
        print('%s = %s <%s>' % (author, name, email))
