import re
import sys
import json
import itertools
import math
import fractions
from collections import defaultdict
sys.setrecursionlimit(5000)

def canmake_fuel(prod:dict, tomake:dict, bag:dict, cur:str, prevNeed:int, depth:int):
    oredelt = 0
    for inp, needOfInp in prod[cur]['i']:
        if inp == 'ORE':
            print(' ' * depth, 'wants more ORE', needOfInp, prevNeed, tomake[cur])
            gen = 0
            while gen < prevNeed:
                bag[cur] += tomake[cur]
                gen += tomake[cur]
                oredelt += needOfInp
            return oredelt

        if inp not in bag:
            print(' ' * depth, 'trying to make', needOfInp * prevNeed, inp)
            oredelt += canmake_fuel(prod, tomake, bag, inp, needOfInp * prevNeed, depth + 1)

        if prevNeed < prod[cur]['c']:
            prevNeed = prod[cur]['c']
        #roundup = math.ceil(needOfInp / tomake[k]) * prevNeed
        roundup = math.ceil(prevNeed / prod[cur]['c']) * prod[cur]['c']
        if prevNeed < prod[cur]['c']:
            needNow = roundup
        elif prevNeed % prod[cur]['c'] != 0:
            print(' ' * depth, 'nums', needOfInp, tomake[k], prevNeed, roundup, prod[cur]['c'])
            needNow = roundup
            #exit()
        else:
            needNow = prevNeed // prod[cur]['c'] * needOfInp
        print(' ' * depth, 'checking for', needNow, inp)
        #print(' ' * depth, 'nums', needOfInp, tomake[k], prevNeed, roundup, prod[cur]['c'])
        if bag[inp] < needNow:
            print(' ' * depth, 'trying to make more', needNow - bag[inp], inp)
            oredelt += canmake_fuel(prod, tomake, bag, inp, needNow - bag[inp], depth + 1)

        if bag[inp] < needNow:
            print('not enough', inp, 'need', needNow, 'have', bag[inp])
            exit()

        print(' ' * depth, 'using', needNow, inp, 'of', bag[inp])
        bag[inp] -= needNow
        print(' ' * depth, 'bag has', bag[inp], inp, 'left')
        
    print(' ' * depth, 'adding', prevNeed, cur, 'to bag')
    bag[cur] += prevNeed

    return oredelt

with open('14-test4.txt') as f:
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

        roundup = math.ceil(v / needsore[k]) * needsore[k]

        print('  used', o, 'ORE to make', roundup, k)
        # print('     ', o, roundup, k, needsore[k], oretomake[k])
        bag[k] = roundup
        ore += o

    print(bag)

    oredelt = canmake_fuel(prod, tomake, bag, 'FUEL', 1, 0)

    bag['FUEL'] = 0

    for ch, c in bag.items():
        if c == 0: continue
        #if ch in needsore and c >= needsore[ch]:
        #    print('-- have', c - needsore[ch], 'too many', ch, prod[ch]['c'])
        if (c - prod[ch]['c']) >= prod[ch]['c']:
            print('-- have', c - prod[ch]['c'], 'too many (!)', ch, c, prod[ch]['c'])
            toremove = (c // prod[ch]['c']) * oretomake[ch]
            print('-- removing', toremove)
            oredelt -= toremove

    print(bag)
    print(ore)
    print(oredelt)
    print(ore + oredelt)
