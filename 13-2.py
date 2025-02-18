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
            #print('inp', ops[ctx['p']+1], v, ctx['pi'], len(inp))
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
    initops = ops.copy()

    inp = []
    ctx =  {'p': 0, 'pi':0, 'rb':0}

    ball = None
    paddle = None
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
        if t == 4: ball = (x,y)
        if t == 3: paddle = [x,y]
        if x > _max[0]: _max[0] = x
        if y > _max[1]: _max[1] = y
        if x < _min[0]: _min[0] = x
        if y < _min[1]: _min[1] = y

    def print_board():
        tiles = {0:' ', 1:'W', 2:'B', 3:'P', 4:'b'}
        print(_max, _min)
        for y in range(_min[1], _max[1] + 1):
            for x in range(_min[0], _max[0] + 1):
                print(tiles[grid[(x,y)]], end='')
            print()
        print()

    print_board()

    ops = initops.copy()
    ops[0] = 2
    inp = []
    score = None

    print('ball', ball)
    print('paddle', paddle)

    oldblocks = 0
    oldscore = 0
    for i in range(0, 200):
        ctx =  {'p': 0, 'pi':0, 'rb':0}
        blocks = 0
        print('starting run')
        seen = 0
        while True:
            x = run_prog(ops, ctx, inp)
            if x is None: 
                break
            y = run_prog(ops, ctx, inp)
            t = run_prog(ops, ctx, inp)

#            if t not in [0,1,2]:
#                print('got',x,y,t)

            if x == -1 and y == 0:
                if t > 0 and t != oldscore:
                    #print('new score', t)
                    oldscore = t
                score = t
                if blocks == 0:
                    break
                continue

            grid[(x,y)] = t
            if t == 4: 
                ball = (x,y)
                #print(' ball now', ball)
            if t == 3:
                paddle = [x,y]
                #print(' padl now', (x,y))

            if t == 2: 
                blocks += 1

            if t == 4:
                if paddle[0] == ball[0]: 
                    inp.append(0)
                elif paddle[0] < ball[0]:
                    inp.append(1)
                    #paddle[0] += 1
                else: 
                    inp.append(-1)
                    #paddle[0] -= 1
                #print(' => inp =', inp[-1])

            #print('ball', ball, 'paddle', paddle)
            #print_board()
        break

        #print_board()
        if blocks == 0:
            break

    print('part2', score)

