import re
import sys
import json
import itertools
import math
import fractions
from collections import defaultdict
sys.setrecursionlimit(5000)

ores = defaultdict(lambda:fractions.Fraction(0,1))
makefrac = defaultdict(lambda:fractions.Fraction(0,1))

def recur(prod:dict, cur:str, depth:int, frac):
    global ores

    if cur == 'ORE':
        return

    for i in prod[cur]['i']:
        if i[0] == 'ORE':
            print(' ' * depth, '  =>  ', i[0], i[1], i[1] * frac)
            ores[cur] += (frac * i[1])
            break

        nfrac = frac * fractions.Fraction(i[1], tomake[i[0]])
        makefrac[i[0]] += nfrac

        print(' ' * depth, i[0], 'need', i[1] * frac, 'canmake', tomake[i[0]], 'mult', nfrac)
        recur(prod, i[0], depth + 1, nfrac)
    pass

with open('14-test1b.txt') as f:
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

    print('FUEL')
    recur(prod, 'FUEL', 0, fractions.Fraction(1,1))

    print(ores)
    print(makefrac)
    s = fractions.Fraction()
    for k,v in ores.items():
        #if v.denominator > 1:
        r = math.ceil(float(v) / oretomake[k]) * oretomake[k]
        #else:
            #r = int(v)
        print(k, v, r, oretomake[k])
        s += r
    print(s, float(s))