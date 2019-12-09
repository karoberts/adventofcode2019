import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

def run_prog(ops, inp):
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
    outp = []
    output = False
    p_in = 0
    p = 0
    ip = 0
    rb = 0
    while True:
        opcode = ops[p] % 100
        inc_p = True
        if opcode == 1:
            v1 = readv(ops, p, 1, rb)
            v2 = readv(ops, p, 2, rb)
            writev(ops, p, 3, rb, v1 + v2)
            if output: print('add', v1, v2, ops[p+3])
            pass
        elif opcode == 2:
            v1 = readv(ops, p, 1, rb)
            v2 = readv(ops, p, 2, rb)
            writev(ops, p, 3, rb, v1 * v2)
            if output: print('mul', v1, v2, ops[p+3])
            pass
        elif opcode == 3:
            v = inp[p_in]
            p_in += 1
            ip += 1
            writev(ops, p, 1, rb, v)
            if output: print('inp', ops[p+1], v)
            pass
        elif opcode == 4:
            v1 = readv(ops, p, 1, rb)
            if output: print('output:', v1)
            outp.append(v1)
            pass
        elif opcode == 5:
            v1 = readv(ops, p, 1, rb)
            if v1 != 0:
                p = readv(ops, p, 2, rb)
                if output: print('jumpnz', p)
                inc_p = False
            else:
                if output: print('nojumpnz', v1)
            pass
        elif opcode == 6:
            if readv(ops, p, 1, rb) == 0:
                p = readv(ops, p, 2, rb)
                if output: print('jumpz', p)
                inc_p = False
            else:
                if output: print('nojumpz')
            pass
        elif opcode == 7:
            v1 = readv(ops, p, 1, rb)
            v2 = readv(ops, p, 2, rb)
            writev(ops, p, 3, rb, 1 if v1 < v2 else 0)
            if output: print('lt', v1, v2, ops[p+3])
            pass
        elif opcode == 8:
            v1 = readv(ops, p, 1, rb)
            v2 = readv(ops, p, 2, rb)
            writev(ops, p, 3, rb, 1 if v1 == v2 else 0)
            if output: print('eq', v1, v2, ops[p+3])
            pass
        elif opcode == 9:
            v1 = readv(ops, p, 1, rb)
            rb += v1
            if output: print('relbase', v1)
            pass
        elif opcode == 99:
            if output: print('HALT')
            break

        if inc_p:
            p += ops_size[opcode]

    return outp

with open('09.txt') as f:
    ops = defaultdict(lambda:0)
    i = 0
    for x in f.readline().strip().split(','):
        ops[i] = int(x)
        i += 1

    o = run_prog(ops.copy(), [1])
    print('part1', o)

    o = run_prog(ops.copy(), [2])
    print('part2', o)
