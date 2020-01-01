import re
import sys
import heapq
import json
import datetime
import copy
from collections import defaultdict

class Robot:
    def __init__(self, id:int, coord:tuple):
        self.id = id
        self.coord = coord
        self.orig_coord = coord
        self.memo = None

    def __repr__(self):
        return 'Bot[{}, @{}]'.format(self.id, self.coord)

def printg2(g, _max, bots:list):
    for y in range(0, _max[1] + 1):
        for x in range(0, _max[0] + 1):
            c = (x,y)
            for b in bots:
                if c == b.coord: 
                    print(b.id, end='')
                    break
            else:
                if c in g:
                    print(g[c], end='')
                else:
                    print(' ', end='')
        print()
    print()

def memo_dijkstra_finddoors(k1:tuple, k2:tuple, grid:dict, _max:tuple):
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
                ns.append( [1, tx, ty, tk, '.'] )
            if tt in 'abcdefghijklmnopqrstuvwxyz':
                ns.append( [1, tx, ty, tk, 'k'] )
            if tt in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                ns.append( [1, tx, ty, tk, 'd'] )

        for n in ns:
            n.append(True)
        return ns

    dist = defaultdict(lambda :999999999)
    prev = {}

    dist[k1] = 0
    prev[k1] = None

    finder = {}

    inq = set()
    h = []
    heapq.heappush(h, [0, k1[0], k1[1], k1, True])
    finder[k1] = h[0]
    inq.add(k1)
    done = False

    while len(h) > 0 and not done:
        #print_map(dist);
        u = heapq.heappop(h)
        if not u[4]:
            continue
        inq.remove(u[3])
        #if u[1] == target_y and u[2] == target_y:
            #return u
        uk = u[3]
        for v in get_neighbors(u[1], u[2]):
            if v[3] == k2:
                dist[v[3]] = dist[uk] + v[0]
                prev[v[3]] = (uk, v[0], v[1], v[2])
                #print('found key:', grid[v[3]], 'at', v[3], dist[uk] + v[0], 'steps')
                #keys.append((v[3], grid[v[3]], dist[uk] + v[0]))
                done = True
                break

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

    crossed_doors = set()
    crossed_keys = set()
    p = k2
    if p not in prev:
        return None
    while p != k1:
        #print( prev[p] )
        p = prev[p][0]
        if p != k1:
            if grid[p] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                crossed_doors.add(grid[p])
            if grid[p] in 'abcdefghijklmnopqrstuvwxyz':
                crossed_keys.add(grid[p])

    return (dist[k2], crossed_doors, crossed_keys)

def make_memo(_keys:dict, doors:dict, grid:dict, _max:tuple, me:tuple):
    memo = dict()

    for k in _keys.keys():
        for k2 in _keys.keys():
            if k == k2: continue
            r = memo_dijkstra_finddoors(_keys[k], _keys[k2], grid, _max)
            if r is None:
                continue
            #print(k, 'to', k2, r)
            memo[(k, k2)] = r
    #printg2(g, _max, None)

    for k in _keys.keys():
        r = memo_dijkstra_finddoors(me, _keys[k], grid, _max)
        if r is None: continue
        memo[('@', k)] = r

    return memo

count = 0
min_end = 2683

def get_keys(pt_id, _keys, bot, opendoors, foundkeys):
    possible = []
    for k in _keys.keys():
        if k == pt_id: continue
        if k.upper() in opendoors: continue
        m_k = (pt_id, k)
        if m_k not in bot.memo: continue
        info = bot.memo[m_k]
        if len(info[2] - foundkeys) != 0: # if we cross a key we don't have yet, don't do this one
            continue
        needed_doors = info[1]
        if len(needed_doors - opendoors) == 0:
            possible.append( (k, info[0]) )

    records = sorted(possible, key=lambda x:x[1])
    return [x for _, x in zip(range(40), records)]


def recur_memo(bots, grid, doors, _keys, _max, dist, opendoors, foundkeys, depth):

    global count, min_end

    for bot in bots:
        pt_id = '@' if bot.coord == bot.orig_coord else grid[bot.coord]
        #print(' ' * depth, 'going to', pt_id)
        keys = get_keys(pt_id, _keys, bot, opendoors, foundkeys)

        rets = []
        for k in keys:
            #print(' ' * depth, 'dist=', dist, bot, 'going to', k, _keys[k[0]])
            door = k[0].upper()
            if count % 10000 == 0:
                print(count, datetime.datetime.now(), 'trying', k[0], dist, 'min', min_end)
            count += 1
            if len(foundkeys) == len(_keys):
                if dist + k[1] < min_end:
                    print('new min_end', dist + k[1], k[0])
                    min_end = dist + k[1]
                rets.append(dist + k[1])
                continue
            if dist + k[1] > min_end:
                continue
            nopendoors = opendoors.copy()
            nopendoors.add(door)
            nfoundkeys = foundkeys.copy()
            nfoundkeys.add(k[0])
            nbots = copy.deepcopy(bots)
            nbots[bot.id].coord = _keys[k[0]]
            rets.append( recur_memo(nbots, grid, doors, _keys, _max, dist + k[1], nopendoors, nfoundkeys, depth + 1) )

    if len(rets) == 0:
        if len(foundkeys) == len(_keys):
            if dist < min_end:
                print('new min_end', dist, count)
                min_end = dist
                """
            elif dist == min_end:
                print('another min_end', dist, seq)
                """
            return dist
        return 99999999

    return min(rets + [min_end])

# 2774 - too high
# 2682 - too high

with open('18-2.txt') as f:
    grid = dict()
    doors = dict()
    _keys = dict()
    y = 0
    botid = 0
    bots = []
    for line in (l.strip() for l in f.readlines()):
        for x in range(0, len(line)):
            grid[(x,y)] = line[x]
            if line[x] == '@':
                grid[(x,y)] = '.'
                bots.append( Robot(botid, (x,y)) )
                botid += 1
            elif line[x] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                doors[line[x]] = (x,y)
            elif line[x] in 'abcdefghijklmnopqrstuvwxyz':
                _keys[line[x]] = (x,y)
        y += 1
    _max = (x,y)

    printg2(grid, _max, bots)

    for bot in bots:
        print('making memo for', bot)
        bot.memo = make_memo(_keys, doors, grid, _max, bot.coord)
        print('memo complete', len(bot.memo), bot.memo)

    #print( get_keys('@', _keys, bots[0], set(), set()) )
    #exit()

    printg2(grid, _max, bots)
    print(doors)
    print(len(_keys), _keys)

    ret = recur_memo(bots, grid.copy(), doors, _keys, _max, 0, set(), set(), 0)
    print('part2', min_end)

    exit()
