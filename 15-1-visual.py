import re
import sys
import json
import itertools
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

block = bytes([0xE2,0x96, 0x88])
def printg_curses(stdscr, g, d, _min, _max, deadends, oxy):
    sc_y = 1
    sc_x = 1
    stdscr.erase()
    for y in range(_min[1] - 1, _max[1] + 2):
        for x in range(_min[0] - 1, _max[0] + 2):
            c = (x,y)
            try:
                if c == oxy:
                    stdscr.insch(sc_y, sc_x, 'o', curses.color_pair(4) | curses.A_BOLD)
                elif c == d:
                    stdscr.insstr(sc_y, sc_x, block, curses.color_pair(1))
                elif c in deadends:
                    stdscr.insstr(sc_y, sc_x, block, curses.color_pair(2) | curses.A_DIM)
                elif c in g:
                    if g[c] == '#':
                        stdscr.insstr(sc_y, sc_x, block, curses.color_pair(0))
                    else:
                        stdscr.insstr(sc_y, sc_x, block, curses.color_pair(3) | curses.A_DIM)
                else:
                    stdscr.insch(sc_y, sc_x, ' ')
            except (curses.error):
                pass
            sc_x += 1
        sc_x = 1
        sc_y += 1
    stdscr.refresh()
    #time.sleep(0.01)

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

def _next(d, dir):
    n = xy_delta_map[dir]
    return (d[0] + n[0], d[1] + n[1])

def main(stdscr):

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
    deadends = set()
    _min = [0,0]
    _max = [0,0]
    d_pos = (0,0)
    oxy_pos = None
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

        printg_curses(stdscr, grid, d_pos, _min, _max, deadends, oxy_pos)

    for y in range(_min[1] - 1, _max[1] + 2):
        for x in range(_min[0] - 1, _max[0] + 2):
            if y == _min[1] - 1 or y == _max[1] + 1 or x == _max[0] + 1 or x == _min[0] - 1:
                grid[(x,y)] = '#'
            elif grid[(x,y)] == ' ':
                grid[(x,y)] = '#'

    printg_curses(stdscr, grid, d_pos, _min, _max, deadends, oxy_pos)
    stdscr.getch()

wrapper(main)