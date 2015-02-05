#!/usr/bin/env python
# Adapted from http://stackoverflow.com/a/19193721
def numToWords(num):
    """<num>

    Converts an integer or float into words."""
    units = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
             'eight', 'nine')
    teens = ('eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
             'seventeen', 'eighteen', 'nineteen')
    tens = ('ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',
            'eighty', 'ninety')
    thousands = ('thousand', 'million', 'billion', 'trillion', 'quadrillion',
                 'quintillion', 'sextillion', 'septillion', 'octillion',
                 'nonillion', 'decillion', 'undecillion', 'duodecillion',
                 'tredecillion', 'quattuordecillion', 'sexdecillion',
                 'septendecillion', 'octodecillion', 'novemdecillion',
                 'vigintillion')
    words = []
    num = float(num)
    # Clobber trailing .0's in floats
    num = int(num) if num.is_integer() else num
    if num == 0:
        return 'zero'
    if num <= 0:
        # Handle negative numbers
        return "negative " + numToWords(abs(num))
    else:
        numStr = str(num).split(".")[0]
        groups = int((len(numStr) + 2) / 3)
        # This is needed for decimals (0.4 --> zero point four)
        if numStr.startswith("0"):
            words.append("zero")
        numStr = numStr.zfill(groups * 3)
        # Split up the number into digit groups
        for i in range(0, groups * 3, 3):
            # Each group will have hundreds (h), tens (t), and units (u)
            # e.g.: 1003 --> 1000 + 003 --> one thousand three
            h, t, u = map(int, (numStr[i], numStr[i+1], numStr[i+2]))
            g = int(groups - (i / 3 + 1))
            if h >= 1:
                # If hundreds count >= 1, add 'hundred' to the
                # output (e.g. 103, 9622)
                words.append(units[h])
                words.append('hundred')
            if t > 1:
                # Twenty, thirty, etc.
                if u >= 1:
                    # Compound numbers like 21 output 'twenty-one'
                    # instead of 'twenty one'
                    words.append(tens[t - 1] + "-")
                    words.append(units[u])
                else:
                    words.append(tens[t - 1])
            elif t == 1:
                if u >= 1:
                    # 11-19 (eleven, twelve, thirteen, etc.)
                    words.append(teens[u - 1])
                else:
                    # must be 10
                    words.append(tens[t - 1])
            else:
                if u >= 1:
                    # one, two, three, four, etc.
                    words.append(units[u])
            if (g >= 1) and ((h + t + u) > 0):
                # comma separates groups: "one million, three hundred and one"
                try:
                    words.append(thousands[g - 1] + ',')
                except IndexError:
                    raise ValueError("I can't count that high!")
        # Decimals are so much easier
        try:
            decimals = str(num).split(".")[1]
            words.append("point")
        except IndexError:
            pass
        else:
            words += [units[int(p)] for p in decimals]

    # Join everything together
    s = ' '.join(words)
    # 'twenty- one' --> 'twenty-one'
    s = s.replace("- ", "-")
    # Remove trailing commas
    s = s.strip(",")
    return s

if __name__ == "__main__":
    from sys import argv
    from os.path import basename
    try:
        n = float(argv[1].replace(",", ""))
        print(numToWords(n))
    except (ValueError, IndexError):
        print("Usage: %s <number>" % basename(__file__))
        for x in (0, 11, 100.5, 100100056, -6, 1020304050607, -8.02, 0.0432):
            print("%s -> %s" % (x, numToWords(x)))
