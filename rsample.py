# coding=utf-8
import random
from sys import platform
if platform == 'win32':
    from os import system
    system('chcp 850')

L = ['apple', 'banana', 'pear', 'watermelon', 'peach', 'grape', 'strawberry', 'pineapple', 'kiwi', 'mango', 'lettuce', 'tomato', 'pumpkin']
M = ['milkshake', 'taco', 'hot dog', 'burger', 'salad', 'wrap', 'vinegar', 'entrée', 'stir fry', 'pancake', 'sauce', 'delicacy', 'cookie']
print "Sampling things without replacement! Total items: {}/{}\n".format(len(L), len(M))

while len(L) > 2:
    random.shuffle(L)
    print("{} {}".format(L.pop(), M.pop()))
    # print L
else:
    print "\nnot enough items left to choose from!"