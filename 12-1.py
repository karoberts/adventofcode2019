import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

with open('12.txt') as f:
    moons = {}
    i = 0
    for line in [x.strip()[1:-1] for x in f.readlines()]:
        coords = line.split(', ')
        data = [a.split('=') for a in coords]
        moons[i] = {'p': [int(data[0][1]), int(data[1][1]), int(data[2][1])], 'v':[0,0,0]}
        i += 1
    print(moons)

    for step in range(0, 1000):

        for mk1 in range(0, len(moons)):
            for mk2 in range(mk1 + 1, len(moons)):
                if mk1 == mk2:
                    continue
                m1 = moons[mk1]
                m2 = moons[mk2]
                #print(mk1, mk2, m1, m2)
                for i in range(0,3):
                    if m1['p'][i] == m2['p'][i]:
                        pass
                    elif m1['p'][i] < m2['p'][i]:
                        m1['v'][i] += 1
                        m2['v'][i] -= 1
                    else:
                        m1['v'][i] -= 1
                        m2['v'][i] += 1
                #print(mk1, mk2, m1, m2)
                #input('a')

        #print(step, moons[0])
        #input('w')

        pot = [0] * len(moons)
        kin = [0] * len(moons)
        tot = [0] * len(moons)
        for m in moons.keys():
            for i in range(0,3):
                moons[m]['p'][i] += moons[m]['v'][i]
                pot[m] += abs(moons[m]['p'][i])
                kin[m] += abs(moons[m]['v'][i])
            tot[m] = pot[m] * kin[m]
            
    print(moons)
    print(pot, kin)
    print('part1', sum(tot))