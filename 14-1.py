import re
import sys
import json
import itertools
import math
import fractions
from collections import defaultdict
sys.setrecursionlimit(5000)

class Chemical:
    def __init__(self, name:str, amount:int):
        self.name:str = name
        self.amount:int = amount

    def __repr__(self):
        return '{} {}'.format(self.amount, self.name)

class Recipe:
    def __init__(self, result:str, resultCount:int, inputs:list):
        self.output:Chemical = Chemical(result, resultCount)
        self.inputs:dict = inputs.copy()

    def __repr__(self):
        return '{} from {}'.format(self.output, self.inputs)



with open('14-test2.txt') as f:

    recipes:dict = {}
    ore_recipes:dict = {}

    for line in (l.strip() for l in f.readlines()):
        sides = line.split(' => ')
        made = sides[1].split(' ')
        inputs = []
        for x in sides[0].split(', '):
            inp = x.split(' ')
            inputs.append(Chemical(inp[1], int(inp[0])))
            if inp[1] == 'ORE':
                ore_recipes[made[1]] = Recipe(made[1], int(made[0]), [Chemical('ORE', int(inp[0]))])

            recipes[made[1]] = Recipe(made[1], int(made[0]), inputs)

        #tomake[made[1]] = int(made[0])
        #prod[made[1]] = {'c':int(made[0]), 'i': inputs}

    print(recipes) 
    print(ore_recipes) 
