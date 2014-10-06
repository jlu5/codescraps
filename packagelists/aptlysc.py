#!/usr/bin/env python2
import sys
import subprocess
import pipes
from collections import defaultdict
import re
import time

command = sys.argv[1].lower()
params = sys.argv[2:]
repos = subprocess.check_output('aptly repo list -raw',shell=True)

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

if command == 'getdup':
    if len(sys.argv) < 3:
        print 'error: needs repo name!'
        sys.exit(2)
    getdups(params[0])
elif command == 'snapshot':
    for repo in repos.split('\n')[:-1]:
        if (params and re.search(params[0], repo)) or not params:
            sys.stdout.write(subprocess.check_output('aptly snapshot create {r}-{d} from repo {r}'.format(
                r=repo,d=time.strftime('%Y-%m-%d')), shell=True))
elif command == 'refreshmirrors':
    mirrors = subprocess.check_output('aptly mirror list -raw',shell=True)
    for m in mirrors.split('\n')[:-1]:
        sys.stdout.write(subprocess.check_output('aptly mirror update %s' % m, shell=True))
else:
    print("error: unknown command '%s', valid commands are 'getdup', 'snapshot',"
          " 'refreshmirrors'")
    sys.exit(1)
