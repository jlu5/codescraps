#!/usr/bin/env python2
import sys
import subprocess
import pipes
from collections import defaultdict
import re
import time

def _error():
    print("error: unknown command, valid commands are 'getdup', 'snapshot',"
          " 'refreshmirrors'")
    sys.exit(1)    

def getdups(reponame):
    if reponame not in repos:
        print "error: repo '%s' does not exist!"%reponame
        sys.exit(2)
    else:
        print 'checking duplicates for repo %s...'%reponame
        showpackages = subprocess.check_output('aptly repo show -with-packages '+pipes.quote(reponame),shell=True).split("\n")
        uniqPackages = defaultdict(set)
        for p in showpackages:
            p = p.split("_")
            if len(p) == 3: 
                packageName, version = p[0].strip(), p[1]
                uniqPackages[packageName].add(version)
        for p, v in uniqPackages.iteritems():
            if len(v) > 1: 
                print 'Duplicate package: %s (%s)' % (p, ', '.join(v))

try:
    command = sys.argv[1].lower()
except IndexError:
    _error()
params = sys.argv[2:]
repos = subprocess.check_output('aptly repo list -raw',shell=True).split('\n')[:-1]
mirrors = subprocess.check_output('aptly mirror list -raw',shell=True).split('\n')[:-1]

if command == 'getdup':
    if len(sys.argv) < 3:
        print 'error: needs repo name!'
        sys.exit(2)
    getdups(params[0])
elif command == 'snapshot':
    for mir in mirrors:
        if (params and re.search(params[0], repo)) or not params:
            sys.stdout.write(subprocess.check_output('aptly snapshot create {r}-{d} from mirror {r}'.format(
                r=mir,d=time.strftime('%Y-%m-%d')), shell=True))
elif command == 'refreshmirrors':
    for m in mirrors:
        sys.stdout.write(subprocess.check_output('aptly mirror update %s' % m, shell=True))
else:
    _error()
