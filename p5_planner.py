import json
from heapq import heappush, heappop
from collections import namedtuple
limit = 32

with open("Crafting.json") as f:
	Crafting = json.load(f)
#with open("Plutonium.json") as f:
	#Crafting = json.load(f)
#print Crafting['Items']
#print Crafting['Initial']

Items = Crafting['Items']
check = None
counter = 0

def inventory_to_tuple(d):
	inventory = tuple(int(d.get(name,0)) for i,name in enumerate(Items))
	return inventory

def make_checker(rule):
	def check(state):
		checker = True
		if rule.get('Requires')!= None:
			inventory = inventory_to_tuple(rule['Requires'])
			for i in xrange(len(state)):
				if inventory[i] != 0:
					if inventory[i] > state[i]:
						return False
					else:
						checker = True
		if rule.get('Consumes')!= None:
			consumes = inventory_to_tuple(rule['Consumes'])
			for i in xrange(len(state)):
				if consumes[i] != 0:
					if consumes[i] > state[i]:
						return False
					else:
						checker = True
		return checker
	return check

def make_effector(rule):
	def effect(state):
		produces = inventory_to_tuple(rule['Produces'])
		if rule.get('Consumes')!= None:
			consumes = inventory_to_tuple(rule['Consumes'])
			tempState = tuple(state[i]-consumes[i] for i,amount in enumerate(state))
			next_state = tuple(tempState[i]+produces[i] for i,amount in enumerate(state))
		else:
			next_state = tuple(state[i]+produces[i] for i,amount in enumerate(state))
		return next_state
	return effect

def graph(state):
	for r in all_recipes:
		if r.check(state):
			yield (r.name, r.effect(state), r.cost)


def is_goal(state):
	goal = Crafting['Goal']
	mygoal = inventory_to_tuple(goal)
	for i in xrange(len(state)):
		if mygoal[i] != 0:
			if state[i] < mygoal[i]:
				return False
	return True

def backWard():
	j= 0
	goal = inventory_to_tuple(Crafting['Goal'])
	discRules = []
	while j < 4:
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

		#print discRules
		j +=1
	return goal

backward_map = backWard()
#print backward_map


def heuristic(backward_map, state, nextState):
	#print backward_map
	#print backward_map[1]
	#print state
	#print 'nextState:'
	#print nextState
	good = False
	counter = 0
	
	for i in xrange(len(state)):
	#	if state[i] == 0 and nextState[i] > 0:
		if state[i] < nextState[i]:
			good = True
	if good == False:
		counter += 2
	if nextState[7] == 1:
		counter -= 20
	if nextState[16] == 1:
		counter -= 100
	if nextState[13] == 1:
		counter -= 100
	if nextState[3] > 0:
		counter += 200

	if nextState[0] > 1 or nextState[1] > 1 or nextState[2] > 1 or nextState[3] > 8 or nextState[4] > 1 or nextState[5] > 6 or nextState[6] > 1 or nextState[7] > 1 or nextState[8] > 1 or nextState[9] > 6 or nextState[11] > 4 or nextState[12] > 1 or nextState[13] > 1  or nextState[14] > 1 or nextState[15] > 1  or nextState[16] > 1 :
		counter += float('inf')
	#if nextState[0] > backward_map[0] or nextState[1] > backward_map[1] or nextState[2] > backward_map[2] or nextState[3] > backward_map[3] or nextState[4] > backward_map[4] or nextState[5] > backward_map[5] or nextState[6] > backward_map[6] or nextState[7] > backward_map[7] or nextState[8] > backward_map[8] or nextState[9] > backward_map[9] or nextState[11] > backward_map[11] or nextState[12] > backward_map[12] or nextState[13] > backward_map[13]  or nextState[14] > backward_map[14] or nextState[15] > backward_map[15] or nextState[16] > backward_map[16] :
	#	counter += float('inf')	
	return counter

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
#print(all_recipes)

initial = Crafting['Initial']
def search(graph, initial, is_goal, limit, heuristic):
	#state = inventory_to_tuple(initial)
	#print graph(state).next()
	cost_so_far = {}
	prev = {}
	steps = {}

	queue = []
	new_cost = 0.0
	priortiy  = 0.0
	state = inventory_to_tuple(initial)
	steps[state] = 'start_state'
	cost_so_far[state] = 0.0
	prev[state] = None
	heappush(queue,(0,0, state))
	goalQueue = []

	#discState = heappop(queue)
	#print discState
	while queue:
		discState = heappop(queue)
		if is_goal(discState[2]):
			#heappush(goalQueue,(discState[0], discState[1]))
			#print ('here')
			break
		for i in graph(discState[2]):
			#print i
			new_cost = cost_so_far[discState[2]] + i[2]
			if i[1] not in cost_so_far or new_cost < cost_so_far[i[1]]:
				cost_so_far[i[1]] = new_cost
				total_cost = new_cost
				priority = new_cost + heuristic(backward_map, discState[2], i[1])
				prev[i[1]] = discState[2]
				steps[i[1]] = i[0]
				#print priority
				heappush(queue,(priority,total_cost, i[1]))
	node = discState[2]
	counter = 0
	while node != None:
		counter += 1
		goalQueue.append(steps[node])
		node = prev[node]
	#goalQueue.append(initial)
	goalQueue.reverse()
	return discState[1], goalQueue, counter-1

#print search(graph, initial, is_goal, limit, heuristic)

cost,path,leng = search(graph, initial, is_goal, limit, heuristic)
print 'Achieve' + str(Crafting['Goal'])
print ('cost=' + str(cost) + ', len=' +str(leng))
print 'path: '
print path





