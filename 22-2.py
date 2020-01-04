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
    
# modpow the polynomial: (ax+b)^m % n
# f(x) = ax+b
# g(x) = cx+d
# f^2(x) = a(ax+b)+b = aax + ab+b
# f(g(x)) = a(cx+d)+b = acx + ad+b
def polypow(a,b,m,n):
    if m==0:
        return 1,0
    if m%2==0:
        return polypow(a*a%n, (a*b+b)%n, m//2, n)
    else:
        c,d = polypow(a,b,m-1,n)
        return a*c%n, (a*d+b)%n

tot = 101741582076661
lenstack = 119315717514047
card = 2020

with open('22.txt') as f:
    ops = [l.strip() for l in f.readlines()]

    #https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
    # modinv(x, p)
    # y = pow(x, p-2, p)

    a = 1
    b = 0
    for x in reversed(ops):
        if x == 'deal into new stack':
            #print('deal();')
            #ops.append(('DEAL', 0))
            a = -a
            b = lenstack - b - 1
        elif x.startswith('deal with increment'):
            #print('incr({});'.format(int(x[len('deal with increment '):])))
            #ops.append(('INCR', int(x[len('deal with increment '):])))
            i = int(x[len('deal with increment '):])
            z = pow(i, lenstack - 2, lenstack)
            a = (a*z) % lenstack
            b = (b*z) % lenstack
        else:
            #print('cut({});'.format(int(x[len('cut '):])))
            #ops.append(('CUT', int(x[len('cut '):])))
            c = int(x[len('cut '):])
            b = (b+c) % lenstack

    print(a,b)
    #print( pow(a*2020 + b, 2, lenstack) )
    a,b = polypow(a,b, tot, lenstack)

    print('ans=', (card*a+b)%lenstack)

    lenstack = 10007
    a = 1
    b = 0
    for x in reversed(ops):
        if x == 'deal into new stack':
            #print('deal();')
            #ops.append(('DEAL', 0))
            a = -a
            b = lenstack - b - 1
        elif x.startswith('deal with increment'):
            #print('incr({});'.format(int(x[len('deal with increment '):])))
            #ops.append(('INCR', int(x[len('deal with increment '):])))
            i = int(x[len('deal with increment '):])
            z = pow(i, lenstack - 2, lenstack)
            a = (a*z) % lenstack
            b = (b*z) % lenstack
        else:
            #print('cut({});'.format(int(x[len('cut '):])))
            #ops.append(('CUT', int(x[len('cut '):])))
            c = int(x[len('cut '):])
            b = (b+c) % lenstack
    print((a*2019+b) % lenstack)
    a,b = polypow(a,b, 1, 10007)
    print(a,b)
    print('p1=', (1538*a+b)%lenstack)

    exit()

    for c in range(0, 3):
        print('calc', card)
        for op in ops:
            if op[0] == 'DEAL':
                card = deal_p(card, lenstack)
            elif op[0] == 'CUT':
                card = cut_p(card, op[1], lenstack)
            else:
                card = incr_p(card, op[1], lenstack)

    exit()

    print(card)
