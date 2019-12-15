import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

with open('14-test1b.txt') as f:
    fuel = None
    prod = dict()
    needsore = dict()
    oretomake = dict()

    for line in (l.strip() for l in f.readlines()):
        sides = line.split(' => ')

        os = sides[1].split(' ')
        inputs = []
        for x in sides[0].split(', '):
            y = x.split(' ')
            inputs.append((y[1], int(y[0])))
            if y[1] == 'ORE':
                oretomake[os[1]] = int(y[0])

        prod[os[1]] = {'c':int(os[0]), 'i': inputs}

    for k,v in prod.items():
        for i in v['i']:
            if i[0] == 'ORE':
                needsore[k] = v['c']

    print('needsore', needsore)
    print('oretomake', oretomake)

    #print(prod)
    #print(prod['FUEL'])

    q = []
    q.append('FUEL')
    extras = defaultdict(lambda:0)
    chneed = defaultdict(lambda:0)
    chneed['FUEL'] = 1

    oreneed = defaultdict(lambda:0)

    while len(q) > 0:
        ch = q.pop(0)
        n = (ch, chneed[ch])
        print('trying to make', n[1], n[0])

        for need in prod[n[0]]['i']:
            if chneed[n[0]] == 0:
                continue

            ineed = need[1] * n[1]

            if need[0] in needsore:
                print('  - will need ORE for ', ineed, need[0])
                oreneed[need[0]] += ineed
                continue

            canmake = prod[need[0]]['c']

            if ineed % canmake == 0:
                multiple = ineed
            elif ineed < canmake:
                multiple = canmake
                #print('    making', multiple - ineed, 'extra', need[0])
                #extras[need[0]] += (multiple - ineed)
            else:
                multiple = ((ineed // canmake) + 1) * canmake
                """
                while extras[need[0]] > 0 and multiple % ineed != 0:
                    print('    using an extra', need[0])
                    multiple -= 1
                    extras[need[0]] -= 1
                print('    making', multiple - ineed, 'extra', need[0])
                """
                #extras[need[0]] += (multiple - ineed)

            print('  need to make', multiple, need[0])
            q.append(need[0])
            chneed[need[0]] += multiple

    #print(chneed)
    #print(extras)
    print('oreneed', oreneed)

    ore = 0
    for k, v in oreneed.items():
        print('** need to make', v, k, 'with', needsore[k], k, 'per', oretomake[k], 'ORE' )
        o = 0
        if v % needsore[k] == 0:
            o = (v // needsore[k]) * oretomake[k]
        elif v < needsore[k]:
            o = needsore[k] * oretomake[k]
        else:
            o = (v // needsore[k] + 1) * oretomake[k]
        print('  used', o, 'ORE to make', v, k)
        ore += o

    print(ore)
