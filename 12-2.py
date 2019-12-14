import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

"""
from xlsx
moon 0
 x:  58171, [169988,48383,6335,1344,2110,2110,1344,6335,48383]
 y:  52740, [55946,49460,1882,1399,1399,1882,49460]
 z:  96209, [26,26,2073,1449,64,8044,2207,7249,5232,698,17581,89,6812,89,17581,698,5232,7249,2207,8044,64,1449,2073]

moon 1:
 x: 43623 [199084,34488,9136,9136,34488]
 y: 161427 [114,223,8,38,59713,41236,59713,38,8,223,114]
 z: 96235 [456,4,29,5193,2016,4348,13644,716,6084,8908,2156,1985,1043,1115,173,496,173,1115,1043,1985,2156,8908,6084,716,13644,4348,2016,5193,29,4,456]

moon 2:
 x: 286331 [11872,349,44446,80999,501,9998,501,80999,44446,349,11872]
 y: 156809 [2314,2244,24,12,24,24,12,24,2244,2314,44120,2594,5059,48646,5059,2594,44120]
 z: 48117 [1673,790,5278,32636,5278,790,1673]

moon 3:
 x: 50923 [184484,50924,50924,184484]  # 470816, 
 y: 161415 [12,12,139,12,5113,52380,8,46100,8,52380,5113,12,139]
 z: 48081 [26,10,10,26,3268,343,4037,7281,6269,5650,6269,7281,4037,343,3268]
"""

moons = {}

moons[0] = {0: (58171, [169988,48383,6335,1344,2110,2110,1344,6335,48383]),
            1: (52740, [55946,49460,1882,1399,1399,1882,49460]),
            2: (96209, [26,26,2073,1449,64,8044,2207,7249,5232,698,17581,89,6812,89,17581,698,5232,7249,2207,8044,64,1449,2073])}

moons[1] = {0: (43623, [199084,34488,9136,9136,34488]),
            1: (161427, [114,223,8,38,59713,41236,59713,38,8,223,114]),
            2: (96235, [456,4,29,5193,2016,4348,13644,716,6084,8908,2156,1985,1043,1115,173,496,173,1115,1043,1985,2156,8908,6084,716,13644,4348,2016,5193,29,4,456])}

moons[2] = {0: (286331, [11872,349,44446,80999,501,9998,501,80999,44446,349,11872]),
            1: (156809, [2314,2244,24,12,24,24,12,24,2244,2314,44120,2594,5059,48646,5059,2594,44120]),
            2: (48117, [1673,790,5278,32636,5278,790,1673])}

moons[3] = {0: (50923, [184484,50924,50924,184484]),
            1: (161415, [12,12,139,12,5113,52380,8,46100,8,52380,5113,12,139]),
            2: (48081, [26,10,10,26,3268,343,4037,7281,6269,5650,6269,7281,4037,343,3268])}

msteps = []
mpos = []
for i in range(0,4):
    msteps.append( [moons[i][0][0], moons[i][1][0], moons[i][2][0]] )
    mpos.append( [0,0,0] )

print(msteps)
print(mpos)

i = 0
while True:
    for m in range(0, 4):
        for c in range(0, 3):
            if m == 3 and c == 0:
                msteps[m][c] += moons[m][c][1][mpos[m][c]]
                mpos[m][c] += 1
                if mpos[m][c] == len(moons[m][c][1]):
                    mpos[m][c] = 0
                continue

            while msteps[m][c] < msteps[3][0]:
                msteps[m][c] += moons[m][c][1][mpos[m][c]]
                mpos[m][c] += 1
                if mpos[m][c] == len(moons[m][c][1]):
                    mpos[m][c] = 0

    allEq = True
    for m in range(0, 4):
        for c in range(0, 3):
            if msteps[m][c] != msteps[0][0]:
                allEq = False
                break
        if not allEq:
            break

    if allEq:
        print('match', msteps[0][0])
        break

    i += 1
    if i % 100000 == 0:
        print(msteps[3][0])

exit()


with open('12.txt') as f:
    moons = {}
    i = 0
    orig = {}
    for line in [x.strip()[1:-1] for x in f.readlines()]:
        coords = line.split(', ')
        data = [a.split('=') for a in coords]
        moons[i] = {'p': [int(data[0][1]), int(data[1][1]), int(data[2][1])], 'v':[0,0,0]}
        orig[i] = {'p': [int(data[0][1]), int(data[1][1]), int(data[2][1])], 'v':[0,0,0]}
        i += 1

    #print(moons)

    cycles = defaultdict(list)

    step = 0
    while True:

        if step > 0 and step % 1000000 == 0:
            #print(step)
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
                if moons[m]['p'][i] == orig[m]['p'][i] and moons[m]['v'][i] == orig[m]['v'][i]:
                    cycles[(m,i)].append(step)
            
        step += 1

for m in range(0,4):
    for coord in range(0,3):
        print(m, coord)
        for s in cycles[(m,coord)]:
            print(s)
        print()
