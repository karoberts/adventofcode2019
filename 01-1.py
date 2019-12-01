
s = 0
with open('01.txt') as f:
    for line in f:
        num = int(line)
        mass = (num // 3) - 2
        s += mass
        print(num, mass, s)
        pass

print(s)
