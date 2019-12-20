import re
import sys
import json
import itertools
import math
import fractions
from typing import List, Dict, DefaultDict
from collections import defaultdict
sys.setrecursionlimit(5000)

class Chemical:
    def __init__(self, name:str, amount:int):
        self.name:str = name
        self.amount:int = amount

    def __repr__(self):
        return '/{} {}/'.format(self.amount, self.name)

class Recipe:
    def __init__(self, result:str, resultCount:int, inputs:List[Chemical]):
        self.output:Chemical = Chemical(result, resultCount)
        self.inputs:List[Chemical] = inputs.copy()

    def __repr__(self):
        return '({} from {})'.format(self.output, self.inputs)

def generate(recipes:Dict[str,Recipe], cur:str, amount:int, made:DefaultDict[str,int], depth:int):
    def get_min_amount(chemToMake:Chemical, toMakeRecipe:Recipe, amountMultiplier:int) -> int:
        amountNeeded:int = chemToMake.amount * amountMultiplier
        #print('min', chemToMake, toMakeRecipe, amountMultiplier)

        if amountNeeded < toMakeRecipe.output.amount:
            return toMakeRecipe.output.amount
        if amountNeeded % toMakeRecipe.output.amount == 0:
            return amountNeeded # // toMakeRecipe.output.amount
        return math.ceil(amountNeeded / toMakeRecipe.output.amount) * toMakeRecipe.output.amount

    def get_min_amount_ore(chemToMake:Chemical, toMakeRecipe:Recipe, amountToMake:int) -> int:
        if amountToMake < toMakeRecipe.output.amount:
            return toMakeRecipe.output.amount * chemToMake.amount
        if amountToMake % toMakeRecipe.output.amount == 0:
            return (amountToMake // toMakeRecipe.output.amount) * chemToMake.amount
        return math.ceil(amountToMake / toMakeRecipe.output.amount) * chemToMake.amount

    curRecipe = recipes[cur]

    print(' ' * depth, 'need to make', amount, 'of', cur, 'using', curRecipe)

    depth += 1
    inputChem:Chemical = None

    if curRecipe.inputs[0].name == 'ORE':
        min_amount:int = get_min_amount_ore(curRecipe.inputs[0], curRecipe, amount)
        print(' ' * depth, 'going to make', min_amount, 'ORE for', amount, 'of', cur, curRecipe.inputs[0])
        made['ORE.{}'.format(cur)] += min_amount
        made['ORE'] += min_amount
        return

    for inputChem in curRecipe.inputs:
        inputRecipe:Chemical = recipes[inputChem.name]
        min_amount:int = get_min_amount(inputChem, inputRecipe, amount)
        print(' ' * depth, 'making', min_amount, 'of', inputChem.name, 'using', inputRecipe)
        made[inputChem.name] += min_amount
        generate(recipes, inputChem.name, min_amount, made, depth + 1)

def findUsed(recipes:Dict[str,Recipe], cur:str, amount:int, made:DefaultDict[str,int], depth:int):
    def get_min_amount(chemToMake:Chemical, toMakeRecipe:Recipe, amountMultiplier:int) -> int:
        amountNeeded:int = chemToMake.amount * amountMultiplier
        #print('min', chemToMake, toMakeRecipe, amountMultiplier)
        return amountNeeded

    def get_min_amount_ore(chemToMake:Chemical, toMakeRecipe:Recipe, amountToMake:int) -> int:
        if amountToMake < toMakeRecipe.output.amount:
            return toMakeRecipe.output.amount * chemToMake.amount
        if amountToMake % toMakeRecipe.output.amount == 0:
            return (amountToMake // toMakeRecipe.output.amount) * chemToMake.amount
        return math.ceil(amountToMake / toMakeRecipe.output.amount) * chemToMake.amount

    curRecipe = recipes[cur]

    print(' ' * depth, 'need to make', amount, 'of', cur, 'using', curRecipe)

    depth += 1
    inputChem:Chemical = None

    if curRecipe.inputs[0].name == 'ORE':
        min_amount:int = get_min_amount_ore(curRecipe.inputs[0], curRecipe, amount)
        print(' ' * depth, 'going to make', min_amount, 'ORE for', amount, 'of', cur, curRecipe.inputs[0])
        made['ORE.{}'.format(cur)] -= min_amount
        return

    for inputChem in curRecipe.inputs:
        inputRecipe:Chemical = recipes[inputChem.name]
        min_amount:int = get_min_amount(inputChem, inputRecipe, amount)
        print(' ' * depth, 'making', min_amount, 'of', inputChem.name, 'using', inputRecipe)
        made[inputChem.name] -= min_amount
        findUsed(recipes, inputChem.name, min_amount, made, depth + 1)

with open('14-test3.txt') as f:

    recipes:Dict[str,Recipe] = {}
    ore_recipes:Dict[str,Recipe] = {}
    made:defaultdict = defaultdict(lambda:0)

    for line in (l.strip() for l in f.readlines()):
        sides = line.split(' => ')
        m = sides[1].split(' ')
        inputs = []
        for x in sides[0].split(', '):
            inp = x.split(' ')
            inputs.append(Chemical(inp[1], int(inp[0])))
            if inp[1] == 'ORE':
                ore_recipes[m[1]] = Recipe(m[1], int(m[0]), [Chemical('ORE', int(inp[0]))])

            recipes[m[1]] = Recipe(m[1], int(m[0]), inputs)

    print(recipes) 
    print(ore_recipes) 
    print()
    print('made',made)
    print()

    generate(recipes, 'FUEL', 1, made, 0)

    print('made',made)
    print()

    findUsed(recipes, 'FUEL', 1, made, 0)

    print()
    print('made',made)
    print()

    chemName:str = None
    amtMade:int = None
    for chemName, amtMade in made.items():
        if amtMade == 0: continue
        if chemName[0:3] == 'ORE': continue
        print('made', amtMade, 'too many of', chemName)
        recipe = recipes[chemName]
        if amtMade < recipe.output.amount:
            print('  can\'t reduce')
            continue
        print('  recipe', recipe)
        print('  can reduce')
        reduced:int = 0
        while amtMade >= recipe.output.amount:
            print('  reducing', recipe.output.amount, 'of', chemName)
            amtMade -= recipe.output.amount
            reduced += recipe.output.amount
        print('  left with', amtMade, 'of', chemName)

        if recipe.inputs[0].name == 'ORE':
            made['ORE'] -= (reduced // recipe.output.amount) * recipe.inputs[0].amount

    print()
    print('made',made)
    print()

    print('part1', made['ORE'])