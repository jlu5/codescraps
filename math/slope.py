#!/usr/bin/env python
def getslope(x1, y1, x2, y2):
    """<x1> <y1> <x2> <y2>

    Returns the slope of a line, given x1, y1, x2, and y2.
    """
    # Don't bother checking for ValueError, you shouldn't be putting things
    # that aren't numbers here anyways.
    # x1, y1, x2, y2 = map(float, (x1, y1, x2, y2))
    try:
        m = 1.0*(y2 - y1) / (x2 - x1)
    except ZeroDivisionError:
        return None
    else:
        return int(m) if m.is_integer() else m

def intercept(m, x, y):
    """<slope> <x> <y>

    Formats and returns (as a string) a line in y intercept form (y = mx + b),
    given the slope and one pair of coordinates.
    """
    if m is None:
        return 'x = {}'.format(x)
    elif m == 0:
        return 'y = {}'.format(y)
    # Slope equation: y = m*x + b
    b = 1.0*y - (m*x)
    if b.is_integer():
        b = int(b)
    if b >= 0:
        bstr = '+ ' + str(b)
    else:
        # Handle negative numbers properly so we don't get things like y = 5x + -14
        bstr = '- ' + str(abs(b))
    if m == 1:
        m = ''
    elif m == -1:
        m = "-"
    return "y = {}x {}".format(m, bstr)

if __name__ == '__main__':
    import re, sys
    numfind = re.compile(r"-?\d+\.?\d*/-?\d+\.?\d*|-?\d+\.?\d*")
    getargs, nums = False, []
    if sys.version_info[0] < 3:
        input = raw_input
    while True:
        try:
            if len(sys.argv) == 5 and not getargs:
                getargs = True
                co = ' '.join(sys.argv[1:])
            else:
                co = input("Enter two pairs of coordinates in the form: x1, y1,"
                    " x2, y2: ")
            nums = re.findall(numfind, co)
            try:
                x1, y1, x2, y2 = map(float, nums[:4])
            except ValueError:
                print("\nInvalid input. Try again.")
            except IndexError:
                pass
            else:
                if x1 == x2 and y1 == y2:
                    print("\nThose two points are the same!")
                else:
                    break
                continue
        except KeyboardInterrupt:
            print('\nExiting...')
            sys.exit()

    m = getslope(x1, y1, x2, y2)
    print("\nThe slope of ({}, {}) and ({}, {}) is {}.".format(x1, y1, x2,
        y2, m if m is not None else "undefined"))
    if x1 == x2:
        print("This is a vertical line!")
    elif y1 == y2:
        print("This is a horizontal line!")
    print("Slope equation: {}".format(intercept(m, x1, y1)))
    if sys.platform == "win32":
        try:
            input("Press Enter to continue... ")
        except KeyboardInterrupt:
            pass
