from heapq import heappush, heappop
t_initial = 'a'
t_limit = 20
edges = {'a': {'c':3, 'b':5}, 'b':{'d':5, 'c':1 }, 'c':{'d':1, 'b':1}}
def t_graph(state):
	for next_state, cost in edges[state].items():
		yield ((state,next_state), next_state, cost)

def t_is_goal(state):
	return state == 'b'

def t_heuristic(state):
	return 0

def search(graph, initial, is_goal, limit, heuristic):
	cost_so_far = {}
	prev = {}
	queue = []
	new_cost = 0.0
	state = initial
	cost_so_far[state] = 0.0
	prev[state] = None
	heappush(queue,(0, state))
	goalQueue = []

	#discState = heappop(queue)
	#print discState
	while queue:
		discState = heappop(queue)
		if is_goal(discState[1]):
			#heappush(goalQueue,(discState[0], discState[1]))
			print ('here')
			break
		for i in graph(discState[1]):
			print i
			new_cost = cost_so_far[discState[1]] + i[2]
			if i[1] not in cost_so_far or new_cost < cost_so_far[i[1]]:
				cost_so_far[i[1]] = new_cost
				total_cost = new_cost
				heappush(queue,(total_cost, i[1]))
				prev[i[1]] = discState[1]
	node = discState[1]
	while node != initial:
		goalQueue.append(node)
		node = prev[node]
	goalQueue.append(initial)
	goalQueue.reverse()
	return discState, goalQueue
	#plan = goalQueue
	#print plan

	#print graph('a').next()
	#print next(graph('a'))

	#return total_cost, plan
print search(t_graph, t_initial, t_is_goal, t_limit, t_heuristic)
#print t_graph('a').next()
#print t_graph('b').next()