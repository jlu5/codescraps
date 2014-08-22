asleep = 1

######
import time

sheep = 0
if not asleep:
    print("Not asleep!")
    exit()
while True:
    try:
        sheep += 1
        print("{} sheep, ").format(sheep)
        time.sleep(0.3)
    except KeyboardInterrupt:
        print "bai."
        exit()