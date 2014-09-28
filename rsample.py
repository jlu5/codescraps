#!/usr/bin/env python2
import random

L = ['apple', 'banana', 'pear', 'watermelon', 'peach', 'grape', 'strawberry', 'pineapple', 'kiwi', 'mango', 'lettuce', 'tomato', 'pumpkin']
M = ['milkshake', 'taco', 'hot dog', 'burger', 'salad', 'wrap', 'vinegar', 'entree', 'stir fry', 'pancake', 'sauce', 'delicacy', 'cookie']
print "Sampling things without replacement! Total items: {}/{}\n".format(len(L), len(M))

while len(L) > 2:
    random.shuffle(L)
    print("{} {}".format(L.pop(), M.pop()))
    # print L
else:
    print "\nnot enough items left to choose from!"
