import re
import socket

print 'Type a cloaked or uncloaked IP address.'
string = raw_input()

# v4ip = re.match("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", string)
v4cloaked = re.match("^(?:[0-9]{1,3}\.){2}[a-z]{1,3}\.[a-z]{1,3}", string)
v6cloaku = re.match("([0-9A-F]{8}:){3}IP", string)
v6cloakc = re.match("([0-9a-z]{1,4}:{1,2}){2,8}", string)
try:
    v6ip = socket.inet_pton(socket.AF_INET6, string)
except socket.error:
    pass
except AttributeError:
    # inet_pton not implemented on platform, use regexp instead
    v6ip = re.match("([0-9a-f]{1,4}:{1,2}){2,8}", string)
try:
    v4ip = socket.inet_aton(string)
except socket.error:
    v4ip = ''

if v4ip:
    print 'Matches an IPv4 address.'
elif v6ip:
    print 'Matches an IPv6 address.'
elif v4cloaked:
    print 'Matches a cloaked IPv4 Iaddress.'
elif v6cloaku:
    print 'matches Unreal-style IPv6 cloak.'
elif v6cloakc:
    print 'matches charybdis-style IPv6 cloak.'
else:
    print 'Does not match!'
print ''
raw_input("Press Enter to continue...")