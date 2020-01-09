import re
import sys
import heapq
import json
import datetime
import curses
import time
from curses import wrapper
from collections import defaultdict

class Robot:
    def __init__(self, id:int, coord:tuple):
        self.id = id
        self.coord = coord
        self.orig_coord = coord
        self.memo = None
        self.path = []

    def __lt__(self, x):
        return self.coord < x.coord

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

def set_to_key(s):
    return ''.join(sorted(s))

def list_to_key(s):
    return ''.join(s)

def bots_to_key(bots):
    return ''.join((str(p.coord) for p in bots))

def dijkstra_nodes(bots, grid, _max, _keys, doors):
    def get_neighbor_keys(bots, opendoors, foundkeys, foundkeylist):
        possible = []
        for bot in bots:
            pt_id = '@' if bot.coord == bot.orig_coord else grid[bot.coord]
            for k in _keys.keys():
                if k == pt_id: continue
                door = k.upper()
                if door in opendoors: continue
                m_k = (pt_id, k)
                if m_k not in bot.memo: continue
                info = bot.memo[m_k]
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
                    nbots = copy.deepcopy(bots)
                    nbots[bot.id].coord = _keys[k]
                    possible.append( [info[0], nbots, nopendoors, nfoundkeys, nfoundkeylist, set_to_key(nfoundkeys) + bots_to_key(nbots) ] )

        records = sorted(possible, key=lambda x:x[0])
        return [x for _, x in zip(range(40), records)]

    dist = defaultdict(lambda :999999999)

    finder = {}
    finder2 = {}

    inq = set()
    h = []
    # 0  : how many keys left
    # 1  : bots
    # 2  : doors
    # 3  : key set
    # 4  : key list
    # 5  : 'key' == keys
    # 6  : valid
    # 7  : dist
    heapq.heappush(h, [len(_keys), bots, set(), set(), list(), ''+bots_to_key(bots), True, 0])
    dist[h[0][5]] = 0
    finder[h[0][5]] = h[0]
    #finder2[me] = (set(), h[0])
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
        for v in get_neighbor_keys(u[1], u[2], u[3], u[4]):
            #print(len(v[5]) * ' ', 'going to', v, 'steps', dist[uk] + v[0])
            if len(v[4]) == len(_keys):
                if dist[uk] + v[0] < min_steps:
                    #print(datetime.datetime.now(), 'found end! at', v[1], dist[uk] + v[0], 'steps', v[5])
                    min_steps = dist[uk] + v[0]
                    #print('->path', v[4])
                continue
            alt = dist[uk] + v[0]
            if alt > min_steps:
                continue
            if alt < dist[v[5]]:
                dist[v[5]] = alt
                entry = [len(_keys) - len(v[5]), v[1], v[2], v[3], v[4], v[5], True, alt]
                if v[5] in inq:
                    finder[v[5]][6] = False

                """
                other = None if v[1] not in finder2 else finder2[v[1]]
                if other and other[0] == v[3] and other[1][7] > alt: # other path with same keys to same position (diff order)
                    if v[5] in finder:
                        finder[v[5]][6] = False
                """

                inq.add(v[5])
                finder[v[5]] = entry
                #finder2[v[1]] = (v[3], entry)

                """
                if len(v[4]) > max_found:
                    print('so far', v[5], len(v[4]), 'of', len(_keys))
                    max_found = len(v[4])
                """

                heapq.heappush(h, entry)
            #else:
            #   print(len(v[5]) * ' ', 'skip', v)
        
    #print(dist)

    return min_steps

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

    for i in range(0, len(ret) - 1):
        k = ret[i]
        k2 = ret[i + 1]
        r = memo_dijkstra_finddoors(_keys[k], _keys[k2], grid, _max)
        if r is None:
            continue
        memo[(k, k2)] = r

    for k in ret:
        r = memo_dijkstra_finddoors(me, _keys[k], grid, _max)
        if r is None: continue
        memo[('@', k)] = r
        break

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

