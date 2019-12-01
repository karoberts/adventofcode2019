
s = 0
with open('01.txt') as f:
    for line in f:
        num = int(line)
        mass = (num // 3) - 2
        while mass > 0:
            s += mass
            mass = (mass // 3) - 2
        pass

print(s)