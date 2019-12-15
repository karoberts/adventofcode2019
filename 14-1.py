import re
import sys
import json
import itertools
import math
from collections import defaultdict
sys.setrecursionlimit(5000)

with open('14-test1d.txt') as f:
    fuel = None
    prod = dict()
    needsore = dict()
    oretomake = dict()
    tomake = dict()

    totneed = defaultdict(lambda:0)

    for line in (l.strip() for l in f.readlines()):
        sides = line.split(' => ')

        os = sides[1].split(' ')
        inputs = []
        for x in sides[0].split(', '):
            y = x.split(' ')
            inputs.append((y[1], int(y[0])))
            if y[1] == 'ORE':
                oretomake[os[1]] = int(y[0])

        tomake[os[1]] = int(os[0])
        prod[os[1]] = {'c':int(os[0]), 'i': inputs}

    for k,v in prod.items():
        for i in v['i']:
            if i[0] == 'ORE':
                needsore[k] = v['c']

    print('needsore', needsore)
    print('oretomake', oretomake)
    print('tomake', tomake)

    #print(prod)
    #print(prod['FUEL'])

    q = []
    q.append(('FUEL', 1))
    extras = defaultdict(lambda:0)

    oreneed = defaultdict(lambda:0)

    extra_ore = 0

    while len(q) > 0:
        n = q.pop(0)
        print('trying to make', n[1], n[0])

        for need in prod[n[0]]['i']:
            ineed = need[1] * n[1]
            #print(need, n)

            if need[0] in needsore:
                if n[1] < tomake[n[0]]:
                    o = need[1]
                elif n[1] % tomake[n[0]] == 0:
                    o = (n[1] // tomake[n[0]]) * need[1]
                else:
                    print('==> making extra ORE')
                    o = math.ceil(n[1] / tomake[n[0]]) * need[1]
                    extra_ore += (o - (n[1] // tomake[n[0]]) * need[1])

                print('o',o, 'n1', n[1], 'need1', need[1], 'tomaken0', tomake[n[0]], 'tomakeneed0', tomake[need[0]])

                print('  - will need ORE for ', o, need[0], need[1], n[1], tomake[need[0]], tomake[n[0]])
                oreneed[need[0]] += o
                continue

            canmake = prod[need[0]]['c']

            print('  need to make', ineed, need[0])
            totneed[need[0]] += ineed
            q.append((need[0], ineed))

    print('totneed', totneed)
    print('oreneed', oreneed)

    ore = 0
    for k, v in oreneed.items():
        print('** need to make', v, k, 'with', needsore[k], k, 'per', oretomake[k], 'ORE' )
        o = 0
        if v < needsore[k]:
            o = needsore[k] * oretomake[k]
        elif v % needsore[k] == 0:
            o = (v // needsore[k]) * oretomake[k]
        else:
            o = math.ceil(v / needsore[k]) * oretomake[k]
        print('  used', o, 'ORE to make', v, k)
        ore += o

    print(ore)
    print(extra_ore)
