#!/usr/bin/env python2
import re

# This fake IP is actually a reserved test range (http://en.wikipedia.org/wiki/Reserved_IP_addresses)
# OurString = 'TestNick!~Derp@ip192-0-2-42.dsl.myisp.net'
print 'Type an IRC hostname in the form of n!u@h:'
OurString = raw_input()

derp = re.split('[!@]', OurString)

print 'Original string: '
print OurString
print ''

print 'List after: '
print derp
print ''

if len(derp) != 3:
    print 'Ruh oh, invalid hostmask length! (length of list != 3)'
else:
    print 'Length of list correct, banmask = *!*@' + derp[2]
    
print ''
raw_input("Press Enter to continue...")
