import re
import sys
import json
from collections import defaultdict
sys.setrecursionlimit(5000)

def recur(n, nodes):
    c = 0
    for s in nodes[n]:
        c += (1 + recur(s, nodes))
    return c

def recur2(n, nodes):
    c = 0
    while n != 'COM':
        c += 1
        n = nodes[n]
    return c

with open('06.txt') as f:
    orbs = [x.strip().split(')') for x in f.readlines()]

    nodes = defaultdict(list)
    nodes2 = dict()
    for o in orbs:
        nodes[o[0]].append(o[1])
        nodes2[o[1]] = o[0]

    #print(nodes2)

    c = 0
    for n in nodes2:
        c += recur2(n, nodes2)

    print('part1', c)