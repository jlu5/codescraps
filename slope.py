#!/usr/bin/env python2
def getslope(x1, y1, x2, y2):
    # Don't bother checking for ValueError, you shouldn't be putting things
    # that aren't numbers here anyways.
    x2, y2, x1, y1 = float(x2), float(y2), float(x1), float(y1)
    try:
        m = (y2 - y1) / (x2 - x1)
    except ZeroDivisionError:
        return None
    else:
        if m.is_integer():
            # If applicable turn this into an integer, so we don't have extra
            # .0's in the final result.
            return int(m)
        else:
            return m

def intercept(m, x, y):
    if m == None:
        return 'x = {}'.format(x)
    elif m == 0:
        return 'y = {}'.format(y)
    x, y, = float(x), float(y)
    # Slope equation: y = m*x + b
    b = y - (m*x)
    if b.is_integer():
        b = int(b)
    if b >= 0:
        bstr = '+ ' + str(b)
    else:
        # Handle negative numbers properly so we don't get things like y = 5x + -14
        bstr = '- ' + str(abs(b))
    return "y = {}x {}".format(m, bstr)

def isverticalline(x1, y1, x2, y2):
    if x1 == x2:
        return True
    return False

def ishorizontalline(x1, y1, x2, y2):
    if y1 == y2:
        return True
    return False

if __name__ == '__main__':
    import re, sys
    numfind = re.compile(r"-?\d+\.?\d*/-?\d+\.?\d*|-?\d+\.?\d*")
    signs = re.compile(r"[a-zA-Z+*\\]")
    getargs, nums = False, []
    while True:
        try:
            if len(sys.argv) == 5 and getargs == False:
                getargs = True
                co = "%s %s %s %s" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
            else:
                co = raw_input("Enter two pairs of coordinates in the form: x1, x2,"
                    " y1, y2: ")
            if re.findall(signs, co):
                print("Invalid input. Please do not enter any letters "
                    "or mathematical symbols.")
                continue
            for n in re.findall(numfind, co):
                if "/" in n:
                    nums.append(eval("1.0*" + n))
                else:
                    nums.append(n)
            if len(nums) == 4:
                x1, y1, x2, y2 = nums
                if x1 == x2 and y1 == y2:
                    # Sanity check!
                    print("\nThose two points are the same!")
                else:
                    break
            else:
                # print("\nInvalid input. Try again.")
                continue
        except KeyboardInterrupt:
            print('\nExiting...')
            sys.exit()

    m = getslope(x1, y1, x2, y2)
    print("\nThe slope of ({}, {}) and ({}, {}) is {}.".format(x1, y1, x2,
        y2, m if m != None else "undefined"))
    if isverticalline(x1, y1, x2, y2):
        print("This is a vertical line!")
    elif ishorizontalline(x1, y1, x2, y2):
        print("This is a horizontal line!")
    print("Slope equation: {}".format(intercept(m, x1, y1)))
    
    try:
        raw_input("Press Enter to continue... ")
    except KeyboardInterrupt:
        pass
