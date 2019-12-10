import re
import sys
import json
import itertools
from collections import defaultdict
sys.setrecursionlimit(5000)

# https://www.geeksforgeeks.org/find-integer-point-line-segment-given-two-ends/
def gcdExtended(a, b, xy):
    # Base Case 
    if a == 0:
        xy[0] = 0; 
        xy[1] = 1; 
        return b; 
  
    xy1 = [0, 0]
    gcd = gcdExtended(b%a, a, xy1); 
  
    # Update x and y using results of recursive call 
    xy[0] = xy1[1] - (b//a) * xy1[0]; 
    xy[1] = xy1[0]; 
  
    return gcd; 
  
# method prints integer point on a line with two points U and V. 
def printIntegerPoint(pointU, pointV):
    # Getting coefficient of line 
    A = (pointU[1] - pointV[1]); 
    B = (pointV[0] - pointU[0]); 
    C = (pointU[0] * (pointU[1] - pointV[1]) + 
         pointU[1] * (pointV[0] - pointU[0])); 
  
    xy = [0,0]  # To be assigned a value by gcdExtended() 
    g = gcdExtended(A, B, xy); 
  
    # if C is not divisible by g, then no solution is available 
    if C % g != 0:
        #print("No possible integer point")
        return None
    else:
        # scaling up x and y to satisfy actual answer 
        #print(xy[0], xy[1], C, g)
        #print("Integer Point : ", (xy[0] * C//g), (xy[1] * C//g))
        return (xy, C, g)

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

p = read('10-test1.txt')

b = p[0]
w = p[1]
h = p[2]

# m = (y2 - y1) / (x2 - x1)
# y = mx + b
# b = y - mx

# https://math.stackexchange.com/questions/497327/find-point-on-line-that-has-integer-coordinates
# (sn(x) + sn(x1)

p1 = (3,4)
p2 = (1,0)
r = printIntegerPoint(p1, p2)
xy = r[0]
xm = xy[0] * r[1]//r[2]
ym = xy[1] * r[1]//r[2]
print(r)
print(xm, ym)
xm = xy[0] * r[1]//r[2]
ym = xy[1] * r[1]//r[2]
print(xm, ym)
exit()

tot = {}

for kc in b.keys():
    ct = 0
    for kt in b.keys():
        if kc == kt:
            continue
        r = printIntegerPoint(kc, kt)
        if r is None:
            ct += 1
        else:
            xy = r[0]
            xm = xy[0] * r[1]//r[2]
            ym = xy[1] * r[1]//r[2]
            if (xm, ym) not in b:
                ct += 1
    print('candidate', kc, ct)
    tot[kc] = ct

print(tot)
    


