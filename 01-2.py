
masses = []
s = 0
with open('01.txt') as f:
    for line in f:
        num = int(line)
        mass = (num // 3) - 2
        masses.append(mass)
        s += mass
        pass

while True:
    nonzero = 0
    nmasses = []
    for m in masses:
        nm = (m // 3) - 2
        if nm > 0:
            s += nm
            nmasses.append(nm)
            nonzero += 1
    masses = nmasses
    if nonzero == 0:
        break

print(s)