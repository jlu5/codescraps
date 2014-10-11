#!/usr/bin/env python2
import random, time, string, sys
characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b',
 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6',
 '7', '8', '9', '0', '+', '-', '*', '/', '.', ',', '\\', '\'', '`', '~', '!',
 '?', '@', '#', '$', '%', '^', '&', '_', '=', '|']
try:
    import terminalsize # https://gist.github.com/jtriley/1108174
    sizex, sizey = terminalsize.get_terminal_size()
except ImportError:
    print 'Missing required terminalsize module! Download it at:'
    ' https://gist.github.com/jtriley/1108174'
    sizex = len(characters) * 2
while sizex > len(characters):
    try:
        print string.join(random.sample(characters, random.randint(len(characters)/3, len(characters)))) * sizex
        time.sleep(random.uniform(0, 0.5))
    except KeyboardInterrupt:
        sys.stdout.write('\n===={ Stopped }=====\n')
        sys.exit()
print 'Terminal size too small!'
