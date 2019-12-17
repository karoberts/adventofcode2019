import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

def make_base(pos:int, dlen:int):
    basesig = [0, 1, 0, -1]
    bpos = 1
    ngen = pos
    while ngen < dlen + 1:
        for j in range(0, pos + 1):
            yield basesig[bpos]
            ngen += 1
        bpos += 1
        if bpos == 4: bpos = 0


with open('16.txt') as f:
    digits = [int(x) for x in f.readline().strip()]
    #digits = [1,2,3,4,5,6,7,8]

    odigits = [None] * len(digits)
    for phase in range(0, 100):
        for d in range(0, len(digits)):
            val = 0
            i = d
            for pat in make_base(d, len(digits)):
                val += pat * digits[i]
                i += 1
                if i == len(digits):
                    break
            val = abs(val) % 10
            odigits[d] = val
        digits = odigits
        print(phase + 1)
        #print(phase, odigits)

    print(''.join((str(x) for x in odigits[0:8])))
