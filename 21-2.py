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

def ascii2cmd(s:str) -> list:
    return [ord(c) for c in s] + [10]

# jumps move forward 4 spaces
"""

 ABCDEFGHI

NOJUMP
 ABCDEFGHI
@####.#.#.##.####
@####.##..#.#####
@####..#.###..###
@####..###.#..###

JUMP
 ABCDEFGHI
@##.#...#.#.###
@##.#.#.##.####
@##.##..#.#####
@#..#.####
@#..#.###..###
@#.##.#.##.###
@##.#..###
 012345678
 ABCDEFGHI

 ##.##...#

 ABCDEFGHI
@---#---#

(D and H AND !(C AND B) )
OR
!(E OR F) AND H // OR G)
OR
!A


"""

def bits_to_bot(b) -> str:
    return ''.join( ('#' if x == 1 else '.' for x in b) )

def play(b, p, act):
    r = None
    if act == 'J':
        p += 4
        if p > 8:
            return True
        if b[p] == '.':
            return False
    elif act == 'R':
        p += 1
        if p > 8:
            return True
        if b[p] == '.':
            return False

    r1 = play(b, p, 'R')
    r2 = play(b, p, 'J')

    return r1 or r2

_mR = []
_mJ = []
_d = []
_e = []
for i in range(0, 2**9):
    bits = [int(x) for x in format(i, '09b')]
    s = bits_to_bot(bits)

    rJ = play(s, -1, 'J')
    rR = play(s, -1, 'R')
    if rJ and not rR: _mJ.append(s)
    elif rR and not rJ: _mR.append(s)
    elif not rJ and not rR: _d.append(s)
    elif rJ and rR: _e.append(s)

print('dead', len(_d))
print('must_jump', len(_mJ))
print('must_run', len(_mR))
print('either', len(_e))

"""
ABCDEFGHI
##.#.#.##

!A
OR
(D AND H)
"""

print('   @   @ ')
print('ABCDEFGHI')
print('012345678')
for s in sorted(_mJ):
    if s[0] == '.': continue
    elif s[3] == '#' and s[7] == '#': continue
    #if s[0] == '#' and s[3] == '#' and s[4] == '.' and s[7] == '#': print('2',s)
    #if s[0] == '#' and s[3] == '#' and s[4] == '#' and s[7] == '#' and s[8] == '.': print('3',s)
    print(s)

for s in _mR:
    if s[0] == '.': print('1',s)
    elif s[3] == '#' and s[7] == '#': print('2',s)

s = '####.#.#.'
r1 = play(s, -1, 'J')
print(r1)

#exit()

"""
!(A and B and C)
and D
and H

"""

with open('21.txt') as f:
    ops = defaultdict(lambda:0)
    i = 0
    for x in f.readline().strip().split(','):
        ops[i] = int(x)
        i += 1

    cmds = [ 
        'OR A T',
        'AND B T',
        'AND C T',
        'NOT T J',
        'AND D J',
        'NOT H T',
        'NOT T T',
        'OR E T',
        'AND T J',
    ]

    cmds += ['RUN']

    inp = []
    ctx =  {'p': 0, 'pi':0, 'rb':0}
    prompt = ''
    while True:
        r = run_prog(ops, ctx, inp)
        prompt += chr(r)
        if prompt == 'Input instructions:':
            break

    inp = [item for cmd in cmds for item in ascii2cmd(cmd)]
    while True:
        r = run_prog(ops, ctx, inp)
        if r is None:
            break
        print(chr(r) if r < 128 else r, end='')

    print()
