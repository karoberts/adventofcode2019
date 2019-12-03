import re

def manhat_dist(x,y):
    return abs(x) + abs(y)

def key(x,y):
    return str(x) + ',' + str(y)

board = dict()
mindist = 999999999

def run(line, inters, stb, step, ck):
    global mindist
    global board
    px = 0
    py = 0
    for p in line:
        dx = 0
        dy = 0
        if p[0] == 'R': dx = 1
        elif p[0] == 'L': dx = -1
        elif p[0] == 'U': dy = -1
        elif p[0] == 'D': dy = 1

        mag = int(p[1:])
        for i in range(0, mag):
            k = key(px, py)
            if ck and k != '0,0' and k in board:
                inters.append(k)
            if not ck:
                board[k] = 1
            stb[k] = step
            step += 1
            px += dx
            py += dy


with open('03.txt') as f:
    line1 = f.readline().strip().split(',')
    line2 = f.readline().strip().split(',')

    #line1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'.split(',')
    #line2 = 'U62,R66,U55,R34,D71,R55,D58,R83'.split(',')
    #line1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(',')
    #line2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(',')

    inters = []
    b1 = dict()
    b2 = dict()

    run(line1, inters, b1, 0, False)
    run(line2, inters, b2, 0, True)

    #print(inters)
    #print(b1)
    #print(b2)
    #print(mindist)

    min_steps = 99999999999
    for i in inters:
        steps = b1[i] + b2[i]
        if steps < min_steps:
            min_steps = steps
    print(min_steps)
