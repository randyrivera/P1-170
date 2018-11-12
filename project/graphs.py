import networkx as nx
import os

def makeCenter(k):
    S = nx.complete_graph(k)
    for i in range(k):
        S.add_nodes_from([k, k + 1, k + 2, k + 3])
        S.add_edges_from([(i, k), (i, k + 1), (i, k + 2), (i, k + 3)])
        k += 4
    return S

def makeOuter(k):
    S = nx.complete_graph(k)
    return S

def makeComplete(input_size):
    if input_size == 'small':
        k = 5
        adder = 25
    elif input_size == 'medium':
        k = 50
        adder = 250
    elif input_size == 'large':
        k = 100
        adder = 500

    center = makeCenter(k)
    for i in range(5):
        outer = makeOuter(k)
        nx.relabel_nodes(outer, lambda x: x + adder, False)
        center.add_nodes_from(outer.nodes)
        center.add_edges_from(outer.edges)
        center.add_edge(i, adder + (i * k))
        adder += k

    nx.relabel(center, lambda x: str(x), False)
    return center
