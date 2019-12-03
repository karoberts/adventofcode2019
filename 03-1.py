import re

def manhat_dist(x,y):
    return abs(x) + abs(y)

def key(x,y):
    return str(x) + ',' + str(y)

board = dict()
mindist = 999999999

def run(line, inters):
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
            if k != '0,0' and k in board:
                d = manhat_dist(px,py)
                inters.append((px, py, d))
                if d < mindist:
                    mindist = d
            board[k] = 1
            px += dx
            py += dy


with open('03.txt') as f:
    line1 = f.readline().strip().split(',')
    line2 = f.readline().strip().split(',')

    inters = []

    run(line1, inters)
    run(line2, inters)

    #print(inters)
    print(mindist)
