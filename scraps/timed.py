import time
import thread

starttime = time.time()
elapsed = 0
max = 5
print("Little test of time-limited actions. Say 'o' to continue. ")
while True:
    if raw_input() == "o":
        print("Received op, waiting {} seconds!".format(max))
        while elapsed < max:
            elapsed = time.time() - starttime