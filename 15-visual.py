import re
import sys
import json
import itertools
import heapq
import curses
import time
from curses import wrapper
from collections import defaultdict
sys.setrecursionlimit(5000)

#ctx {'p': 0, 'pi':0, 'rb':0 'i':[i]})
def run_prog(ops, ctx, inp):
    modes = {0: 'POS', 1:'IMM', 2:'REL'}

    def readv(ops, p, offs, rb):
        if offs == 1: mode = modes[(ops[p] % 1000) // 100]
        elif offs == 2: mode = modes[(ops[p] % 10000) // 1000]
        elif offs == 3: mode = modes[(ops[p] % 100000) // 10000]
        #print('r', p, mode, ops[p], ops[p + offs])
        if mode == 'IMM': return ops[p + offs]
        elif mode == 'POS': return ops[ops[p + offs]]
        elif mode == 'REL': return ops[ops[p + offs] + rb]

    def writev(ops, p, offs, rb, v):
        if offs == 1: mode = modes[(ops[p] % 1000) // 100]
        elif offs == 2: mode = modes[(ops[p] % 10000) // 1000]
        elif offs == 3: mode = modes[(ops[p] % 100000) // 10000]
        #print('r', p, mode, ops[p], ops[p + offs])
        if mode == 'POS': ops[ops[p + offs]] = v
        elif mode == 'REL': ops[ops[p + offs] + rb] = v

    ops_size = {1:4, 2:4, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:2, 99:0}
    output = False
    while True:
        opcode = ops[ctx['p']] % 100
        inc_p = True
        if opcode == 1:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            v2 = readv(ops, ctx['p'], 2, ctx['rb'])
            writev(ops, ctx['p'], 3, ctx['rb'], v1 + v2)
            if output: print('add', v1, v2, ops[ctx['p']+3])
            pass
        elif opcode == 2:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            v2 = readv(ops, ctx['p'], 2, ctx['rb'])
            writev(ops, ctx['p'], 3, ctx['rb'], v1 * v2)
            if output: print('mul', v1, v2, ops[ctx['p']+3])
            pass
        elif opcode == 3:
            v = inp[ctx['pi']]
            ctx['pi'] += 1
            writev(ops, ctx['p'], 1, ctx['rb'], v)
            if output: print('inp', ops[ctx['p']+1], v)
            pass
        elif opcode == 4:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            if output: print('output:', v1)
            ctx['p'] += ops_size[opcode]
            return v1
            pass
        elif opcode == 5:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            if v1 != 0:
                ctx['p'] = readv(ops, ctx['p'], 2, ctx['rb'])
                if output: print('jumpnz', ctx['p'])
                inc_p = False
            else:
                if output: print('nojumpnz', v1)
            pass
        elif opcode == 6:
            if readv(ops, ctx['p'], 1, ctx['rb']) == 0:
                ctx['p'] = readv(ops, ctx['p'], 2, ctx['rb'])
                if output: print('jumpz', ctx['p'])
                inc_p = False
            else:
                if output: print('nojumpz')
            pass
        elif opcode == 7:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            v2 = readv(ops, ctx['p'], 2, ctx['rb'])
            writev(ops, ctx['p'], 3, ctx['rb'], 1 if v1 < v2 else 0)
            if output: print('lt', v1, v2, ops[ctx['p']+3])
            pass
        elif opcode == 8:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            v2 = readv(ops, ctx['p'], 2, ctx['rb'])
            writev(ops, ctx['p'], 3, ctx['rb'], 1 if v1 == v2 else 0)
            if output: print('eq', v1, v2, ops[ctx['p']+3])
            pass
        elif opcode == 9:
            v1 = readv(ops, ctx['p'], 1, ctx['rb'])
            ctx['rb'] += v1
            if output: print('relbase', v1)
            pass
        elif opcode == 99:
            if output: print('HALT')
            return None

        if inc_p:
            ctx['p'] += ops_size[opcode]

_min = [0,0]
_max = [0,0]
oxy_pos = None
deadends = set()
steps_to_oxy = set()

def dijkstra_findoxy(me:tuple, oxy:tuple, grid:dict):
    global deadends

    tests = [ (1, 0), (-1, 0), (0, -1), (0, 1) ]
    def get_neighbors(x,y):
        k = (x,y)
        c = grid[k]
        ns = []

        for t in tests:
            tx = x + t[0]
            ty = y + t[1]
            tk = (tx, ty)
            tt = grid[tk]

            if tk in deadends or tt == '.':
                ns.append( [1, tx, ty, tk, True] )

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

    while len(h) > 0:
        u = heapq.heappop(h)
        if not u[4]:
            continue
        inq.remove(u[3])
        uk = u[3]
        for v in get_neighbors(u[1], u[2]):
            alt = dist[uk] + v[0]
            if alt < dist[v[3]]:
                dist[v[3]] = alt
                prev[v[3]] = (uk, v[0], v[1], v[2])
                entry = [alt, v[1], v[2], v[3], True]
                if v[3] in inq:
                    finder[v[3]][4] = False
                inq.add(v[3])
                finder[v[3]] = entry

                if v[3] == oxy:
                    return prev

                heapq.heappush(h, entry)

    return None

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

MODE_EXPLORE = 0
MODE_FIND_OXY = 1
MODE_OXY = 2
MODE_DONE = 3

block = bytes([0xE2,0x96, 0x88,0xE2,0x96,0x88])
def printg_curses(stdscr, g, d, mode, steps = None, minutes = None):
    global oxy_pos, deadends, _min, _max, steps_to_oxy

    sc_y = 0
    sc_x = 0
    stdscr.erase()
    for y in range(_min[1] - 1, _max[1] + 2):
        for x in range(_min[0] - 1, _max[0] + 2):
            c = (x,y)
            if c == oxy_pos:
                stdscr.addstr(sc_y, sc_x, block, curses.color_pair(4) | curses.A_BOLD)
            elif c == d:
                stdscr.addstr(sc_y, sc_x, block, curses.color_pair(1))
            elif g[c] == 'O':
                stdscr.addstr(sc_y, sc_x, block, curses.color_pair(2))
            elif c in steps_to_oxy:
                stdscr.addstr(sc_y, sc_x, block, curses.color_pair(4) | curses.A_DIM)
            elif c in deadends:
                stdscr.addstr(sc_y, sc_x, block, curses.color_pair(2) | curses.A_DIM)
            elif c in g:
                if g[c] == '#':
                    stdscr.addstr(sc_y, sc_x, block, curses.color_pair(0))
                elif g[c] == '.':
                    stdscr.addstr(sc_y, sc_x, block, curses.color_pair(3) | curses.A_DIM)
            sc_x += 2
        sc_x = 0
        sc_y += 1

    sc_x = (_max[0] - _min[0] + 2) * 2
    if mode == MODE_EXPLORE:
        stdscr.addstr(1, sc_x + 5, 'Exploring...')
    if mode == MODE_FIND_OXY:
        stdscr.addstr(1, sc_x + 5, 'Finding Oxygen...')
    elif mode == MODE_OXY:
        stdscr.addstr(1, sc_x + 5, 'Filling...')
    elif mode == MODE_DONE:
        stdscr.addstr(1, sc_x + 5, 'Done, press enter to exit')

    if mode > MODE_EXPLORE:
        stdscr.addstr(3, sc_x + 5, 'Steps: ' + str(steps))
    if mode > MODE_FIND_OXY:
        stdscr.addstr(5, sc_x + 5, 'Minutes: ' + str(minutes))

    stdscr.refresh()

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

HITWALL = 0
MOVED = 1
ATOXY = 2

oppo = {NORTH:SOUTH, WEST:EAST, EAST:WEST, SOUTH:NORTH}
nextdir = {NORTH:WEST, WEST:SOUTH, SOUTH:EAST, EAST:NORTH}

xy_delta_map = {NORTH:(0,-1), SOUTH:(0,1), WEST:(-1,0),EAST:(1,0)}
dirs_to_try = {NORTH: [NORTH, EAST, SOUTH, WEST], EAST: [EAST, SOUTH, WEST, NORTH], SOUTH: [SOUTH, WEST, NORTH, EAST], WEST: [WEST, NORTH, EAST, SOUTH]}

steps = 0
minutes = 0

def _next(d, dir):
    n = xy_delta_map[dir]
    return (d[0] + n[0], d[1] + n[1])

def oxy_flood(stdscr, grid:dict):
    global oxy_pos, deadends, _min, _max, minutes, steps

    max_min = minutes
    q = [(oxy_pos,0)]
    last_depth = 0
    while len(q) > 0:
        pos = q.pop(0)
        max_min = max(max_min, pos[1])

        for dir in range(1, 4+1):
            npos = _next(pos[0], dir)
            g = grid[npos]
            if npos in deadends:
                grid[npos] = 'O'
                deadends.remove(npos)
                q.append((npos, pos[1] + 1))

        if pos[1] > last_depth:
            last_depth = pos[1]
            printg_curses(stdscr, grid, None, MODE_OXY, steps, max_min)
        time.sleep(0.02)
    minutes = max_min

def main(stdscr):
    global oxy_pos, deadends, _min, _max, steps, minutes, steps_to_oxy

    # Clear screen
    stdscr.clear()
    curses.curs_set(0)
    stdscr.refresh()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    ops = defaultdict(lambda:0)
    with open('15.txt') as f:
        i = 0
        for x in f.readline().strip().split(','):
            ops[i] = int(x)
            i += 1

    dir = NORTH
    inp = [dir]
    ctx =  {'p': 0, 'pi':0, 'rb':0}

    blocks = 0
    grid = defaultdict(lambda:' ')
    d_pos = (0,0)
    grid[d_pos] = '.'

    while dir is not None:
        r = run_prog(ops, ctx, inp)

        new_pos = _next(d_pos, dir)
        if r == HITWALL:
            grid[new_pos] = '#'
        elif r == MOVED:
            grid[new_pos] = '.'
            d_pos = new_pos
        elif r == ATOXY:
            oxy_pos = new_pos
            grid[new_pos] = 'o'
            d_pos = new_pos

        opts = {}
        for next_dir in dirs_to_try[dir]:
            next_pos = _next(d_pos, next_dir)
            opts[next_dir] = grid[next_pos]
            if opts[next_dir] == ' ':
                inp.append(next_dir)
                r = run_prog(ops, ctx, inp)
                if r == HITWALL:
                    grid[next_pos] = '#'
                else:
                    inp.append(oppo[next_dir])
                    run_prog(ops, ctx, inp)

        for next_dir in dirs_to_try[dir]:
            if opts[next_dir] == ' ':
                dir = next_dir
                break
        else:
            for next_dir in dirs_to_try[dir]:
                if opts[next_dir] == '.':
                    dir = next_dir
                    break
            else:
                dir = None

        if sum(1 for x in opts.values() if x == '#') == 3:
            deadends.add(d_pos)
            grid[d_pos] = '#'

        inp.append(dir)

        if d_pos[0] < _min[0]: _min[0] = d_pos[0]
        if d_pos[1] < _min[1]: _min[1] = d_pos[1]
        if d_pos[0] > _max[0]: _max[0] = d_pos[0]
        if d_pos[1] > _max[1]: _max[1] = d_pos[1]

        printg_curses(stdscr, grid, d_pos, MODE_EXPLORE)
        time.sleep(0.005)

    for y in range(_min[1] - 1, _max[1] + 2):
        for x in range(_min[0] - 1, _max[0] + 2):
            if y == _min[1] - 1 or y == _max[1] + 1 or x == _max[0] + 1 or x == _min[0] - 1:
                grid[(x,y)] = '#'
            elif grid[(x,y)] == ' ':
                grid[(x,y)] = '#'
    grid[d_pos] = '#'
    deadends.add(d_pos)

    printg_curses(stdscr, grid, d_pos, MODE_FIND_OXY, steps, minutes)

    prev = dijkstra_findoxy((0,0), oxy_pos, grid)
    p = prev[oxy_pos][0]
    path = [p]
    while p != (0,0):
        p = prev[p][0]
        path.append(p)
    
    for p in reversed(path):
        steps_to_oxy.add(p)
        steps += 1
        printg_curses(stdscr, grid, p, MODE_FIND_OXY, steps, minutes)
        time.sleep(0.02)
    
    #steps_to_oxy.clear()

    #stdscr.getch()
    time.sleep(1.0)

    oxy_flood(stdscr, grid)

    printg_curses(stdscr, grid, None, MODE_DONE, steps, minutes)
    stdscr.getch()

wrapper(main)