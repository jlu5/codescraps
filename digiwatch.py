import time, sys, os

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

try:
    t = float(sys.argv[1])
except (ValueError, IndexError):
    t = 0.5
else:
    if t <= 0.05 or t >= 10:
        print "NOPE"
        sys.exit(1)
    
try:
    while True:
        cls()
        s1 = time.strftime('Current time: %I:%M:%S', time.localtime())
        s2 = str(time.time()).split(".")[1]
        s3 = time.strftime(' %p, %B %d, %Y (%Z)', time.localtime())
        print("{}.{}{}".format(s1, s2, s3))
        # raw_input()
        time.sleep(t)
except KeyboardInterrupt:
    sys.exit()