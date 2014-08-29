import sys
s = ' '.join(sys.argv[1:])
if s:
    n = 1
    l = 0
    while n < len(s) and l < 5000:
        print(s[:n])
        n += 1
        l += 1
    else:
        while n > 0 and l < 5000:
            print(s[:n])
            n -= 1
            l += 1
        else: print("Total of {} lines printed.".format(l))