import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

def deal(stack):
    return list(reversed(stack))

def cut(stack, i):
    if i > 0:
        return stack[i:] + stack[0:i]
    else:
        return stack[len(stack) + i:] + stack[0:len(stack) + i]
    
def incr(stack, i):
    newstack = stack.copy()
    p = 0
    for s in range(0, len(stack)):
        newstack[p] = stack[s]
        p += i
        if p >= len(stack):
            p -= len(stack)
    return newstack


with open('22.txt') as f:
    ops = []
    for x in (l.strip() for l in f.readlines()):
        if x == 'deal into new stack':
            ops.append(('DEAL', 0))
        elif x.startswith('deal with increment'):
            ops.append(('INCR', int(x[len('deal with increment '):])))
        else:
            ops.append(('CUT', int(x[len('cut '):])))

    stack = [x for x in range(0, 10007)]
    #stack = [x for x in range(0, 10)]

    for op in ops:
        print(op, len(stack))
        if op[0] == 'DEAL':
            stack = deal(stack)
        elif op[0] == 'CUT':
            stack = cut(stack, op[1])
        else:
            stack = incr(stack, op[1])

    print(len(stack))
    #print(stack)

    print(stack.index(2019))

# 8588 too high
