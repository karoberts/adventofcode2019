import re
import sys
import json
import itertools
import math
import fractions
from collections import defaultdict
sys.setrecursionlimit(5000)

def canmake_fuel(prod:dict, tomake:dict, bag:dict, cur:str, prevNeed:int, depth:int):
    for inp, needOfInp in prod[cur]['i']:
        if inp == 'ORE':
            return

        if inp not in bag:
            print(' ' * depth, 'trying to make', needOfInp, inp)
            canmake_fuel(prod, tomake, bag, inp, needOfInp, depth + 1)

        print(' ' * depth, 'checking for', needOfInp * prevNeed, inp)
        if bag[inp] < needOfInp:
            print('not enough', inp, 'need', needOfInp, 'have', bag[inp])
            exit()

        print(' ' * depth, 'using', needOfInp * prevNeed, inp)
        bag[inp] -= (needOfInp * prevNeed)
        print(' ' * depth, 'bag has', bag[inp], inp, 'left')
        
    bag[cur] += tomake[cur] * prevNeed

    pass

with open('14-test2.txt') as f:
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
    oreneed = defaultdict(lambda:0)
    fracs = defaultdict(lambda:fractions.Fraction(0,1))

    while len(q) > 0:
        n = q.pop(0)
        print('trying to make', n[1], n[0])

        for need in prod[n[0]]['i']:

            if need[0] in needsore:
                if n[1] < tomake[n[0]]:
                    o = need[1]
                elif n[1] % tomake[n[0]] == 0:
                    o = (n[1] // tomake[n[0]]) * need[1]
                else:
                    print('==> making extra ORE')
                    o = math.ceil(n[1] / tomake[n[0]]) * need[1]

                print('o',o, 'n1', n[1], 'need1', need[1], 'tomaken0', tomake[n[0]], 'tomakeneed0', tomake[need[0]])

                print('  - will need ORE for ', o, need[0], need[1], n[1], tomake[need[0]], tomake[n[0]])
                oreneed[need[0]] += o
                continue

            fracneed = fractions.Fraction(need[1], tomake[n[0]])
            print('  need to make', fracneed, need[0])

            ineed = need[1] * n[1]
            #canmake = prod[need[0]]['c']

            #print('  need to make', ineed, need[0])
            #totneed[need[0]] += ineed
            q.append((need[0], ineed))

    print('totneed', totneed)
    print('oreneed', oreneed)

    bag = defaultdict(lambda:0)

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
        bag[k] = o 
        ore += o

    print(bag)
    print(ore)

    canmake_fuel(prod, tomake, bag, 'FUEL', 1, 0)

    print(bag)
