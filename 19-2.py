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

def printg(g, _min, _max):
    print('grid')
    for y in range(_min[1], _max[1] + 1):
        for x in range(_min[0], _max[0] + 1):
            c = (x,y)
            if c in g:
                print(g[c], end='')
            else:
                print(' ', end='')
        print()
    print()

with open('19.txt') as f:
    ops = defaultdict(lambda:0)
    i = 0
    for x in f.readline().strip().split(','):
        ops[i] = int(x)
        i += 1

    _min = [0,0]
    _max = [1600,1600]

    x_start = dict()
    x_stop = dict()
    y_start = dict()
    y_stop = dict()

    grid = defaultdict(lambda:' ')
    deadends = set()
    for y in range(_min[1], _max[1]):
        xst = x_start[y-1] if (y-1) in x_start else 0
        for x in range(xst, _max[0]):
            inp = [x,y]
            ctx =  {'p': 0, 'pi':0, 'rb':0}
            r = run_prog(ops.copy(), ctx, inp)
            #print(x,y,r)
            if r == 0:
                grid[(x,y)] = '.'
                if y in x_start:
                    break
            elif r == 1:
                grid[(x,y)] = '#'
                if x not in y_start:
                    y_start[x] = y
                if y not in x_start:
                    x_start[y] = x
                y_stop[x] = y
                x_stop[y] = x
                """
                if x - x_start[y] == 100:
                    grid[(x_start[y],y)] = 'O'
                    grid[(x-1,y)] = 'Z'
                    if y - y_start[x-1] == 100:
                        grid[(x-1, y_start[x-1])] = '!'
                        grid[(x_start[y], y_start[x-1])] = 'A'
                        print('found', (x-1,y), (x-1,y_start[x-1]), 'answer?', (x_start[y], y_start[x-1]), (x_start[y] * 10000 + y_start[x-1]), file=sys.stderr)
                """
        if y > 400:
            low_startx = x_start[y]
            low_endx = x_stop[y]
            high_startx = low_startx
            high_starty = y - 99
            high_endx = x_stop[y - 99]
            if low_endx - low_startx >= 99 and high_endx - high_startx >= 99:
                print(low_startx, low_endx, high_startx, high_starty, high_endx, 'answer', high_startx, high_starty, high_startx * 10000 + high_starty)
                exit()

    """
    stops = []
    for k, v in x_stop.items():
        y = k
        ys = x_start[y]
        x = v
        s = (x, y, v - x_start[y], y_stop[x] - y_start[x])
        stops.append(s)
        if s[2] >= 5 and s[3] >= 5:
            xs = x_start[ys]
            ys = y_start[xs]
            grid[(xs, ys)] = 'O'
            print(s, xs, ys)
    """

    #printg(grid, _min, _max)

"""
    for y in range(_min[1], _max[1]):
        if y in x_start and x_stop[y] - x_start[y] >= 5:
            for x in range(x_start[y], x_stop[y]):
                if x in y_start and y_stop[x] - y_start[x] >= 5:
                    grid[(x,y)] = 'O'
                    """

