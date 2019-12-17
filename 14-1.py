import re
import sys
import json
import itertools
import math
import fractions
from collections import defaultdict
sys.setrecursionlimit(5000)

def canmake_fuel(prod:dict, bag:dict, cur:str, depth:int)
    if cur == 'ORE':
        return

    for inp, needOfInp in prod[cur]['i']:
        if inp == 'ORE':
            #print(' ' * depth, '  =>  ', i[0], i[1], i[1] * frac)
            #ores[cur] += (frac * i[1])
            break

        

        #print(' ' * depth, i[0], 'need', i[1] * frac, 'canmake', tomake[i[0]], 'mult', nfrac)
        recur(prod, i[0], depth + 1, nfrac)
    pass

with open('14-test1.txt') as f:
    fuel = None
    prod = dict()
    needsore = dict()
    oretomake = dict()
    tomake = dict()

    oreNodes = dict()

    for line in (l.strip() for l in f.readlines()):
        sides = line.split(' => ')

        made = sides[1].split(' ')
        inputs = []
        for x in sides[0].split(', '):
            inp = x.split(' ')
            inputs.append((inp[1], int(inp[0])))
            if inp[1] == 'ORE':
                oretomake[made[1]] = int(inp[0])
                oreNodes[made[1]] = made[0]

        tomake[made[1]] = int(made[0])
        prod[made[1]] = {'c':int(made[0]), 'i': inputs}

    bag = defaultdict(lambda:0)
    oreMade = defaultdict(lambda:0)

    for ch, co in oreNodes.items():
        print('{} ORE for {} {}'.format(oretomake[ch], co, ch))
        bag[ch] += co
        oreMade[ch] += oretomake[ch]
    
