# The MIT License (MIT)

# Copyright (c) 2014 James Lu (GLolol)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
    import re
    numfind = re.compile(r'-\d+\.\d+|\d+\.\d+|-\d+|\d+')
    fracfind = re.compile(r'/')
    # fractions = re.compile(r'-\d+/-\d+|-\d+/\d+|\d+/-\d+|\d+/\d+')
    while True:
        co = raw_input("Enter two pairs of coordinates in the form (a, b),"
            " (c, d): ")
        if fracfind.search(co):
            print("Fraction (/) detected, please input all values separately...")
            fracs = nums = []
            fracs.append(raw_input("x1: "))
            fracs.append(raw_input("x2: "))
            fracs.append(raw_input("y1: "))
            fracs.append(raw_input("y2: "))
            for n in fracs:
                fracl = re.split("/", str(n))
                if len(fracl) == 2:
                    try:
                        nums.append(float(fracl[0])/float(fracl[1]))
                    except (ValueError, ZeroDivisionError):
                        print("Error, not a fraction!")
                else:
                    try:
                        nums.append(float(fracl[0]))
                    except (ValueError, ZeroDivisionError):
                        print("Error, not a fraction!")
        else:
            nums = re.findall(numfind, co)
        if len(nums) == 4:
            x1, y1, x2, y2 = nums
            if x1 == x2 and y1 == y2:
                # Sanity check!
                print("\nThose two points are the same! Try again.")
            else:
                break
        else:
            print("\nInvalid input. Try again.")
            continue

    m = getslope(x1, y1, x2, y2)
    if m == None:
        mstr = 'undefined'
    else:
        mstr = m
    print("\nThe slope of ({}, {}) and ({}, {}) is {}.".format(x1, y1, x2,
        y2, mstr))
    if isverticalline(x1, y1, x2, y2):
        print("This is a vertical line!")
    elif ishorizontalline(x1, y1, x2, y2):
        print("This is a horizontal line!")
    print("Slope equation: {}".format(intercept(m, x1, y1)))