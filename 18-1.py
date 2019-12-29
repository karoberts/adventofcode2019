import re
import sys
import heapq
import json
from collections import defaultdict

def printg2(g, _max, me):
    for y in range(0, _max[1] + 1):
        for x in range(0, _max[0] + 1):
            c = (x,y)
            if c == me:
                print('@', end='')
            elif c in g:
                print(g[c], end='')
            else:
                print(' ', end='')
        print()
    print()

def dijkstra(me, grid, _max):
    tests = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]
    def get_neighbors(x,y):
        k = (x,y)
        c = grid[k]
        ns = []

        for t in tests:
            tx = x + t[0]
            ty = y + t[1]
            if tx < 0 or ty < 0 or tx >= _max[0] or ty >= _max[1]:
                continue
            tk = (tx, ty)
            tt = grid[tk]

            if tt == '.':
                ns.append( [1, tx, ty, tk, False] )
            if tt in 'abcdefghijklmnopqrstuvwxyz':
                ns.append( [1, tx, ty, tk, True] )

        for n in ns:
            n.append(True)
        return ns

    dist = defaultdict(lambda :999999999)
    prev = {}

    dist[me] = 0
    prev[me] = None

    finder = {}

    inq = set()
    h = []
    heapq.heappush(h, [0, me[0], me[1], me, True])
    finder[me] = h[0]
    inq.add(me)
    keys = []

    while len(h) > 0:
        #print_map(dist);
        u = heapq.heappop(h)
        if not u[4]:
            continue
        inq.remove(u[3])
        #if u[1] == target_y and u[2] == target_y:
            #return u
        uk = u[3]
        for v in get_neighbors(u[1], u[2]):
            if v[4]:
                #print('found key:', grid[v[3]], 'at', v[3], dist[uk] + v[0], 'steps')
                keys.append((v[3], grid[v[3]], dist[uk] + v[0]))
                continue
            alt = dist[uk] + v[0]
            if alt < dist[v[3]]:
                dist[v[3]] = alt
                prev[v[3]] = (uk, v[0], v[1], v[2])
                entry = [alt, v[1], v[2], v[3], True]
                if v[3] in inq:
                    finder[v[3]][4] = False
                inq.add(v[3])
                finder[v[3]] = entry

                heapq.heappush(h, entry)

    return keys

# 5122 too high  cnkeoiqdjrtwbuzvyfhmalgsxp
# 5090 too high  onkjciqdtzvyerwbuhfmaslgxp
# 5088           nkojciqdtezvyrwbuhfmalgsxp  (not right answer)
# first set [((33, 48), 'o', 16), ((45, 50), 'n', 28), ((3, 50), 'c', 88), ((55, 2), 'z', 104)]

count = 0
min_end = 5088
min_seq = None

def recur(me, grid, doors, _keys, _max, dist, seq):
    global count, min_end, min_seq
    keys = dijkstra(me, grid, _max)
    #print(keys)
    #return

    order = sorted(keys, key=lambda x:x[2])
    if len(seq) == 0:
       order = [keys[0], keys[2], keys[1], keys[3]]

    rets = []
    for k in order:
        door = k[1].upper()
        if count % 10000 == 0:
            print(count, 'trying', seq, k[1], dist, 'min', min_end, min_seq)
        count += 1
        if len(seq) == len(_keys):
            if dist + k[2] < min_end:
                print('new min_end', dist + k[2], seq, k[1], len(seq))
                min_end = dist + k[2]
                min_seq = seq + k[1]
            rets.append(dist + k[2])
            continue
        if dist + k[2] > min_end:
            continue
        gridnew = grid.copy()
        gridnew[k[0]] = '.'
        if door in doors: # some keys don't have matching doors
            gridnew[doors[door]] = '.'
        rets.append( recur(k[0], gridnew, doors, _keys, _max, dist + k[2], str(seq) + k[1]) )

    if len(rets) == 0:
        if len(seq) == len(_keys):
            if dist < min_end:
                print('new min_end', dist, seq)
                min_end = dist
                min_seq = seq
            elif dist == min_end:
                print('another min_end', dist, seq)
            return dist
        return 99999999

    return min(rets)

with open('18.txt') as f:
    line = f.readline().strip()

    grid = dict()
    doors = dict()
    _keys = dict()
    me = None
    y = 0
    for line in (l.strip() for l in f.readlines()):
        for x in range(0, len(line)):
            grid[(x,y)] = line[x]
            if line[x] == '@':
                grid[(x,y)] = '.'
                me = (x,y)
            elif line[x] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                doors[line[x]] = (x,y)
            elif line[x] in 'abcdefghijklmnopqrstuvwxyz':
                _keys[line[x]] = (x,y)
        y += 1
    _max = (x,y)

    printg2(grid, _max, me)
    print(me)
    print(doors)
    print(len(_keys), _keys)

    ret = recur(me, grid.copy(), doors, _keys, _max, 0, '')
    print(ret)

    exit()
