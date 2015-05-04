import json
from heapq import heappush, heappop
from collections import namedtuple

with open("Crafting.json") as f:
	Crafting = json.load(f)

Items = Crafting['Items']
check = None

def make_checker(rule):
	def check(state):
		#if rule['Requires']
		#print(rule['Consumes'])
		return True
		#else 
		#return False
	return True

def make_effector(rule):
	def effect(state):
		#return next_state
		return state
	return check

def inventory_to_tuple(d):
	inventory = tuple(int(d.get(name,0)) for i,name in enumerate(Items))
	return inventory

goal = Crafting['Goal']
initial = Crafting['Initial']
print inventory_to_tuple(goal)
print inventory_to_tuple(initial)
#return state == inventory_to_tuple(goal)

Recipe = namedtuple('Recipe',['name','check','effect','cost'])
# print yes
#print (a.check)
#a = Recipe('peace', 'yes', None, 50)
all_recipes = []
for name, rule in Crafting['Recipes'].items():
	checker = make_checker(rule)
	effector = make_effector(rule)
	recipe = Recipe(name, checker, effector, rule['Time'])
	all_recipes.append(recipe)
	
print inventory_to_tuple(rule['Requires'])
#print(all_recipes)