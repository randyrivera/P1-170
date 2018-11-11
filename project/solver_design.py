import networkx as nx
import collections
import os

# design solver

G = None
num_buses = 0
size_bus = 0 
constraints = []
total_capacity = 0
disjoint_sets = {}
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
		key_string = "bus#" + str(i)
		print(nodes[i])
		nodes_groups[nodes[i]] = get_rowdy(str(i))
		disjoint_sets[key_string] = []
		i += 1

def check_status():

	print("Number of students: ", len(G.nodes()))
	print("Number of buses: ", num_buses)
	print("Size of buses: ", size_bus)
	print("Total Capacity: ", total_capacity)
	print("Rowdy groups: ")
	for constraint in constraints:
		print(constraint)
    
    #return nx.write_gml(G, "test.gml")
