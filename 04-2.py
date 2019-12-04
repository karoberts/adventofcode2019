import re
import sys
import json
from collections import defaultdict
sys.setrecursionlimit(5000)

start = 382345
stop  = 843167

def proc(x):
    digs = [int(d) for d in str(x)]
    min = digs[0]
    for i in digs[1:]:
        if i < min:
            return False
        min = i

    counts = defaultdict(lambda:0)
    for i in digs:
        counts[i] += 1

    num2s = 0
    numMors = 0
    for c in counts.values():
        if c == 2: num2s += 1
        if c > 2: numMors += 1

    if num2s == 0:
        return False

    return True

print(proc(111222))

npass = 0
for x in range(start, stop + 1):
    if proc(x):
        npass += 1

print(npass)

#with open('04.txt') as f:
 #   lines = [x.strip() for x in f.readlines()]

