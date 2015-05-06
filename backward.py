import json
from heapq import heappush, heappop
from collections import namedtuple

with open("Crafting.json") as f:
	Crafting = json.load(f)
Items = Crafting['Items']

def inventory_to_tuple(d):
	inventory = tuple(int(d.get(name,0)) for i,name in enumerate(Items))
	return inventory

#def make_planer(rule):


Recipe = namedtuple('Recipe',['name','check','effect','cost'])
# print yes
#print (a.check)
#a = Recipe('peace', 'yes', None, 50)
all_recipes = [Crafting['Goal']]
#while 1:

goal = inventory_to_tuple(Crafting['Goal'])
j= 0
discRules = []
while 1:
	
	
	for name, rule in Crafting['Recipes'].items():
		if name not in discRules:
			produces = inventory_to_tuple(rule['Produces'])
			for i in xrange(len(goal)):
				if goal[i]  >0 and produces[i] > 0:
					#print name
					discRules.append(name)
					if rule.get('Requires')!= None:
						requires = inventory_to_tuple(rule['Requires'])
						for i in xrange(len(goal)):
							if requires[i] > 0 and goal[i] == 0:
								goal = tuple(goal[i]+requires[i] for i,amount in enumerate(goal))
					if rule.get('Consumes')!= None:
						consumes = inventory_to_tuple(rule['Consumes'])	
						goal = tuple(goal[i]+consumes[i] for i,amount in enumerate(goal)) 
		else:
			print 'here'
			print name
					#stop or not?
					#if name == 'punch for wood':
					#	break
						#print "goal"
						#print goal
						#print('consumes')
						#print inventory_to_tuple(rule['Consumes'])			
						#print inventory_to_tuple(rule['Requires'])

	#print discRules
	print goal
