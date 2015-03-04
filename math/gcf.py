#!/usr/bin/python
from factors import factors

def _gcf(first, second):
    """<first> <second>
    
    Finds the greatest common factor of two numbers."""
    first = factors(first)
    second = factors(second)
    common = set(first) & set(second)
    return sorted(common)[-1]

def _lcm(first, second):
    """<first> <second>
    
    Finds the lowest common multiple of two numbers."""
    first, second = map(int, (first, second))
    pass # finish this later

def gcf(*nums):
    """<number1> <number2> [<number3>] [<number4>]...
    
    Finds the greatest common factor of a series of numbers."""
    if len(nums) < 2:
        raise ValueError("need at least two numbers to find gcf of")
    res = _gcf(nums[0], nums[1])
    round = 2
    for s in nums:
        try:
            res = _gcf(res, nums[round])
        except IndexError:
            break
        else:
            round += 1
    return res

if __name__ == '__main__':
    from sys import argv
    args = argv[1:]
    gcf_res = gcf(*args)
    print("Greatest common factor of %s: %s" % (', '.join(args), gcf_res))
    if gcf_res == 1:
        print("These numbers are relatively prime.")
