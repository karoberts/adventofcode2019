import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

def make_base(pos:int, dlen:int):
    basesig = [0, 1, 0, -1]
    bpos = 1
    ngen = d
    while ngen < dlen + 1:
        for j in range(0, pos + 1):
            yield basesig[bpos]
            ngen += 1
        bpos += 1
        if bpos == 4: bpos = 0


with open('16.txt') as f:
    orig_digits = [int(x) for x in f.readline().strip()]
    digits = []
    repeat = 10000

    #orig_digits = [1,2,3,4,5,6,7,8]
    #repeat = 10

    for i in range(0, repeat):
        digits.extend(orig_digits)

    #print(digits)

    offset = int(''.join((str(x) for x in orig_digits[0:8])))
    print('offset', offset, 'digitlen', len(digits))

    odigits = [None] * len(digits)
    for phase in range(0, 100):
        for d in range(0, len(digits)):
            val = 0
            print('dig', d)
            i = d
            #print('base gen')
            for pat in make_base(d, len(digits)):
                val += pat * digits[i]
                i += 1
                if i == len(digits):
                    break
            #print('calc')
            val = abs(val) % 10
            odigits[d] = val
            #print('next')
        digits = odigits
        #print(''.join((str(x) for x in digits[0:50])))
        print(phase + 1)
        #print(phase, odigits)

    print(''.join((str(x) for x in odigits[offset:offset+9])))

