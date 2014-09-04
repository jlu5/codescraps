import urllib2
import collections
d = collections.OrderedDict()
fd = urllib2.urlopen('http://qa.debian.org/madison.php?package=fonts-liberation&table=debian&a=i386%2Camd64%2Csource%2Call&c=&s=&text=on')
for line in fd.readlines():
    line = line.split("|")
    d[line[2].strip()] = line[1].strip()
s = 'Found %s results: ' % len(d) + ', '.join("{!s} ({!s})".format(k,v) for (k,v) in d.items())
print s