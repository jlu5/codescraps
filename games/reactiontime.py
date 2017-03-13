#!/usr/bin/env python
from __future__ import print_function
from RPi import GPIO
import time
import sys
import random
import threading

#TARGET_STRING = 'QUACK'
MIN_TIME = 0.2
MAX_TIME = 3

TARGET_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TARGET_PIN, GPIO.OUT)

ison = False

def led(state=None):
    global ison
    if state is not None:
        ison = state
    else:
        ison = not ison
    GPIO.output(TARGET_PIN, GPIO.HIGH if ison else GPIO.LOW)

if sys.version_info[0] <= 2:  # Python 2 support
    input = raw_input

#print('Instructions: when the string %r shows up, press the Enter key to check your reaction time!' % TARGET_STRING)
print("Instructions: You are an economical engineer who is trying to minimize their energy "
      "bills by turning off all the lights when they aren't being used. When the light turns on, "
      "hit enter to turn it back off!")
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

        #print(TARGET_STRING)
        led(True)

        popup_inactive.wait()

t = threading.Thread(target=wait)
t.daemon = True
t.start()

while True:
    try:
        input()
    except KeyboardInterrupt:
        # Allow quitting on Ctrl+C
        print_stats()
        led(False)
        sys.exit()

    if popup_inactive.is_set():
        print('You pressed the button too early! :(')
        misses += 1
    else:
        result = time.time() - popup_time
        print('Your reaction time: %f seconds' % result)
        led(False)
        results.append(result)

        popup_inactive.set()
