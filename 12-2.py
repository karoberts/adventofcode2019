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

    states = dict()
    states[str(moons)] = (moons, 0)

    print(moons)

    xs = [moons[0]['p'][0]]
    
    step = 0
    while True:

        if step > 0 and step % 10000 == 0:
            print(step)
            break

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
            
        #print(step, moons[0]['v'][0])

        xs.append(moons[0]['p'][0])

        step += 1

        hash = str(moons)
        if hash in states:
            print('dupe', states[hash][1], moons)
            break
        states[hash] = (moons, step)


    #print(moons)
    print('part2', step)

    for i in range(1,len(xs) // 2):
        if xs[:i] == xs[i:i*2]:
            print('cycle at', i)