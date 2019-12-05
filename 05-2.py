import re
import sys
import json
from collections import defaultdict
sys.setrecursionlimit(5000)

def readv(ops, p, offs):
    if offs == 1: mode = 'IMM' if ((ops[p] % 1000) // 100) == 1 else 'POS'
    elif offs == 2: mode = 'IMM' if ((ops[p] % 10000) // 1000) == 1 else 'POS'
    elif offs == 3: mode = 'IMM' if ((ops[p] % 100000) // 10000) == 1 else 'POS'
    #print('r', p, mode, ops[p], ops[p + offs])
    return ops[p + offs] if mode == 'IMM' else ops[ops[p + offs]]

with open('05.txt') as f:
    oops = [int(x) for x in f.readline().split(',')]

    output = False

    p = 0
    ops = oops.copy()
    inp = [5]
    ip = 0

    ops_size = {1:4, 2:4, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 99:0}
    while True:
        opcode = ops[p] % 100
        inc_p = True
        if opcode == 1:
            v1 = readv(ops, p, 1)
            v2 = readv(ops, p, 2)
            ops[ops[p+3]] = v1 + v2
            if output: print('add', v1, v2, ops[p+3])
            pass
        elif opcode == 2:
            v1 = readv(ops, p, 1)
            v2 = readv(ops, p, 2)
            ops[ops[p+3]] = v1 * v2
            if output: print('mul', v1, v2, ops[p+3])
            pass
        elif opcode == 3:
            v = inp[ip]
            ip += 1
            ops[ops[p+1]] = v
            if output: print('inp', ops[p+1], v)
            pass
        elif opcode == 4:
            print('output:', readv(ops, p, 1))
            pass
        elif opcode == 5:
            v1 = readv(ops, p, 1)
            if v1 != 0:
                p = readv(ops, p, 2)
                if output: print('jumpnz', p)
                inc_p = False
            else:
                if output: print('nojumpnz', v1)
            pass
        elif opcode == 6:
            if readv(ops, p, 1) == 0:
                p = readv(ops, p, 2)
                if output: print('jumpz', p)
                inc_p = False
            else:
                if output: print('nojumpz')
            pass
        elif opcode == 7:
            v1 = readv(ops, p, 1)
            v2 = readv(ops, p, 2)
            ops[ops[p+3]] = 1 if v1 < v2 else 0
            if output: print('lt', v1, v2, ops[p+3])
            pass
        elif opcode == 8:
            v1 = readv(ops, p, 1)
            v2 = readv(ops, p, 2)
            ops[ops[p+3]] = 1 if v1 == v2 else 0
            if output: print('eq', v1, v2, ops[p+3])
            pass
        elif opcode == 99:
            if output: print('HALT')
            break

        if inc_p:
            p += ops_size[opcode]
