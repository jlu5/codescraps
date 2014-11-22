#!/usr/bin/env python2
import random, time, sys

tries = 0
fails = 0
while True:
    if fails >= 5:
        print "\nIs this some sort of joke? I'm outta here."
        sys.exit() 
    elif fails == 0 and len(sys.argv) > 1:
        s = sys.argv[1] # Try to use arguments given to start IF present
    else:
        s = raw_input("Pick a number between 1 and 100: ")
    try:
        n = int(s)
    except ValueError:
        fails = fails + 1
    else:
        if n > 100 or n < 1: 
            fails = fails + 1
        else: 
            break
        
while True:
    r = random.randint(1, 100)
    time.sleep(0.02) # Do this so the script doesn't hog the CPU
    if tries >= 250:
        print 'Max. amount of tries ({}) reached, terminating...'.format(tries)
        break
    if r != n:
        print 'Random number is not {}, trying again... (found {})'.format(n, r)
        tries = tries + 1
    else: 
        if tries <= 10:
            print 'Wow, you got {} in only {} tries? Impressive!'.format(r, tries)
        else: 
            print 'Random number {} found! It took {} tries to get this!'.format(r, tries)
        raw_input()
        break