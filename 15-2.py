import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

#ctx {'p': 0, 'pi':0, 'rb':0 'i':[i]})
def run_prog(ops, ctx, inp):
    modes = {0: 'POS', 1:'IMM', 2:'REL'}

    def readv(ops, p, offs, rb):
        if offs == 1: mode = modes[(ops[p] % 1000) // 100]
        elif offs == 2: mode = modes[(ops[p] % 10000) // 1000]
        elif offs == 3: mode = modes[(ops[p] % 100000) // 10000]
        #print('r', p, mode, ops[p], ops[p + offs])
        if mode == 'IMM': return ops[p + offs]
        elif mode == 'POS': return ops[ops[p + offs]]
        elif mode == 'REL': return ops[ops[p + offs] + rb]

    def writev(ops, p, offs, rb, v):
        if offs == 1: mode = modes[(ops[p] % 1000) // 100]
        elif offs == 2: mode = modes[(ops[p] % 10000) // 1000]
        elif offs == 3: mode = modes[(ops[p] % 100000) // 10000]
        #print('r', p, mode, ops[p], ops[p + offs])
        if mode == 'POS': ops[ops[p + offs]] = v
        elif mode == 'REL': ops[ops[p + offs] + rb] = v

    ops_size = {1:4, 2:4, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:2, 99:0}
    output = False
    while True:
        opcode = ops[ctx['p']] % 100
        inc_p = True
        if opcode == 1:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            v2 = readv(ops, ctx['p'], 2, ctx['rb'])
            writev(ops, ctx['p'], 3, ctx['rb'], v1 + v2)
            if output: print('add', v1, v2, ops[ctx['p']+3])
            pass
        elif opcode == 2:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            v2 = readv(ops, ctx['p'], 2, ctx['rb'])
            writev(ops, ctx['p'], 3, ctx['rb'], v1 * v2)
            if output: print('mul', v1, v2, ops[ctx['p']+3])
            pass
        elif opcode == 3:
            v = inp[ctx['pi']]
            ctx['pi'] += 1
            writev(ops, ctx['p'], 1, ctx['rb'], v)
            if output: print('inp', ops[ctx['p']+1], v)
            pass
        elif opcode == 4:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            if output: print('output:', v1)
            ctx['p'] += ops_size[opcode]
            return v1
            pass
        elif opcode == 5:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            if v1 != 0:
                ctx['p'] = readv(ops, ctx['p'], 2, ctx['rb'])
                if output: print('jumpnz', ctx['p'])
                inc_p = False
            else:
                if output: print('nojumpnz', v1)
            pass
        elif opcode == 6:
            if readv(ops, ctx['p'], 1, ctx['rb']) == 0:
                ctx['p'] = readv(ops, ctx['p'], 2, ctx['rb'])
                if output: print('jumpz', ctx['p'])
                inc_p = False
            else:
                if output: print('nojumpz')
            pass
        elif opcode == 7:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            v2 = readv(ops, ctx['p'], 2, ctx['rb'])
            writev(ops, ctx['p'], 3, ctx['rb'], 1 if v1 < v2 else 0)
            if output: print('lt', v1, v2, ops[ctx['p']+3])
            pass
        elif opcode == 8:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            v2 = readv(ops, ctx['p'], 2, ctx['rb'])
            writev(ops, ctx['p'], 3, ctx['rb'], 1 if v1 == v2 else 0)
            if output: print('eq', v1, v2, ops[ctx['p']+3])
            pass
        elif opcode == 9:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            ctx['rb'] += v1
            if output: print('relbase', v1)
            pass
        elif opcode == 99:
            if output: print('HALT')
            return None

        if inc_p:
            ctx['p'] += ops_size[opcode]

def printg(g, d, _min, _max, deadends, oxy):
    print('grid', 'd=', d)
    for y in range(_min[1], _max[1] + 1):
        for x in range(_min[0], _max[0] + 1):
            c = (x,y)
            if c == (0,0):
                print('S', end='')
            elif c == oxy:
                print('!', end='')
            elif c == d:
                print('D', end='')
            elif c in deadends:
                print('-', end='')
            elif c in g:
                print(g[c], end='')
            else:
                print(' ', end='')
        print()
    print()

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

HITWALL = 0
MOVED = 1
ATOXY = 2

dirname = {NORTH:'NORTH',SOUTH:'SOUTH',WEST:'WEST',EAST:'EAST'}
retname = {HITWALL:'WALL',MOVED:'OPEN',ATOXY:'OXY'}
intended = {NORTH:(0,-1), SOUTH:(0,1), WEST:(-1,0),EAST:(1,0)}
oppo = {NORTH:SOUTH, WEST:EAST, EAST:WEST, SOUTH:NORTH}
nextdir = {NORTH:WEST, WEST:SOUTH, SOUTH:EAST, EAST:NORTH}

def _next(d, dir):
    n = intended[dir]
    return (d[0] + n[0], d[1] + n[1])

def done():
    printg(grid, d, _min, _max, deadends, oxy)
    exit()

with open('15.txt') as f:
    ops = defaultdict(lambda:0)
    i = 0
    for x in f.readline().strip().split(','):
        ops[i] = int(x)
        i += 1

    dir = NORTH
    inp = [dir]
    ctx =  {'p': 0, 'pi':0, 'rb':0}

    blocks = 0
    grid = defaultdict(lambda:' ')
    deadends = set()
    _min = [0,0]
    _max = [0,0]
    d = (0,0)
    oxy = None
    grid[d] = '.'
    for i in range(0, 50000):
        r = run_prog(ops, ctx, inp)
        #print('D', d)
        #print('GOING', dirname[dir], 'ret', retname[r])

        n = intended[dir]
        nsp = (d[0] + n[0], d[1] + n[1])
        if r == HITWALL:
            grid[nsp] = '#'
            ndir = dir
            walls = set()
            for i in range(0, 8):
                ndir = nextdir[ndir]
                g = grid[_next(d,ndir)]
                #print('  trying', dirname[ndir], 'found', g, 'i=', i)
                if g == '#':
                    walls.add(ndir)
                if g == ' ':
                    break
                if g == '.' and i > 3:
                    break
                #print('    continue')
            if len(walls) == 3:
                #print('dead end at', d)
                deadends.add(d)
                grid[d] = '#'
            #print('chose', dirname[ndir])
            dir = ndir
            inp.append(dir)
        elif r == MOVED or r == ATOXY:
            d = nsp
            if r == ATOXY:
                oxy = nsp
            grid[d] = '.'
            g = grid[_next(d,dir)]
            if g == '.' or g == '#':
                #print('next is known')
                ndir = dir
                for i in range(0, 3):
                    ndir = nextdir[ndir]
                    g = grid[_next(d,ndir)]
                    #print('  trying', dirname[ndir], 'found', g, 'i=', i)
                    if g == ' ':
                        break
                    if g == '.' and i > 3:
                        break
                    #print('    continue')
                #print('chose', dirname[ndir])
                dir = ndir
            else:
                # find what is around
                for i in range(1,4+1):
                    g = grid[_next(d,i)]
                    if g == ' ':
                        #print('=> looking', dirname[i])
                        inp.append(i)
                        r = run_prog(ops, ctx, inp)
                        #print('=> got', retname[r])
                        if r == HITWALL:
                            grid[_next(d,i)] = '#'
                        elif r == MOVED or r == ATOXY:
                            grid[_next(d,i)] = '.'
                            if r == ATOXY:
                                oxy = _next(d,i)
                            inp.append(oppo[i])
                            r = run_prog(ops, ctx, inp)
                        elif r == ATOXY:
                            oxy = _next(d,i)
                            #print('oxygen', oxy)
                            done()
            inp.append(dir)
        """
        elif r == ATOXY:
            oxy = nsp
            print('oxygen', nsp)
            break
        """

        if nsp[0] < _min[0]: _min[0] = nsp[0]
        if nsp[1] < _min[1]: _min[1] = nsp[1]
        if nsp[0] > _max[0]: _max[0] = nsp[0]
        if nsp[1] > _max[1]: _max[1] = nsp[1]

        #printg(grid, d, _min, _max, deadends, oxy)
        #input('next')

    done()
