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
    while p < len(pix):
        layer = []
        for i in range(0, scan):
            layer.append(pix[p + i])
        layers.append(layer)
        p += scan

    img = defaultdict(lambda:2)

    for layer in layers:
        for y in range(0, h):
            for x in range(0, w):
                p = layer[x + y * w]
                cur = img[(x,y)]
                if cur == 2: img[(x,y)] = p

    pixels = {0: ' ', 1: '*'}
    for y in range(0, h):
        for x in range(0, w):
            print(pixels[img[(x,y)]], end='')
        print()


