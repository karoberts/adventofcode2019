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

def run_prog(amp):
    ops = amp['o']
    ops_size = {1:4, 2:4, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 99:0}
    outp = []
    output = False
    p = amp['p']
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
            v = amp['i'][amp['pi']]
            amp['pi'] += 1
            ops[ops[p+1]] = v
            if output: print('inp', ops[p+1], v)
            pass
        elif opcode == 4:
            v1 = readv(ops, p, 1)
            #print('output:', v1)
            amp['p'] = p + ops_size[opcode]
            return v1
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

    return None

with open('07.txt') as f:
    oops = [int(x) for x in f.readline().split(',')]
    #oops = [int(x) for x in '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'.split(',')]

    max_sig = 0
    for order in itertools.permutations([5,6,7,8,9], 5):
        print(order)
        amps = []
        for i in order:
            amps.append({'o':oops.copy(), 'p': 0, 'pi':0, 'i':[i]})

        sig = 0
        final_sig = 0
        done = False
        while not done:
            #print('feedback', sig)
            #input("Press Enter to continue...")
            halted = 0
            for a in amps:
                #print('run', a['i'], sig, a['p'], a['o'])
                a['i'].append(sig)
                o = run_prog(a)
                if o is None:
                    #print('halted')
                    halted += 1
                    continue
                sig = o
                final_sig = sig
                #if j == 4: final_sig = sig
            if halted == 5:
                break

        #print('final_sig', sig)
        if sig > max_sig:
            print('max', sig)
            max_sig = sig
    
    print(max_sig)


