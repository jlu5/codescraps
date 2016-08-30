#!/usr/bin/env python3
import sys
import random

with open('namegen-starts.txt') as f:
    starts = f.read().splitlines()
with open('namegen-middles.txt') as f:
    middles = f.read().splitlines()
with open('namegen-ends.txt') as f:
    ends = f.read().splitlines()

def namegen():
    syllable_count = random.randint(0, 2)
    name = "{}{}{}".format(random.choice(starts), ''.join(random.sample(middles, syllable_count)), random.choice(ends))
    return name

if __name__ == "__main__":
    try:
        names = int(sys.argv[1])
    except (IndexError, ValueError):
        names = 3
    for n in range(names):
        print(namegen())
