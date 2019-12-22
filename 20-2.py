import re
import sys
import heapq
import json
from collections import defaultdict

def printg2(g, _max, me, tgt):
    for y in range(0, _max[1] + 1):
        for x in range(0, _max[0] + 1):
            c = (x,y)
            if c == me:
                print('@', end='')
            elif c == tgt:
                print('!', end='')
            elif c in g:
                print(g[c], end='')
            else:
                print(' ', end='')
        print()
    print()

def dijkstra(me, tgt, grid, _max, portal_coords, portals, outer_portals, inner_portals):
    tests = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]
    def get_neighbors(x,y,lev):
        k = (x,y)
        c = grid[k]
        ns = []

        for t in tests:
            tx = x + t[0]
            ty = y + t[1]
            if tx < 0 or ty < 0 or tx >= _max[0] or ty >= _max[1]:
                continue
            itk = (tx, ty)
            tt = grid[itk]
            tk = (tx, ty, lev)

            if tt == '.':
                ns.append( [1, tx, ty, lev, tk, False] )
            if tt in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                portal_id = portal_coords[itk][0]
                if portal_id == 'AA': 
                    continue
                if portal_id == 'ZZ':
                    if lev == 0:
                        ns.append( [1, tx, ty, lev, tk, True] )
                    continue
                portal_tgts = portals[portal_id]
                #print('found portal', tt, tk, k, portal_id, portal_tgts)
                if k == portal_tgts[0]:
                    p = portal_tgts[1]
                else:
                    p = portal_tgts[0]
                if itk in outer_portals:
                    if lev > 0:
                        ns.append( [1, p[0], p[1], lev - 1, (p[0], p[1], lev - 1), False] )
                elif itk in inner_portals:
                    ns.append( [1, p[0], p[1], lev + 1, (p[0], p[1], lev + 1), False] )
                else:
                    print('bad portal', k, itk, p, portal_tgts)
                    exit()

        for n in ns:
            n.append(True)
        return ns

    dist = defaultdict(lambda :999999999)
    prev = {}

    k_me = (me[0], me[1], 0)
    dist[k_me] = 0
    prev[k_me] = None

    finder = {}

    inq = set()
    h = []
    heapq.heappush(h, [0, me[0], me[1], 0, k_me, True])
    finder[k_me] = h[0]
    inq.add(k_me)

    while len(h) > 0:
        #print_map(dist);
        u = heapq.heappop(h)
        if not u[5]:
            continue
        inq.remove(u[4])
        #if u[1] == target_y and u[2] == target_y:
            #return u
        uk = u[4]
        for v in get_neighbors(u[1], u[2], u[3]):
            if v[5]:
                print('found zz at level 0:', grid[(v[4][0], v[4][1])], 'at', v[4], dist[uk] + v[0], 'steps')
                return dist[uk]
            alt = dist[uk] + v[0]
            if alt < dist[v[4]]:
                dist[v[4]] = alt
                #prev[v[4]] = (uk, v[0], v[1], v[2])
                entry = [alt, v[1], v[2], v[3], v[4], True]
                if v[4] in inq:
                    finder[v[4]][5] = False
                inq.add(v[4])
                finder[v[4]] = entry

                heapq.heappush(h, entry)

    return dist[tgt]

# NOT 691

with open('20.txt') as f:
    grid = dict()
    portal_items = []
    portals = defaultdict(list)
    portal_coords = defaultdict(list)
    inner_portals = dict()
    outer_portals = dict()
    me = None
    tgt = None
    y = 0
    for line in f.readlines():
        for x in range(0, len(line) - 1):
            if line[x] == '#' or line[x] == '.':
                grid[(x,y)] = line[x]
            elif line[x] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                grid[(x,y)] = line[x]
                portal_items.append(((x,y), line[x]))
        y += 1
    _max = (x,y)
    print(_max)
    y_edge = _max[1] - 4
    x_edge = _max[0] - 4

    for pi in portal_items:
        c = grid[pi[0]]
        up = (pi[0][0], pi[0][1] - 1)
        dn = (pi[0][0], pi[0][1] + 1)
        lf = (pi[0][0] - 1, pi[0][1])
        ri = (pi[0][0] + 1, pi[0][1])
        if up in grid and grid[up] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            up2 = (pi[0][0], pi[0][1] - 2)
            if up2 in grid and grid[up2] == '.':
                portal_coords[up].append(grid[up] + c)
                portals[grid[up] + c].append(up2)
                if grid[up] + c == 'AA': me = up2
                if grid[up] + c == 'ZZ': tgt = up2
                if up[1] < 3 or up[1] > y_edge:
                    outer_portals[up] = grid[up] + c
                else:
                    inner_portals[up] = grid[up] + c
            """
            elif dn in grid and grid[dn] == '.':
                portal_coords[pi[0]].append(grid[up] + c)
                portals[grid[up] + c].append(pi[0])
            """
        elif dn in grid and grid[dn] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            dn2 = (pi[0][0], pi[0][1] + 2)
            if dn2 in grid and grid[dn2] == '.':
                portal_coords[dn].append(c + grid[dn])
                portals[c + grid[dn]].append(dn2)
                if c + grid[dn] == 'AA': me = dn2
                if c + grid[dn] == 'ZZ': tgt = dn2
                if dn[1] < 3 or dn[1] > y_edge:
                    outer_portals[dn] = c + grid[dn]
                else:
                    inner_portals[dn] = c + grid[dn]
            """
            elif up in grid and grid[up] == '.':
                portal_coords[pi[0]].append(c + grid[dn])
                portals[grid[dn] + c].append(pi[0])
            """
        elif ri in grid and grid[ri] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            ri2 = (pi[0][0] + 2, pi[0][1])
            if ri2 in grid and grid[ri2] == '.':
                portal_coords[ri].append(c + grid[ri])
                portals[c + grid[ri]].append(ri2)
                if c + grid[ri] == 'AA': me = ri2
                if c + grid[ri] == 'ZZ': tgt = ri2
                if ri[0] < 3 or ri[0] > x_edge:
                    outer_portals[ri] = c + grid[ri]
                else:
                    inner_portals[ri] = c + grid[ri]
            """
            elif lf in grid and grid[lf] == '.':
                portal_coords[pi[0]].append(c + grid[ri])
                portals[grid[ri] + c].append(pi[0])
            """
        elif lf in grid and grid[lf] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            lf2 = (pi[0][0] - 2, pi[0][1])
            if lf2 in grid and grid[lf2] == '.':
                portal_coords[lf].append(grid[lf] + c)
                portals[grid[lf] + c].append(lf2)
                if grid[lf] + c == 'AA': me = lf2
                if grid[lf] + c == 'ZZ': tgt = lf2
                if lf[0] < 3 or lf[0] > x_edge:
                    outer_portals[lf] = grid[lf] + c 
                else:
                    inner_portals[lf] = grid[lf] + c 
            """
            elif ri in grid and grid[ri] == '.':
                portal_coords[pi[0]].append(grid[lf] + c)
                portals[grid[lf] + c].append(pi[0])
            """

    #print(portals)
    #print(portal_coords)
    print('outer', outer_portals)
    print('inner', inner_portals)

    #printg2(grid, _max, me, tgt)

    r = dijkstra(me, tgt, grid, _max, portal_coords, portals, outer_portals, inner_portals)

    print(r)
