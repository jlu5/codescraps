#!/usr/bin/env python2
import time
s = time.strftime('Current time: %I:%M:%S %p, %B %d, %Y (%Z)', time.localtime())
#s = time.strftime('Time at UTC: %I:%M:%S %p, %B %d, %Y', time.gmtime())
print(s)
