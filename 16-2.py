import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

with open('16.txt') as f:
    orig_digits = [int(x) for x in f.readline().strip()]
    digits = []
    repeat = 10000

    #orig_digits = [int(x) for x in '03036732577212944063491565474664']
    #repeat = 10000

    for i in range(0, repeat):
        digits.extend(orig_digits)

    #print(digits)

    offset = int(''.join((str(x) for x in orig_digits[0:7])))
    digits = list(reversed(digits[offset:]))
    print('offset', offset, 'digitlen', len(digits))

    odigits = [None] * len(digits)
    for phase in range(0, 100):
        lastv = 0
        for d in range(0, len(digits)):
            val = 0
            val += (digits[d] + lastv)
            val = abs(val) % 10
            lastv = val
            odigits[d] = val
        digits = odigits
        #print(''.join((str(x) for x in digits[0:50])))
        print(phase + 1)
        #print(phase, odigits)

    print(*list(reversed(digits))[:8], sep='')

# 39731117 too low
# 51553111 too low

# 87880114 too high
