#!/usr/bin/env python

TARGET_STRING = 'QUACK'
MIN_TIME = 0.2
MAX_TIME = 3

import time
import sys
import random
import threading

if sys.version_info[0] <= 2:  # Python 2 support
    input = raw_input

print('Instructions: when the string %r shows up, press the Enter key to check your reaction time!' % TARGET_STRING)
print('Press CTRL-C to exit')

# Internal states
popup_time = 0
popup_inactive = threading.Event()
popup_inactive.set()

# Stats
misses = 0
results = []

def print_stats():
    hits = len(results)
    print()
    print('          Hits: %s' % hits)
    print('        Misses: %s' % misses)
    print('Total attempts: %s' % (hits+misses))
    if hits:
        print('     Best time: %f seconds' % min(results))
        print('    Worst time: %f seconds' % max(results))
        print('     Avg. time: %f seconds' % (1.0*sum(results)/hits))

def wait():
    global popup_time, popup_inactive
    while True:
        # Wait a while...
        time.sleep(random.uniform(MIN_TIME, MAX_TIME))
        popup_inactive.clear()

        popup_time = time.time()

        print(TARGET_STRING)

        popup_inactive.wait()

t = threading.Thread(target=wait, daemon=True)
t.start()

while True:
    try:
        input()
    except KeyboardInterrupt:
        # Allow quitting on Ctrl+C
        print_stats()
        sys.exit()

    if popup_inactive.is_set():
        print('You pressed the button too early! :(')
        misses += 1
    else:
        result = time.time() - popup_time
        print('Your reaction time: %f seconds' % result)
        results.append(result)

        popup_inactive.set()
