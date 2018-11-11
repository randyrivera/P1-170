import networkx as nx
import random
import os

### Creates new Inputs and Parameters ###


def create_graph(num_nodes, num_edges, file_name):
	''' 
		Creates a new graph with num_nodes number of nodes, 
		num_edges number of edges, and writes it to ./inputs/filname
	'''
	G = nx.Graph()
	G.add_nodes_from([str(x) for x in range(num_nodes)])
	while num_edges > 0:
		node_u = str(random.randrange(num_nodes))
		node_v = str(random.randrange(num_nodes))

		if not (G.has_edge(node_u, node_v)):
			G.add_edge(node_u, node_v)
			num_edges -= 1
	#print("./inputs/" + file_name)
	path = "./inputs/" + file_name + "/graph.gml"		
	nx.write_gml(G, path)

def random_constraints(num_nodes):
	'''
		creates a string of random ass constraints for stuff
	'''
	constraint = "["
	rowdy_size = random.randrange(2, 6)

	while rowdy_size > 0:
		node = ("'" + str(random.randrange(num_nodes)) + "', ")
		if node not in constraint:
			constraint += node

			rowdy_size -=1

	return constraint[:-2] + "]"

def create_parameters(num_buses, bus_capacity, num_nodes, num_constraints, file_name):
	'''
		Creates new parameter.txt file with number of buses, the capacity 
		of the buses, and random restraints.
	'''
	file = open("./inputs/" + file_name + "/parameters.txt", "w")

	file.write(str(num_buses) + "\n")
	file.write(str(bus_capacity))

	constraint_lst = []
	while num_constraints > 0:
		constraint = random_constraints(num_nodes)
		if constraint not in constraint_lst:
			constraint_lst.append(constraint)
			file.write("\n" + constraint)
			num_constraints -= 1
