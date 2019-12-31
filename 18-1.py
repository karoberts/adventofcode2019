import re
import sys
import heapq
import json
import datetime
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

    #print(doors)
    for k in _keys.keys():
        for k2 in _keys.keys():
            if k == k2: continue
            r = memo_dijkstra_finddoors(_keys[k], _keys[k2], grid, _max)
            #print(k, 'to', k2, r)
            memo[(k, k2)] = r
    #printg2(g, _max, None)

    for k in _keys.keys():
        r = memo_dijkstra_finddoors(me, _keys[k], grid, _max)
        memo[('@', k)] = r

    #print(memo)

    return memo

# 5122 too high  cnkeoiqdjrtwbuzvyfhmalgsxp
# 5090 too high  onkjciqdtzvyerwbuhfmaslgxp
# 5088           nkojciqdtezvyrwbuhfmalgsxp  (not right answer)
# 4942           onkjiqdctzvyerwbuhfmaslgxp  (not right answer)
# 4940           nkojiqdctzvyerwbuhfmaslgxp  (not right answer)
# 4938           onkjiqdctwbuzvyerhfmaslgxp  ???
# 4906           onjiqdkwbuctzvyerhfmaslgxp  ???
# 4902           onjiqdctkwbuzvyerhfmaslgxp  ???
# 4900           nojiqdctkwbuzvyerhfmaslgxp  !!!! right answer !!!!
# first set [((33, 48), 'o', 16), ((45, 50), 'n', 28), ((3, 50), 'c', 88), ((55, 2), 'z', 104)]

count = 0
min_end = 4940
min_seq = None

def get_keys(pt_id, _keys, memo, opendoors, foundkeys):
    possible = []
    for k in _keys.keys():
        if k == pt_id: continue
        if k.upper() in opendoors: continue
        info = memo[(pt_id, k)]
        if len(info[2] - foundkeys) != 0: # if we cross a key we don't have yet, don't do this one
            continue
        needed_doors = info[1]
        if len(needed_doors - opendoors) == 0:
            possible.append( (k, info[0]) )

    records = sorted(possible, key=lambda x:x[1])
    return [x for _, x in zip(range(4), records)]


def recur_memo(ome, me, grid, doors, _keys, _max, dist, seq, opendoors, foundkeys, memo):

    global count, min_end, min_seq
    pt_id = '@' if me == ome else grid[me]
    keys = get_keys(pt_id, _keys, memo, opendoors, foundkeys)
    """
    if len(opendoors) == 6:
        print('==>', pt_id, keys, opendoors)
        return 999999
        """

    rets = []
    for k in keys:
        door = k[0].upper()
        if count % 10000000 == 0:
            print(count, datetime.datetime.now(), 'trying', seq, k[0], dist, 'min', min_end, min_seq)
        count += 1
        if len(seq) == len(_keys):
            if dist + k[1] < min_end:
                print('new min_end', dist + k[1], seq, k[0], len(seq))
                min_end = dist + k[1]
                min_seq = seq + k[0]
            rets.append(dist + k[1])
            continue
        if dist + k[1] > min_end:
            continue
        #gridnew = grid.copy()
        #gridnew[k[0]] = '.'
        nopendoors = opendoors.copy()
        nopendoors.add(door)
        nfoundkeys = foundkeys.copy()
        nfoundkeys.add(k[0])
        #if door in doors: # some keys don't have matching doors
        #    gridnew[doors[door]] = '.'
        rets.append( recur_memo(ome, _keys[k[0]], grid, doors, _keys, _max, dist + k[1], str(seq) + k[0], nopendoors, nfoundkeys, memo) )

    if len(rets) == 0:
        if len(seq) == len(_keys):
            if dist < min_end:
                print('new min_end', dist, seq)
                min_end = dist
                min_seq = seq
                """
            elif dist == min_end:
                print('another min_end', dist, seq)
                """
            return dist
        return 99999999

    return min(rets)

def recur(me, grid, doors, _keys, _max, dist, seq):
    global count, min_end, min_seq
    keys = dijkstra(me, grid, _max)
    #print(keys)
    #return

    order = sorted(keys, key=lambda x:x[2])
    if len(seq) == 0:
       order = [keys[1], keys[2], keys[0], keys[3]]

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
                ome = (x,y)
            elif line[x] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                doors[line[x]] = (x,y)
            elif line[x] in 'abcdefghijklmnopqrstuvwxyz':
                _keys[line[x]] = (x,y)
        y += 1
    _max = (x,y)

    print('making memo')
    memo = make_memo(_keys, doors, grid, _max, me)
    print('memo complete', len(memo))

    #print( get_keys('@', _keys, memo, set(), set()) )
    #print( get_keys('o', _keys, memo, set(['O']), set(['o'])) )
    #print( get_keys('n', _keys, memo, set(['O', 'N']), set(['o', 'n'])) )
    #exit()

    printg2(grid, _max, me)
    print(me)
    print(doors)
    print(len(_keys), _keys)

    #ret = recur(me, grid.copy(), doors, _keys, _max, 0, '')
    ret = recur_memo(ome, me, grid.copy(), doors, _keys, _max, 0, '', set(), set(), memo)
    print(ret)

    exit()
