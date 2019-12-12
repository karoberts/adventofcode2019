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

    states = dict()

    step = 0
    while True:

        if step % 10000 == 0:
            print(step)

        for mk1 in range(0, len(moons)):
            for mk2 in range(mk1 + 1, len(moons)):
                if mk1 == mk2:
                    continue
                m1 = moons[mk1]
                m2 = moons[mk2]
                for i in range(0,3):
                    if m1['p'][i] == m2['p'][i]:
                        pass
                    elif m1['p'][i] < m2['p'][i]:
                        m1['v'][i] += 1
                        m2['v'][i] -= 1
                    else:
                        m1['v'][i] -= 1
                        m2['v'][i] += 1

        for m in moons.keys():
            for i in range(0,3):
                moons[m]['p'][i] += moons[m]['v'][i]

        hash = str(moons)
        if hash in states:
            break
        states[hash] = moons

        step += 1

    print('part2', step)