bots = []
def main(stdscr):

    stdscr.clear()
    curses.curs_set(0)
    stdscr.refresh()

    #stdscr.idcok(False)
    #stdscr.idlok(False)

    COLOR_BLACK_WHITE = 0
    COLOR_RED_BLACK = 1
    COLOR_CYAN_BLACK = 2
    COLOR_WHITE_BLACK = 3
    COLOR_YELLOW_BLACK = 4
    COLOR_GREEN_BLACK = 5
    COLOR_BLACK_YELLOW = 6
    COLOR_BLACK_CYAN = 7
    COLOR_BLACK_RED = 8

    curses.init_pair(COLOR_RED_BLACK, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_CYAN_BLACK, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_WHITE_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_YELLOW_BLACK, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(COLOR_GREEN_BLACK, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_BLACK_YELLOW, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(COLOR_BLACK_CYAN, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(COLOR_BLACK_RED, curses.COLOR_BLACK, curses.COLOR_RED)

    COLOR_DEVICE = curses.color_pair(COLOR_RED_BLACK)
    COLOR_WALLS = curses.color_pair(COLOR_BLACK_WHITE)
    COLOR_DOORS = curses.color_pair(COLOR_BLACK_YELLOW)
    COLOR_KEYS_HAVE = curses.color_pair(COLOR_BLACK_CYAN)
    COLOR_KEYS_NEED = curses.color_pair(COLOR_YELLOW_BLACK)
    COLOR_VISITED = curses.color_pair(COLOR_CYAN_BLACK) | curses.A_DIM
    COLOR_VISIBLE = curses.color_pair(COLOR_GREEN_BLACK) | curses.A_DIM
    COLOR_FLOOR = curses.color_pair(COLOR_WHITE_BLACK) | curses.A_DIM
    COLOR_STATUS_KEYS_HAVE = curses.color_pair(COLOR_CYAN_BLACK)
    COLOR_STATUS_KEYS_NEED = curses.color_pair(COLOR_WHITE_BLACK) | curses.A_DIM

    block = bytes([0xE2,0x96, 0x88,0xE2,0x96, 0x88])
    def printg_curses(stdscr, g, _max, botpos, doors, _keys, gotkeys, visited:set, visible:set, steps:int, end:bool = False):
        stdscr.erase()
        sy = 0
        sx = 0
        for y in range(0, _max[1] + 1):
            for x in range(0, _max[0] + 1):
                c = (x,y)
                if c in botpos:
                    stdscr.addstr(sy, sx, block, COLOR_DEVICE)
                    pass
                elif c in doors:
                    stdscr.addstr(sy, sx, doors[c] + doors[c], COLOR_DOORS)
                elif c in _keys:
                    if _keys[c] in gotkeys:
                        stdscr.addstr(sy, sx, _keys[c] + _keys[c], COLOR_KEYS_HAVE)
                    else:
                        stdscr.addstr(sy, sx, _keys[c] + _keys[c], COLOR_KEYS_NEED)
                elif c in visited:
                    stdscr.addstr(sy, sx, block, COLOR_VISITED)
                elif c in visible:
                    stdscr.addstr(sy, sx, block, COLOR_VISIBLE)
                elif c in g:
                    if g[c] == '#':
                        stdscr.addstr(sy, sx, block, COLOR_WALLS)
                    elif g[c] == '.':
                        stdscr.addstr(sy, sx, block, COLOR_FLOOR)
                sx += 2
            sx = 0
            sy += 1

        stdscr.addstr(2, _max[0] * 2 + 5, 'Steps: {}'.format(steps))
        stdscr.addstr(3, _max[0] * 2 + 5, 'Keys : ')
        xpos = _max[0] * 2 + 5 + 7
        for k in 'abcdefghijklmnopqrstuvwxyz':
            if k in gotkeys:
                stdscr.addstr(3, xpos, k, COLOR_STATUS_KEYS_HAVE)
            else:
                stdscr.addch(3, xpos, k, COLOR_STATUS_KEYS_NEED)
            xpos += 2

        if end:
            stdscr.addstr(8, _max[0] * 2 + 5, 'Press enter to exit')

        stdscr.refresh()

    with open('18-2.txt') as f:
        grid = dict()
        doors = dict()
        _keys = dict()
        rdoors = dict()
        r_keys = dict()
        me = None
        y = 0
        botid = 0
        for line in (l.strip() for l in f.readlines()):
            for x in range(0, len(line)):
                grid[(x,y)] = line[x]
                if line[x] == '@':
                    grid[(x,y)] = '.'
                    bots.append( Robot(botid, (x,y)) )
                    botid += 1
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
        for bot in bots:
            map_visible(grid, bot.coord, visible)
        botpos = {b.coord:b for b in bots}

        printg_curses(stdscr, grid, _max, botpos, rdoors, r_keys, dict(), visited, visible, 0)

        fullret = ['o', 'n', 'k', 'c', 'e', 'r', 'z', 'v', 'j', 'w', 'b', 'u', 'i', 'q', 't', 'y', 'h', 'x', 'd', 'f', 'm', 'a', 's', 'l', 'g', 'p']
        ret = [None] * 4

        ret[0] = ['r', 'j', 'i', 'q', 'd']
        ret[1] = ['e', 'z', 'v', 'y', 'x', 'p']
        ret[2] = ['o', 'c', 't', 'h', 'f']
        ret[3] = ['n', 'k', 'w', 'b', 'u', 'm', 'a', 's', 'l', 'g']

        for bot in bots:
            bot.memo = make_memo(_keys, doors, grid, _max, bot.coord, ret[bot.id])
        time.sleep(0.5)
        #stdscr.getch()

        last_k = ['@', '@', '@', '@']
        gotkeys = set()
        steps = 0
        for k in fullret:
            bot = None 
            for b in bots:
                if (last_k[b.id], k) in b.memo:
                    bot = b
                    break
            else:
                raise Exception('key path: {} {} {}'.format(k, bots, last_k))

            #bot.path.append(k)
            prev = bot.memo[(last_k[bot.id], k)][3]
            for p in reversed(prev):
                visited.add(p)
                botpos.pop(bot.coord)
                botpos[p] = bot
                bot.coord = p
                printg_curses(stdscr, grid, _max, botpos, rdoors, r_keys, gotkeys, visited, visible, steps)
                me = p
                steps += 1
                time.sleep(0.01)
            steps -= 1
            #time.sleep(0.1)
            gotkeys.add(k)
            rdoors.pop( doors[k.upper()] ) 
            grid[doors[k.upper()]] = '.'
            visible.clear()
            for b in bots:
                map_visible(grid, b.coord, visible)
            last_k[bot.id] = k
            printg_curses(stdscr, grid, _max, botpos, rdoors, r_keys, gotkeys, visited, visible, steps)
            #stdscr.getch()

        printg_curses(stdscr, grid, _max, botpos, rdoors, r_keys, gotkeys, visited, visible, steps, True)
        stdscr.getch()

wrapper(main)

"""
for b in bots:
    print(b.id, b.path)
    """