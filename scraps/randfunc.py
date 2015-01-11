from itertools import product
from random import choice, randint

a = ('load', 'repeat', 'draw', 'redraw', 'unzip', 'passthrough', 'render', 'parse', 'get',
    'write', 'query', 'enumerate', 'connect', 'strip', 'crypt', 'unzip', 'compile', 'optimize',
    'make', 'fetch', 'filter', 'format', 'process', 'transcode')
b = ('texture', 'drawing', 'object', 'bevel', 'handler', 'database', 'registry', 'control',
    'function', 'response', 'update', 'link', 'file', 'device', 'memory', 'stream', 'handle',
    'processor')
b = list(map(str.title, b))

func = ''.join(choice(list(product(a,b))))
rhex = hex(randint(0,2**32))
rhex = rhex.replace("L", "")
print("ERR: UNSUPPORTED FUNCTION:{%s: %s}" % (func, rhex))