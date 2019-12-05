import re
import sys
import json
from collections import defaultdict
sys.setrecursionlimit(5000)

def readv(ops, p, offs):
    if offs == 1: mode = 'IMM' if ((ops[p] % 1000) // 100) == 1 else 'POS'
    elif offs == 2: mode = 'IMM' if ((ops[p] % 10000) // 1000) == 1 else 'POS'
    #print('r', p, mode, ops[p], ops[p + offs])
    return ops[p + offs] if mode == 'IMM' else ops[ops[p + offs]]

with open('05.txt') as f:
    oops = [int(x) for x in f.readline().split(',')]

    p = 0
    ops = oops.copy()
    inp = [1]
    ip = 0

    while True:
        opcode = ops[p] % 100
        #print('p', p, opcode, ops[p])
        if opcode == 1:
            ops[ops[p+3]] = readv(ops, p, 1) + readv(ops, p, 2)
            p += 4
            pass
        elif opcode == 2:
            ops[ops[p+3]] = readv(ops, p, 1) * readv(ops, p, 2)
            p += 4
            pass
        elif opcode == 3:
            v = inp[ip]
            ip += 1
            ops[ops[p+1]] = v
            p += 2
            pass
        elif opcode == 4:
            print('output:', readv(ops, p, 1))
            p += 2
            pass
        elif opcode == 99:
            break
