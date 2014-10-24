#!/usr/bin/env python2
import ConfigParser
import json
try:
    from colorama import init, Style
except ImportError:
    def _bold(s): return s
else: 
    def _bold(s): return '{}{}{}'.format(Style.BRIGHT,s,Style.RESET_ALL)
    init()

Config = ConfigParser.ConfigParser()
Config.read("aconfigtest.conf")
print "Archs: %s" % ' '.join(json.loads(Config.get('Config', "archs")))
print "Package lists output directory: %s" % Config.get('Config', "pparse-outdir")
repos = json.loads(Config.get('Config', "mirror-imports"))
for repo in repos:
    print
    m = sorted(repos[repo])
    print "Mirrors for repository %s: %s (total %s)" % (_bold(repo), ' '.join(m), _bold(len(m)))
