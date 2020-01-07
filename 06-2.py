import re
import sys
import json
from collections import defaultdict
sys.setrecursionlimit(5000)

def recur2(n, nodes):
    path = []
    while n != 'COM':
        path.append(n)
        n = nodes[n]
    return path

#with open('06-test2.txt') as f:
with open('06.txt') as f:
    orbs = [x.strip().split(')') for x in f.readlines()]

    #nodes = defaultdict(list)
    nodes2 = dict()
    for o in orbs:
        #nodes[o[0]].append(o[1])
        nodes2[o[1]] = o[0]

    #print(nodes2)

    you_path = recur2('YOU', nodes2)
    san_path = recur2('SAN', nodes2)

    #print('you', you_path)
    #print('san', san_path)

    yp = len(you_path) - 1
    sp = len(san_path) - 1
    while you_path[yp] == san_path[sp]:
        yp -= 1
        sp -= 1

    c = yp + sp

    print('part2', c)
