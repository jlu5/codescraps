#!/usr/bin/env python2
import sys
import subprocess
from collections import defaultdict

command = sys.argv[1].lower()
params = sys.argv[2:]

def getdups(reponame):
    if reponame not in subprocess.check_output('aptly repo list -raw', shell=True):
        print "error: repo '%s' does not exist!"%reponame
        sys.exit(2)
    else:
        print 'checking duplicates for repo %s...'%reponame
        showpackages = subprocess.check_output('aptly repo show -with-packages '+reponame, shell=True).split("\n")
        uniqPackages = defaultdict(set)
        for p in showpackages:
            p = p.split("_")
            if len(p) == 3:
                packageName, version = p[0].strip(), p[1]
                uniqPackages[packageName].add(version)
        for p, v in uniqPackages.iteritems():
            if len(v) > 1:
                print 'Duplicate package: %s (%s)' % (p, ', '.join(v))
        # print plist

if command == 'getdup':
    if len(sys.argv) < 3:
        print 'error: needs repo name!'
        sys.exit(2)
    getdups(params[0])
else:
    print "error: unknown command '%s', valid commands are"
    sys.exit(1)
