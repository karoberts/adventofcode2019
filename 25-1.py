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
            #print('less', v1, v2)
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

"""

- se: space heater
- s: photons  (death)
- sw: shell
- wn: jam
- wnn: astronaut ice cream
- wnnne: molten lava
- wnnnen: infinite loop
- wnes: asterisk
- wness: klein bottle
- wnesse: spool of cat6
- wnese: giant electomagnet
- wnnnes: space law space brochure

# determined by printout out less commands when going south from checkpoint
astronaut ice cream = 2097152
jam = 262144
shell = 16384
space heater = 8192
klein bottle = 32
spool of cat6 = 4
space law space brochure = 2
asterisk = 1

ice cream    heater    bottle    spool    law    asterisk                
2097152        8192                                         2105344    
2097152        8192    32                                   2105376    
2097152        8192    32                           1       2105377    answer!
2097152        8192    32                  2                2105378    too heavy
2097152        8192    32          4                        2105380    too heavy
2097152    16384                                            2113536    too heavy


"""

map = dict()
items = defaultdict(set)
oppo = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
chain = []

with open('25.txt') as f:
    ops = defaultdict(lambda:0)
    i = 0
    for x in f.readline().strip().split(','):
        ops[i] = int(x)
        i += 1

    inp = []
    ctx =  {'p': 0, 'pi':0, 'rb':0}
    prompt = ''
    last_move = None
    while True:
        r = run_prog(ops, ctx, inp)
        print(chr(r), end='')
        if r == 10:
            if len(prompt) > 0:
                if prompt[0] == '=':
                    map[prompt] = ''.join(chain)
                #elif prompt[0] == '-':
                    #items[prompt[2:-2]].add(''.join(chain))
            prompt = ''
        else:
            prompt += chr(r)
        if prompt == 'Command?':
            c = input(' ')
            while True:
                if c == 'c':
                    print('-- cur = ', ''.join(chain))
                elif c == 'm':
                    print('-- map')
                    for m,ch in map.items():
                        print('  ', m, ch)
                elif c == 'i':
                    print('-- items')
                    for m,ch in items.items():
                        print('  ', m, ch)
                else:
                    break
                c = input('Command? ')
            if c == 's': c = 'south'
            elif c == 'e': c = 'east'
            elif c == 'w': c = 'west'
            elif c == 'n': c = 'north'
            inp += [ord(x) for x in c] + [10]
            prompt = ''
            if c[0] in oppo:
                if len(chain) > 0 and chain[-1] in oppo and c[0] == oppo[chain[-1]]:
                    chain.pop()
                else:
                    chain.append(c[0])

    print()
