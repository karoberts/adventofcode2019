import re
import sys
import heapq
import json
import datetime
import curses
import time
from curses import wrapper
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

def set_to_key(s):
    return ''.join(sorted(s))

def list_to_key(s):
    return ''.join(s)

def dijkstra_nodes(ome, me, grid, _max, memo, _keys, doors):
    def get_neighbor_keys(pt_id, opendoors, foundkeys, foundkeylist):
        possible = []
        for k in _keys.keys():
            if k == pt_id: continue
            door = k.upper()
            if door in opendoors: continue
            info = memo[(pt_id, k)]
            if len(info[2] - foundkeys) != 0: # if we cross a key we don't have yet, don't do this one
                continue
            needed_doors = info[1]
            if len(needed_doors - opendoors) == 0:
                #possible.append( (k, info[0]) )
                nopendoors = opendoors.copy()
                nopendoors.add(door)
                nfoundkeys = foundkeys.copy()
                nfoundkeys.add(k)
                nfoundkeylist = foundkeylist.copy()
                nfoundkeylist.append(k)
                #possible.append( [info[0], _keys[k], nopendoors, nfoundkeys, nfoundkeylist, list_to_key(nfoundkeylist) ] )
                possible.append( [info[0], _keys[k], nopendoors, nfoundkeys, nfoundkeylist, set_to_key(nfoundkeys) + str(_keys[k]) ] )

        records = sorted(possible, key=lambda x:x[0])
        return [x for _, x in zip(range(4), records)]

    dist = defaultdict(lambda :999999999)

    finder = {}
    finder2 = {}

    inq = set()
    h = []
    # 0  : how many keys left
    # 1  : (x,y)
    # 2  : doors
    # 3  : key set
    # 4  : key list
    # 5  : 'key' == keys
    # 6  : valid
    # 7  : dist
    heapq.heappush(h, [len(_keys), me, set(), set(), list(), ''+str(me), True, 0])
    dist[h[0][5]] = 0
    finder[h[0][5]] = h[0]
    finder2[me] = (set(), h[0])
    inq.add(h[0][5])

    max_found = 0
    min_steps = 99999999

    while len(h) > 0:
        #print_map(dist);
        u = heapq.heappop(h)
        #print(len(u[5]) * ' ', 'at', u)
        if not u[6]:
            continue
        inq.remove(u[5])
        uk = u[5]
        pt_id = '@' if u[1] == ome else grid[u[1]]
        for v in get_neighbor_keys(pt_id, u[2], u[3], u[4]):
            #print(len(v[5]) * ' ', 'going to', v, 'steps', dist[uk] + v[0])
            if len(v[4]) == len(_keys):
                if dist[uk] + v[0] < min_steps:
                    #print(datetime.datetime.now(), 'found end! at', v[1], dist[uk] + v[0], 'steps', v[5])
                    min_steps = dist[uk] + v[0]
                    if min_steps == 4900:
                        return v[4]
                continue
            alt = dist[uk] + v[0]
            if alt > min_steps:
                continue
            if alt < dist[v[5]]:
                dist[v[5]] = alt
                entry = [len(_keys) - len(v[5]), v[1], v[2], v[3], v[4], v[5], True, alt]
                if v[5] in inq:
                    finder[v[5]][6] = False

                other = None if v[1] not in finder2 else finder2[v[1]]
                if other and other[0] == v[3] and other[1][7] > alt: # other path with same keys to same position (diff order)
                    if v[5] in finder:
                        finder[v[5]][6] = False

                inq.add(v[5])
                finder[v[5]] = entry
                finder2[v[1]] = (v[3], entry)

                """
                if len(v[4]) > max_found:
                    print('so far', v[5], len(v[4]), 'of', len(_keys))
                    max_found = len(v[4])
                """

                heapq.heappush(h, entry)
            #else:
            #   print(len(v[5]) * ' ', 'skip', v)
        
    #print(dist)

    return None

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

            if tt == '.' or tt == '_':
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
    path = [k2]
    while p != k1:
        #print( prev[p] )
        p = prev[p][0]
        path.append(p)
        if p != k1:
            if grid[p] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                crossed_doors.add(grid[p])
            if grid[p] in 'abcdefghijklmnopqrstuvwxyz':
                crossed_keys.add(grid[p])

    return (dist[k2], crossed_doors, crossed_keys, path)

def make_memo(_keys:dict, doors:dict, grid:dict, _max:tuple, me:tuple, ret:list):
    memo = dict()

    #print(doors)
    for i in range(0, len(ret) - 1):
        k = ret[i]
        k2 = ret[i + 1]
        r = memo_dijkstra_finddoors(_keys[k], _keys[k2], grid, _max)
        #print(k, 'to', k2, r)
        memo[(k, k2)] = r
    #printg2(g, _max, None)

    memo[('@', ret[0])] = memo_dijkstra_finddoors(me, _keys[ret[0]], grid, _max)

    #print(memo)

    return memo

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

def map_visible(grid:dict, pos:tuple, visible:set):
    tests = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]

    q = [pos]
    while len(q) > 0:
        pos = q.pop()

        for t in tests:
            tk = (pos[0] + t[0], pos[1] + t[1])
            tt = grid[tk]

            if tk in visible:
                continue

            if tt == '.':
                visible.add(tk)
                q.append(tk)
            if tt in 'abcdefghijklmnopqrstuvwxyz':
                q.append(tk)

