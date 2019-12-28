import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

def deal(stack):
    return list(reversed(stack))

def deal_p(c, lenstack):
    return lenstack - c - 1

def cut(stack, i):
    if i > 0:
        return stack[i:] + stack[0:i]
    else:
        return stack[len(stack) + i:] + stack[0:len(stack) + i]

def cut_p(c, i, lenstack):
    if i < 0:
        i = lenstack + i
    if c < i:
        return c + (lenstack - i)
    else:
        return c - i
    
def incr(stack, i):
    newstack = stack.copy()
    p = 0
    for s in range(0, len(stack)):
        newstack[p] = stack[s]
        p += i
        if p >= len(stack):
            p -= len(stack)
    return newstack

def incr_p(c, i, lenstack):
    pos = c * i
    mod = pos % lenstack
    return mod

with open('22.txt') as f:
    ops = []

    for x in (l.strip() for l in f.readlines()):
        if x == 'deal into new stack':
            ops.append(('DEAL', 0))
        elif x.startswith('deal with increment'):
            ops.append(('INCR', int(x[len('deal with increment '):])))
        else:
            ops.append(('CUT', int(x[len('cut '):])))

    lenstack = 119315717514047
    card = 2020

    tot = 101741582076661
    for c in range(0, 10000):
        print(card)
        for op in ops:
            #print(op, card)
            if op[0] == 'DEAL':
                card = deal_p(card, lenstack)
            elif op[0] == 'CUT':
                card = cut_p(card, op[1], lenstack)
            else:
                card = incr_p(card, op[1], lenstack)

    print(card)
