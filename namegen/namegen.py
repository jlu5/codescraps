import sys, random
with open('starts.txt') as f:
    starts = f.read().splitlines()
with open('middles.txt') as f:
    middles = f.read().splitlines()
with open('ends.txt') as f:
    ends = f.read().splitlines()

def namegen():
    numSyl = random.randint(0, 2)
    name = "{}{}{}".format(random.choice(starts), ''.join(random.sample(middles, numSyl)), random.choice(ends))
    return name

if __name__ == "__main__":
    try: names = int(sys.argv[1])
    except (IndexError, ValueError): names = 3
    for n in xrange(names): print namegen()