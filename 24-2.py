import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

def printg(g, _max, min_lev, max_lev):
    rmin = 0
    rmax = 0
    for lev in range(min_lev, max_lev + 1):
        nbugs = 0
        for y in range(0, 5):
            for x in range(0, 5):
                if grid[(lev, x, y)] == '#':
                    nbugs += 1
        if nbugs > 0:
            if lev < rmin: rmin = lev
            if lev > rmax: rmax = lev

    for lev in range(rmin, rmax + 1):
        print('Depth', lev)
        for y in range(0, 5):
            for x in range(0, 5):
                c = (lev,x,y)
                if x == 2 and y == 2:
                    print('?', end='')
                elif c in g:
                    print(g[c], end='')
                else:
                    print(' ', end='')
            print()
        print()

def make_map():
    def reg(x,y):
        tests = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]
        m = []
        for t in tests:
            tx = x + t[0]
            ty = y + t[1]
            if tx < 0 or ty < 0 or tx >= 5 or ty >= 5 or (tx == 2 and ty == 2):
                continue
            m.append( (0, (tx, ty)) )
        return m

    def others(x, y): 
        m = []
        if x == 0: m.append( (-1, (1,2)) )
        if y == 0: m.append( (-1, (2,1)) )
        if x == 4: m.append( (-1, (3,2)) )
        if y == 4: m.append( (-1, (2,3)) )

        if x == 1 and y == 2:
            for i in range(0, 5):
                m.append( (1, (0, i)) )
        if x == 3 and y == 2:
            for i in range(0, 5):
                m.append( (1, (4, i)) )
        if x == 2 and y == 1:
            for i in range(0, 5):
                m.append( (1, (i, 0)) )
        if x == 2 and y == 3:
            for i in range(0, 5):
                m.append( (1, (i, 4)) )
        return m

    mapping = dict()
    for y in range(0, 5):
        for x in range(0, 5):
            mapping[(x,y)] = reg(x,y) + others(x,y)
    return mapping


def nextround(grid, lev, x, y, _max, mapping):
    k = (lev,x,y)
    tests = mapping[(x,y)]
    c = grid[k]

    nbugs = 0
    for t in tests:
        tx = t[1][0]
        ty = t[1][1]
        tk = (lev + t[0], tx, ty)
        tt = grid[tk]
        #if lev == 1 and x == 4 and y == 1:
        #    print('checking', t, tk, tt)
        if tt == '#':
            nbugs += 1

    if c == '#':
        if nbugs != 1:
            c = '.'
    elif c == '.' and (nbugs == 1 or nbugs == 2):
        c = '#'

    #print('=>', 'l',lev, (x, y), 'nb', nbugs, '=>', c)

    return c

with open('24.txt') as f:

    mapping = make_map()
    #print(mapping[(2,3)])
    #exit()

    grid = defaultdict(lambda:'.')
    min_lev = -5 
    max_lev = 5
    y = 0
    for line in f.readlines():
        for x in range(0, len(line) - 1):
            if line[x] == '#' or line[x] == '.':
                grid[(0,x,y)] = line[x]
        y += 1
    _max = (x + 1,y)
    print(_max)
    printg(grid, _max, min_lev, max_lev)

    for r in range(0,200):
        ngrid = grid.copy()
        for lev in range(min_lev - 1, max_lev + 2):
            for y in range(0, _max[1]):
                for x in range(0, _max[0]):
                    if x == 2 and y == 2: continue
                    r = nextround(grid, lev, x, y, _max, mapping)
                    #print('n', x, y, r, min_lev, max_lev)
                    ngrid[(lev,x,y)] = r
        grid = ngrid
        min_lev -= 1
        max_lev += 1

    printg(grid, _max, min_lev, max_lev)

    s = 0
    for k, v in grid.items():
        if v == '#':
            s += 1
    print('bugs:', s) 
        


