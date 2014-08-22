import sys

try:
    s = int(raw_input("Enter an amount of seconds: "))
except ValueError:
    print "try again"
    sys.exit(1)
else:
    if s < 1:
        print "try again"
        sys.exit(1)
    
# divmod gives a pair of numbers: the quotient and remainder.
# For example, dividing 's' (seconds) by 60 will yield 'm' amount of complete minutes +
# 's' remaining seconds, and so on.

m, s = divmod(s, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)
w, d = divmod(d, 7)

elapsed = "Elapsed time: {}w {}d {}h {}m {}s".format(w, d, h, m, s)
print elapsed