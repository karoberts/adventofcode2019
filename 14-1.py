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
    q.append('FUEL')
    extras = defaultdict(lambda:0)
    chneed = defaultdict(lambda:0)
    chneed['FUEL'] = 1
    ore = 0

    while len(q) > 0:
        ch = q.pop(0)
        n = (ch, chneed[ch])
        print('trying to make', n[1], n[0])

        for need in prod[n[0]]['i']:
            if chneed[n[0]] == 0:
                continue

            if need[0] == 'ORE':
                if n[1] % prod[n[0]]['c'] == 0:
                    needore = (n[1] // prod[n[0]]['c']) * need[1]
                elif n[1] < prod[n[0]]['c']:
                    needore = need[1]
                else:
                    needore = ((n[1] // prod[n[0]]['c']) + 1) * need[1]
                print('  need ORE', needore, 'd', n[1], need[1], prod[n[0]]['c'])
                ore += needore
                chneed[n[0]] = 0
                continue

            ineed = need[1] * n[1]
            canmake = prod[need[0]]['c']
            if ineed % canmake == 0:
                multiple = ineed
            elif ineed < canmake:
                multiple = canmake
                print('    making', multiple - ineed, 'extra', need[0])
                extras[need[0]] += (multiple - ineed)
            else:
                multiple = ((ineed // canmake) + 1) * canmake
                while extras[need[0]] > 0 and multiple % ineed != 0:
                    print('    using an extra', need[0])
                    multiple -= 1
                    extras[need[0]] -= 1
                print('    making', multiple - ineed, 'extra', need[0])
                extras[need[0]] += (multiple - ineed)

            print('  need to make', multiple, need[0])
            q.append(need[0])
            chneed[need[0]] += multiple

    print(chneed)
    print(extras)
    print(ore)
