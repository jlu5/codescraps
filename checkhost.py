# Retrieved from http://freenode.net/irc_servers.shtml (11/03/2014)
# This list is just an example, it should theoretically work for any list.
hosts = [# Asia/Pacific Rim
        "banks.freenode.net",
        "bradbury.freenode.net",
        "brooks.freenode.net",
        "roddenberry.freenode.net",
        # Europe
        "adams.freenode.net",
        "barjavel.freenode.net",
        "calvino.freenode.net",
        "cameron.freenode.net",
        "gibson.freenode.net",
        "hitchcock.freenode.net",
        "hobana.freenode.net",
        "holmes.freenode.net",
        "kornbluth.freenode.net",
        "leguin.freenode.net",
        "orwell.freenode.net",
        "pratchett.freenode.net",
        "rajaniemi.freenode.net",
        "sendak.freenode.net",
        # "wolfe.freenode.net", # DNS dead (11/03/2014)
        # North America
        "asimov.freenode.net",
        "card.freenode.net",
        "dickson.freenode.net",
        "hubbard.freenode.net",
        "moorcock.freenode.net",
        "morgan.freenode.net",
        # "wright.freenode.net" # DNS dead (11/03/2014)
        ]
timeout = 1 # In seconds; auto-converted to milliseconds on Windows

###
import subprocess, sys, os
n, s = len(hosts), 0
if n == 0:
    print("No hosts defined to ping!")
    sys.exit()

print("Ping test started...")
for host in hosts:
    if sys.platform.startswith("linux"):
        try:
            FNULL = open(os.devnull, 'w')
            data = subprocess.call(["ping", host, "-c 1 -w {}".format(timeout)], stdout=FNULL)
        except KeyboardInterrupt:
            continue # Be patient!
    elif sys.platform == "win32":
        try:
            FNULL = open(os.devnull, 'w')
            data = subprocess.call("ping -w {} -n 1 {}".format(timeout*1000, host), stdout=FNULL)
        except KeyboardInterrupt:
            continue
    else:
        print("Unknown system version: {}".format(sys.platform))
    if data == 0:
        s = s + 1
        print("Ping to {} successful.".format(host))
    else: 
        print("Ping to {} failed.".format(host))
print "Finished, with a total of {}/{} hosts successfully reached.".format(s, n)
raw_input()
