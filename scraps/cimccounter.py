global DIGITS
DIGITS = 7

def f(nums):
    """Returns a list (w, x, y, z), where w is the number of 0's given,
    and x,y, and z are the amount of 1's, 2's, and 3's given respectively."""
    res = [nums.count(num) for num in range(DIGITS)]
    return res
    
if __name__ in '__main__':
    from os.path import basename
    import sys
    if '--help' in sys.argv:
        print("usage: %s [--help] --nums]" % basename(__file__))
        sys.exit(0)
    elif '--combinations' in sys.argv:
        import itertools
        for x in itertools.product(range(DIGITS), repeat=DIGITS):
            x = list(x)
            res = f(x)
            in_text = ', '.join([str(n) for n in x])
            out_text = ', '.join([str(n) for n in res])
            # sys.stderr.write("Trying: (%s)\n" % in_text)
            if x == res:
                print("Matching combination: (%s)" % out_text)
            # else:
                # print("Output for (%s): (%s)" % (in_text, out_text))
    else:
        inp = raw_input("Enter %s numbers in the form 'a b c d ...': " % DIGITS)
        nums = list(map(int, inp.split()))
        if not all(i <= DIGITS for i in nums):
            print("Numbers should be <%s." % DIGITS)
            sys.exit(1)
        print(f(nums))