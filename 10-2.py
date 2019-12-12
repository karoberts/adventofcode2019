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
    #if kc != (8,3): continue
    #print('candidate', kc)
    for kt in b.keys():
        if kc == kt:
            continue
        if kc in seen[kt] or kt in seen[kc] or kc in notseen[kt] or kt in notseen[kc]:
            continue

        fp = (0,0)
        
        if kc[0] == kt[0]: # vertical
            fp = (1,0) if kc[1] < kt[1] else (-1,0)
        elif kc[1] == kt[1]: # horizontal
            fp = (0,1) if kc[0] < kt[0] else (0,-1)
        else:
            np = getCount(kc, kt)
            if np == 0: # no integer points between
                seen[kc].add(kt)
                seen[kt].add(kc)
                #print('  target seen [1]', kt, seen[kc])
                continue
            fp = get_int_pt(kc, kt)

        xr = kc[0] + fp[1]
        yr = kc[1] + fp[0]

        #print(' -target', kt, np, fp)

        i = 0
        while True:
            i += 1
            if i > 50: exit()
            #print('  checking', (xr,yr))
            if (xr,yr) in b:
                #print('  maybe target seen [1]', (xr,yr), kt)
                seen[kc].add((xr,yr))
                seen[(xr,yr)].add(kc)
                if (xr,yr) != kt:
                    #print('  in the way', (xr,yr), kt)
                    notseen[kc].add(kt)
                    notseen[kt].add(kc)
                break
            xr += fp[1]
            yr += fp[0]
            if (xr, yr) == kt:
                #print('  target seen [2]', kt)
                seen[kc].add(kt)
                seen[kt].add(kc)
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

print('best', max_pt, len(seen[max_pt]))
#print('seen', seen[max_pt])

# 1st quad: -pi/2 to 0
# 2nd quad: 0 to pi/2
# 3rd quad: 

print()
for pt in notseen[max_pt]:
    print(pt)
print()

pts = {}
for pt in seen[max_pt]:
    if max_pt[0] == pt[0]: 
        pts[pt] = -math.pi/2 if pt[1] > max_pt[1] else math.pi/2
        #print(pt, 'vert')
        continue
    if max_pt[1] == pt[1]: 
        pts[pt] = 0 if pt[0] > max_pt[0] else -math.pi
        #print(pt, 'horiz')
        continue

    fp = get_int_pt(max_pt, pt)

    rise = -fp[0]
    run = fp[1]
    angle = math.atan(rise/run)

    #print(pt, fp, angle)
    pts[pt] = angle

pts = {k: v for k, v in sorted(pts.items(), key=lambda x:-x[1])}

for pt in pts:
    print(pt, pts[pt])