def main(stdscr):

    stdscr.clear()
    curses.curs_set(0)
    stdscr.refresh()

    COLOR_BLACK_WHITE = 0
    COLOR_RED_BLACK = 1
    COLOR_CYAN_BLACK = 2
    COLOR_WHITE_BLACK = 3
    COLOR_YELLOW_BLACK = 4
    COLOR_GREEN_BLACK = 5
    COLOR_BLACK_YELLOW = 6
    COLOR_BLACK_CYAN = 7

    curses.init_pair(COLOR_RED_BLACK, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_CYAN_BLACK, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_WHITE_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_YELLOW_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_GREEN_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_BLACK_YELLOW, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(COLOR_BLACK_CYAN, curses.COLOR_BLACK, curses.COLOR_CYAN)

    COLOR_DEVICE = curses.color_pair(COLOR_RED_BLACK)
    COLOR_WALLS = curses.color_pair(COLOR_BLACK_WHITE)
    COLOR_DOORS = curses.color_pair(COLOR_BLACK_YELLOW)
    COLOR_KEYS_HAVE = curses.color_pair(COLOR_BLACK_CYAN)
    COLOR_KEYS_NEED = curses.color_pair(COLOR_YELLOW_BLACK)
    COLOR_VISITED = curses.color_pair(COLOR_CYAN_BLACK) | curses.A_DIM
    COLOR_VISIBLE = curses.color_pair(COLOR_GREEN_BLACK) | curses.A_DIM
    COLOR_FLOOR = curses.color_pair(COLOR_WHITE_BLACK) | curses.A_DIM

    block = bytes([0xE2,0x96, 0x88])
    def printg_curses(stdscr, g, _max, me, doors, _keys, gotkeys, visited:set, visible:set, steps:int):
        stdscr.erase()
        for y in range(0, _max[1] + 1):
            for x in range(0, _max[0] + 1):
                c = (x,y)
                sc_y = y
                sc_x = x
                try:
                    if c == me:
                        stdscr.insstr(sc_y, sc_x, block, COLOR_DEVICE)
                    elif c in doors:
                        stdscr.insstr(sc_y, sc_x, doors[c], COLOR_DOORS)
                    elif c in _keys:
                        if _keys[c] in gotkeys:
                            stdscr.insstr(sc_y, sc_x, _keys[c], COLOR_KEYS_HAVE)
                        else:
                            stdscr.insstr(sc_y, sc_x, _keys[c], COLOR_KEYS_NEED)
                    elif c in visited:
                        stdscr.insstr(sc_y, sc_x, block, COLOR_VISITED)
                    elif c in visible:
                        stdscr.insstr(sc_y, sc_x, block, COLOR_VISIBLE)
                    elif c in g:
                        if g[c] == '#':
                            stdscr.insstr(sc_y, sc_x, block, COLOR_WALLS)
                        elif g[c] == '.':
                            stdscr.insstr(sc_y, sc_x, block, COLOR_FLOOR)
                    else:
                        stdscr.insch(sc_y, sc_x, ' ')
                except (curses.error):
                    pass
        try:
            stdscr.addstr(2, _max[0] + 5, 'Steps: {}'.format(steps))
            stdscr.addstr(3, _max[0] + 5, 'Keys : ')
            xpos = _max[0] + 5 + 7
            for k in 'abcdefghijklmnopqrstuvwxyz':
                if k in gotkeys:
                    stdscr.addstr(3, xpos, k, curses.color_pair(COLOR_CYAN_BLACK))
                else:
                    stdscr.addstr(3, xpos, k)
                stdscr.addstr(3, xpos + 1, ' ')
                xpos += 2
        except (curses.error):
            pass
        stdscr.refresh()

    with open('18.txt') as f:
        grid = dict()
        doors = dict()
        _keys = dict()
        rdoors = dict()
        r_keys = dict()
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
                    rdoors[(x,y)] = line[x]
                elif line[x] in 'abcdefghijklmnopqrstuvwxyz':
                    _keys[line[x]] = (x,y)
                    r_keys[(x,y)] = line[x]
            y += 1
        _max = (x,y)

        visible = set()
        visited = set()
        map_visible(grid, me, visible)

        printg_curses(stdscr, grid, _max, me, rdoors, r_keys, dict(), visited, visible, 0)

        ret = ['n', 'o', 'j', 'i', 'q', 'd', 't', 'c', 'k', 'w', 'u', 'b', 'z', 'v', 'y', 'e', 'r', 'f', 'h', 'm', 'a', 's', 'l', 'g', 'x', 'p']

        memo = make_memo(_keys, doors, grid, _max, me, ret)
        time.sleep(1.0)

        last_k = '@'
        gotkeys = set()
        steps = 0
        for k in ret:
            prev = memo[(last_k, k)][3]
            for p in reversed(prev):
                visited.add(p)
                printg_curses(stdscr, grid, _max, p, rdoors, r_keys, gotkeys, visited, visible, steps)
                me = p
                steps += 1
            steps -= 1
            #time.sleep(0.0001)
            gotkeys.add(k)
            rdoors.pop( doors[k.upper()] ) 
            grid[doors[k.upper()]] = '.'
            visible.clear()
            map_visible(grid, p, visible)
            last_k = k
            printg_curses(stdscr, grid, _max, p, rdoors, r_keys, gotkeys, visited, visible, steps)
            #stdscr.getch()

        printg_curses(stdscr, grid, _max, me, rdoors, r_keys, gotkeys, visited, visible, steps)
        stdscr.getch()

wrapper(main)
