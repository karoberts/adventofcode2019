import re

with open('02.txt') as f:
    for line in (l.strip() for l in f):
        ops = [int(x) for x in line.split(',')]
        p = 0

        # part 1
        ops[1] = 12
        ops[2] = 2

        while True:
            if ops[p] == 1:
                ops[ops[p+3]] = ops[ops[p+1]] + ops[ops[p+2]]
                pass
            elif ops[p] == 2:
                ops[ops[p+3]] = ops[ops[p+1]] * ops[ops[p+2]]
                pass
            elif ops[p] == 99:
                break
            p += 4

        print('part1', ops[0])

        break
