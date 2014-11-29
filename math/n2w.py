#!/usr/bin/env python
# Licensed under cc by-sa 3.0, Adapted from http://stackoverflow.com/a/19193721
def numToWords(num):
    """<num>
    
    Converts an integer or float into words."""
    units = ('zero','one','two','three','four','five','six','seven','eight',
        'nine')
    teens = ('','eleven','twelve','thirteen','fourteen','fifteen','sixteen',
             'seventeen','eighteen','nineteen')
    tens = ('','ten','twenty','thirty','forty','fifty','sixty','seventy',
            'eighty','ninety')
    thousands = ('','thousand','million','billion','trillion','quadrillion',
                 'quintillion','sextillion','septillion','octillion',
                 'nonillion','decillion','undecillion','duodecillion',
                 'tredecillion','quattuordecillion','sexdecillion',
                 'septendecillion','octodecillion','novemdecillion',
                 'vigintillion')
    words = []
    if num == 0:
        return 'zero'
    if num <= 0:
        return "negative "+numToWords(abs(num))
    else:
        numStr = str(num).split(".")[0]
        groups = int((len(numStr)+2)/3)
        if numStr.startswith("0"): words.append("zero")
        numStr = numStr.zfill(groups*3)
        for i in range(0, groups*3, 3):
            h, t, u = map(int, (numStr[i], numStr[i+1], numStr[i+2]))
            g = int(groups-(i/3+1))
            if h >= 1:
                words.append(units[h])
                words.append('hundred')
            if t > 1:
                if u >= 1: 
                    words.append(tens[t]+"-")
                    words.append(units[u])
                else: 
                    words.append(tens[t])  
            elif t == 1:
                if u >= 1: 
                    words.append(teens[u])
                else: 
                    words.append(tens[t])
            else:
                if u >= 1:
                    words.append(units[u])
            if (g>=1) and ((h+t+u)>0): 
                words.append(thousands[g] + ',')
        try:
            decimals = str(num).split(".")[1]
            words.append("point")
        except IndexError: pass
        else: 
            for p in decimals: words.append(units[int(p)])
    s = ' '.join(words).replace("- ","-")
    if s.endswith(","): s = s[:-1]
    return s

if __name__ == "__main__":
    from sys import argv
    from os.path import basename
    try: 
        n = float(argv[1].replace(",", ""))
        print(numToWords(int(n) if n.is_integer() else n))
    except (ValueError, IndexError):
        print("Usage: %s <number>" % basename(__file__))
        for x in (0, 11, 109.5, 100100006, -6, 1020304050607, -8.02, 0.0432):
            print("%s -> %s" % (x, numToWords(x)))
