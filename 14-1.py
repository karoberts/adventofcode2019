import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

with open('14-test1.txt') as f:
    fuel = None
    prod = dict()

    for line in (l.strip() for l in f.readlines()):
        sides = line.split(' => ')

        inputs = []
        for x in sides[0].split(', '):
            y = x.split(' ')
            inputs.append((y[1], int(y[0])))
        os = sides[1].split(' ')

        prod[os[1]] = {'c':int(os[0]), 'i': inputs}

    #print(prod)
    #print(prod['FUEL'])

    q = []
    q.append(('FUEL', 1))
    have = defaultdict(lambda:0)
    chneed = defaultdict(lambda:0)

    while len(q) > 0:
        n = q.pop(0)
        print('trying to make', n[1], n[0])

        if n[0] == 'ORE':
            continue

        for need in prod[n[0]]['i']:
            ineed = need[1] * n[1]
            canmake = prod[need[0]]['c'] if need[0] != 'ORE' else ineed
            multiple = ineed // canmake if ineed % canmake == 0 else ineed // canmake + 1

            q.append((need[0], need[1] * multiple))
            chneed[need[0]] += need[1] * multiple
            have[need[0]] += need[1] * multiple

    print(chneed)
