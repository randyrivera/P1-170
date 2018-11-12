import networkx as nx
import collections
import os

# design solver

G = None
num_buses = 0
size_bus = 0 
constraints = []
total_capacity = 0
bus_index = 0
disjoint_sets = []
nodes_groups = {} #the rowdy groups each node belongs to

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list of vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []
    
    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints

def get_rowdy(node):
	'''
		Takes a node and returns a list of all the rowdy groups that contain it 

		Inputs:
			vertex - a string representing the name of a node in the graph
		Output:
			list - a list of list containing the rowdy groups the vertex belongs to
	'''
	rowdy_groups = []
	for constraint in constraints:
		if node in constraint:
			rowdy_groups.append(constraint)
	return rowdy_groups

def set_global_scope(folder_name):
	''' 
		Sets all global variables
	'''
	global G, num_buses, size_bus, constraints, total_capacity, disjoint_sets
	G, num_buses, size_bus, constraints = parse_input(folder_name)
	total_capacity = num_buses * size_bus
	nodes = list(G.nodes())
	i = 0
	while i < num_buses:
		disjoint_sets.append([])
		i += 1

def get_max_node(Graph):
	''' 
		Finds node with highest degree
		*** probably have to handle case when returnin empty list
	''' 
	if (len(Graph.nodes()) > 0):
		highest_degree = Graph.nodes()[0]
		for node in Graph.nodes():
			if G.degree(node) > G.degree(highest_degree):
				highest_degree = node
		return highest_degree
	return None

def get_min_adj(adj_node_lst):
	''' 
		Finds node adjacent node with lowest degree
		*** probably have to handle case when returnin empty list
	''' 
	if (len(adj_node_lst) > 0):
		lowest_degree = adj_node_lst[0]
		for node in adj_node_lst:
			if len(G.edges(node)) < len(G.edges(lowest_degree)):
				lowest_degree = node
		return lowest_degree
	return None	

def get_adjacent(current_node):
	''' 
		return string list of all adjacent vertices
		!!!works!!!
	'''

	return_vertices = []
	for edge in G.edges(current_node):
			if edge[0] == str(current_node):
				return_vertices.append(str(edge[1]))
			else:
				return_vertices.append(str(edge[0]))
	return return_vertices

def finisher():
	global G
	while(len(G.nodes()) > 0):
		current_node = G.nodes()[0]
		G.remove_node(current_node)
		for bus in disjoint_sets:
			if len(bus) < size_bus:
				bus.append(current_node)
				break

def	algo():
	global G #, adjacent_nodes
	current_node = get_max_node(G)
	adjacent_nodes = get_adjacent(current_node)
	adjacent_to_iter = adjacent_nodes
	current_min = get_min_adj(adjacent_to_iter)

	i = 0
	print("initial nodes: ", G.nodes(), "\n")
	print("size of bus is ", size_bus, "\n")
	while(len(G.nodes()) > 0 and i < num_buses): 
		while (len(adjacent_to_iter) > 0) and (len(disjoint_sets[i]) < size_bus - 1):

			print("current min adj: ", current_min)

			disjoint_sets[i].append(current_min)
			adjacent_to_iter.remove(current_min)
			current_min = get_min_adj(adjacent_to_iter)

		print("current max node: ", current_node)
		disjoint_sets[i].append(current_node)

		print("to be removed: ", disjoint_sets[i], "\n")

		for node in disjoint_sets[i]:
			G.remove_node(node)

		print("all nodes in G: ", G.nodes(), "\n")
	
		current_node = get_max_node(G)
		adjacent_nodes = get_adjacent(current_node)
		adjacent_to_iter = adjacent_nodes
		current_min = get_min_adj(adjacent_to_iter)		
		i += 1

	### break into seperate function that finishes matching leftover nodes
	
	[print("bus contains: ", bus) for bus in disjoint_sets]
	print("Nodes left: ", G.nodes(), "\n")
	finisher()
	print("Nodes left: ", G.nodes())
	[print("bus contains: ", bus) for bus in disjoint_sets]
		

set_global_scope("./inputs/small")

def write_solution(file_name):
	file = open("./outputs/" + file_name + ".out", "w")

	for bus in disjoint_sets:
		if len(bus) > 0:
			group = "["
			for node in bus:
				group += "'" + node + "', "
			file.write(group[:-2] + "]" + "\n")



def check_status():

	print("Number of students: ", len(G.nodes()))
	print("Number of buses: ", num_buses)
	print("Size of buses: ", size_bus)
	print("Total Capacity: ", total_capacity)
	print("Rowdy groups: ")
	for constraint in constraints:
		print(constraint)
    
    #return nx.write_gml(G, "test.gml")
