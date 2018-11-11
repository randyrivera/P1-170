import networkx as nx
import os

G = nx.Graph()
nodes = [str(x) for x in range(10)]
G.add_nodes_from(nodes)

G.add_edge('1', '2')
G.add_edge('1', '3')
G.add_edge('3', '5')
G.add_edge('8', '9')

print("Number of Edges: ", G.number_of_edges())
print("Number of Nodes: ", G.number_of_nodes())

nx.write_gml(G, "test.gml")
