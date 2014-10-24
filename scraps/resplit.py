#!/usr/bin/env python2
import re
print 'Type an IRC hostname in the form of n!u@h:'
OurString = raw_input()
derp = re.split('[!@]', OurString)
print '\nSplit parts: '
print derp
print ''
if len(derp) != 3:
    print 'Ruh oh, invalid hostmask length! (length of list != 3)'
else:
    print 'Length of list correct, banmask = *!*@' + derp[2]
