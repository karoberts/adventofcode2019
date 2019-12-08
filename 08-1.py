import re
import sys
import json
from collections import defaultdict
sys.setrecursionlimit(5000)

with open('08.txt') as f:
    pix = [int(x) for x in f.readline().strip()]

    w = 25
    h = 6
    scan = w * h
    p = 0
    layers = []
    min_zcount = 999999999999
    min_layer = None
    while p < len(pix):
        layer = []
        zcount = 0
        for i in range(0, scan):
            layer.append(pix[p + i])
            if pix[p + i] == 0:
                zcount += 1
        if zcount < min_zcount:
            min_zcount = zcount
            min_layer = layer
        p += scan

    print(min_layer)
    n_ones = 0
    n_twos = 0
    for i in min_layer:
        if i == 1: n_ones += 1
        if i == 2: n_twos += 1
    
    print(n_ones, n_twos)
    print(n_ones * n_twos)
            

