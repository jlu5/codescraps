import sys
import string

if sys.version_info[0] >= 3:
    raw_input = input

text = raw_input('Input something: ')
for char in text:
    if char not in string.printable:
        print('Not ASCII')
        break
else:
    print('ASCII')