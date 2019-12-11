import re
import sys
import json
import itertools
import math
from collections import defaultdict
sys.setrecursionlimit(5000)


# Utility function to find GCD 
# of two numbers GCD of a and b 
gcd_memo = {}
def gcd(a, b): 
    if (a,b) in gcd_memo:
        return gcd_memo[(a,b)]
    if b == 0: 
        return a 
    r = gcd(b, a % b) 
    gcd_memo[(a,b)] = r
    return r
  
# method prints integer point on a line with two points U and V. 
def get_int_pt(u, v):
    # Getting coefficient of line 
    A = v[1] - u[1]; 
    B = v[0] - u[0]; 

    g = gcd(abs(A), abs(B))
    #print('A,B,g', A, B, g, A // g, B // g)
    return (A // g, B // g)

# Finds the no. of Integral points 
# between two given points. 
def getCount(p, q): 
  
    # If line joining p and q is parallel  
    # to x axis, then count is difference 
    # of y values 
    if p[0] == q[0]: 
        return abs(p[1] - q[1]) - 1
  
    # If line joining p and q is parallel  
    # to y axis, then count is difference  
    # of x values 
    if p[1] == q[1]: 
        return abs(p[0] - q[0]) - 1
  
    return gcd(abs(p[0] - q[0]),  
               abs(p[1] - q[1])) - 1

def read(fn):
    d = {}
    with open(fn) as f:
        y = 0
        for line in f.readlines():
            x = 0
            for c in line.strip():
                if c == '#':
                    d[(x,y)] = True
                x += 1
            y += 1
    return (d, x, y)

p = read('10-test3.txt')

b = p[0]
w = p[1]
h = p[2]

# m = (y2 - y1) / (x2 - x1)
# y = mx + b
# b = y - mx

# https://math.stackexchange.com/questions/497327/find-point-on-line-that-has-integer-coordinates
# (sn(x) + sn(x1)

seen = defaultdict(set)
notseen = defaultdict(set)

for kc in b.keys():
    #print('candidate', kc)
    for kt in b.keys():
        if kc == kt:
            continue
        if kc in seen[kt] or kt in seen[kc] or kc in notseen[kt] or kt in notseen[kc]:
            continue

        np = getCount(kc, kt)
        if np == 0:
            #print('  target seen [1]', kt)
            seen[kc].add(kt)
            seen[kt].add(kc)
            continue

        fp = get_int_pt(kc, kt)

        #print(' -target', kt, np, fp)
        
        src = kc
        tgt = kt

        xr = src[0] + fp[1]
        yr = src[1] + fp[0]
        found = False
        i = 0
        while True:
            i += 1
            if i > 50: exit()
            #print('  checking', (xr,yr))
            if (xr,yr) in b:
                if found:
                    #print('  seen')
                    seen[src].add((xr,yr))
                    seen[(xr,yr)].add(src)
                    found = True
                    break
                else: 
                    #print('  not seen')
                    notseen[src].add((xr,yr))
                    notseen[(xr,yr)].add(src)
                    found = True
                    break
            else:
                #print('  empty')
                pass
            found = True
            xr += fp[1]
            yr += fp[0]
            if (xr, yr) == tgt:
                #print('  target seen [2]', kt)
                seen[src].add(tgt)
                seen[tgt].add(src)
                break

            #input('ipause')

        #input('pause')
        #print()


#print(seen)
#for pt in seen:
    #print(pt, len(seen[pt]))

print()
max_f = 0
max_pt = None
for y in range(0,h):
    for x in range(0,w):
        if (x,y) in seen:
            l = len(seen[(x,y)])
            if l > max_f:
                max_f = l
                max_pt = (x,y)
            #print(l, end='')
        else:
            #print('.', end='')
            pass
    #print()

print('best', max_pt)
seen.pop(max_pt)
#print('seen', seen[max_pt])

# 1st quad: -pi/2 to 0
# 2nd quad: 0 to pi/2
# 3rd quad: 

pts = {}
for pt in seen:
    if max_pt[0] == pt[0]: 
        print('vert', pt)
        continue
    if max_pt[1] == pt[1]: 
        print('horiz', pt)
        continue

    fp = get_int_pt(max_pt, pt)
    #print(pt, fp, math.atan2(fp[0], fp[1]))
    pts[pt] = math.atan2(fp[0], fp[1])