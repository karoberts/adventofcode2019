import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

def readv(ops, p, offs):
    if offs == 1: mode = 'IMM' if ((ops[p] % 1000) // 100) == 1 else 'POS'
    elif offs == 2: mode = 'IMM' if ((ops[p] % 10000) // 1000) == 1 else 'POS'
    elif offs == 3: mode = 'IMM' if ((ops[p] % 100000) // 10000) == 1 else 'POS'
    #print('r', p, mode, ops[p], ops[p + offs])
    return ops[p + offs] if mode == 'IMM' else ops[ops[p + offs]]

def run_prog(ops, inp):
    ops_size = {1:4, 2:4, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 99:0}
    outp = []
    output = False
    p_in = 0
    p = 0
    ip = 0
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
            v = inp[p_in]
            p_in += 1
            ip += 1
            ops[ops[p+1]] = v
            if output: print('inp', ops[p+1], v)
            pass
        elif opcode == 4:
            v1 = readv(ops, p, 1)
            print('output:', v1)
            outp.append(v1)
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

    return outp

with open('07.txt') as f:
    oops = [int(x) for x in f.readline().split(',')]
    #oops = [int(x) for x in '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'.split(',')]

    max_sig = 0
    for i in itertools.permutations([0,1,2,3,4], 5):
        sig = 0
        print(i)
        for j in range(0,5):
            o = run_prog(oops.copy(), [i[j], sig])
            sig = o[0]
        print('sig', sig)
        if sig > max_sig:
            max_sig = sig
    print(max_sig)


