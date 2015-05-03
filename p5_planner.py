import json
from collections import namedtuple

with open("Crafting.json") as f:
	Crafting = json.load(f)
#print Crafting['Items']
#print Crafting['Initial']
#print Crafting['Goal']
check = None

def make_checker(rule):

	def check(state):
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

def graph(state):
	for r in all_recipes:
		if r.check(state):
			yield (r.name, r.effect(state), r.cost)

def is_goal(state):
	return True
	#return state == 'goal'

def heuristic(state):
	return 0


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
#print( all_recipes)

def search(graph, initial, is_goal, limit, heuristic):


	return total_cost, plan
print(search())

