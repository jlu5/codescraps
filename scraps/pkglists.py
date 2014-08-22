import sys, urllib2
from HTMLParser import HTMLParser

class DebPkgParse(HTMLParser):
    # Debian/Ubuntu are nice and give us meta tags in the beginning of the page
    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            attrs = dict(attrs)
            try:
                if attrs['name'] == "Description":
                    self.tags.append(attrs['content'])
                elif attrs['name'] == "Keywords":
                    self.tags.extend(attrs['content'].replace(",","").split())
            except KeyError: pass
    def feed(self, data):
        self.tags = []
        HTMLParser.feed(self, data)
        return self.tags

parser = DebPkgParse()

print "http://packages.debian.org/{}/{}".format(sys.argv[1],sys.argv[2])
fd = urllib2.urlopen("http://packages.debian.org/{}/{}".format(sys.argv[1],sys.argv[2]))
#fd = urllib2.urlopen("http://packages.debian.org/jessie/hexchat")
p = parser.feed(fd.read())
if len(p) != 7:
    print("Error")
else: print "Package: {} ({}) in {} {} - {}".format(sys.argv[2], p[-1], p[1], p[2], p[0])