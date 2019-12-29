import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

def printg(g, _max):
    for y in range(0, _max[1] + 1):
        for x in range(0, _max[0] + 1):
            c = (x,y)
            if c in g:
                print(g[c], end='')
            else:
                print(' ', end='')
        print()
    print()

def nextround(grid, x, y, _max):
    tests = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]
    k = (x,y)
    c = grid[k]

    nbugs = 0
    for t in tests:
        tx = x + t[0]
        ty = y + t[1]
        if tx < 0 or ty < 0 or tx >= _max[0] or ty >= _max[1]:
            continue
        tk = (tx, ty)
        tt = grid[tk]
        if tt == '#':
            nbugs += 1

    if c == '#':
        if nbugs != 1:
            return '.'
    elif c == '.' and (nbugs == 1 or nbugs == 2):
        return '#'
    return c

def calc(g, _max):
    sc = 0
    fac = 1
    for y in range(0, _max[1]):
        for x in range(0, _max[0]):
            if g[(x,y)] == '#':
                sc += fac
            fac *= 2
    return sc


with open('24.txt') as f:

    grid = defaultdict(lambda:'.')
    y = 0
    for line in f.readlines():
        for x in range(0, len(line) - 1):
            if line[x] == '#' or line[x] == '.':
                grid[(x,y)] = line[x]
        y += 1
    _max = (x + 1,y)
    print(_max)
    printg(grid, _max)

    seen = set()

    for r in range(1,10000):
        ngrid = grid.copy()
        for y in range(0, _max[1]):
            for x in range(0, _max[0]):
                ngrid[(x,y)] = nextround(grid, x, y, _max)
        nsc = calc(ngrid, _max)
        print(r, nsc)
        if nsc in seen:
            printg(ngrid, _max)
            print('score', nsc)
            break
        seen.add(nsc)
        grid = ngrid


