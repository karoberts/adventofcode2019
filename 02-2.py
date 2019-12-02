import re

with open('02.txt') as f:
    for line in (l.strip() for l in f):
        oops = [int(x) for x in line.split(',')]

        for a in range (0,100):
            for b in range (0,100):
                #print(a,b)
                p = 0
                ops = oops.copy()
                ops[1] = a
                ops[2] = b

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

                if ops[0] == 19690720:
                    print('part2', a, b, 100 * a + b)
                    exit()
                #print('got', ops[0])

        break
