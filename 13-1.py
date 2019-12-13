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

with open('13.txt') as f:
    ops = defaultdict(lambda:0)
    i = 0
    for x in f.readline().strip().split(','):
        ops[i] = int(x)
        i += 1

    inp = [1]
    ctx =  {'p': 0, 'pi':0, 'rb':0}

    blocks = 0
    grid = defaultdict(lambda:0)
    _min = [0,0]
    _max = [0,0]
    while True:
        x = run_prog(ops, ctx, inp)
        if x is None: 
            break
        y = run_prog(ops, ctx, inp)
        t = run_prog(ops, ctx, inp)

        grid[(x,y)] = t
        if t == 2:
            blocks += 1

    print('part1', blocks)
