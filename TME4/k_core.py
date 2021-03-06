import sys
import time
from math import inf, isinf
from TME3.graph import load_graph, makeAdjArray
import networkx as nx


def order_nodes_degree(graph):
    # number of nodes
    n = len(graph.nodes)
    # degrees[i] == (i, degree_node_i)
    degrees = list(nx.degree(graph))
    # (i, degree_node_i)
    max_degree = tuple(map(max, zip(*degrees)))[1]
    # sort nodes, by degree of each node
    sorted_node = [node for (node, degree) in sorted(degrees, key=lambda t:t[1])]

    # indexes where each degree section starts
    start_degrees_index = list(range(max_degree + 1))
    # location of each node in sorted_node
    node_index = list(range(n))

    # a 2-dimension array (dictionary in python) to represent the nodes having a same degree
    ordered_nodes = {i:[] for i in range(max_degree + 1)}

    for node in range(n):
        d = degrees[node][1]
        ordered_nodes[d].append(node)
    index = 0
    for d in range(max_degree + 1):
        start_degrees_index[d] = index
        for node in ordered_nodes[d]:
            node_index[node] = index
            index += 1
    return degrees, sorted_node, start_degrees_index, node_index


def core_decomposition(graph):
    """
    core decomposition of a graph
    :param graph: a networkx.Graph
    :return: a core value of graph
    """
    # core value
    c = 0
    # nodes
    nodes = list(graph.nodes)
    n = len(nodes)
    # core of each node, initialised to 0
    nodes_core = [(i, 0) for i in nodes]
    degrees, sorted_nodes, start_degrees_index, node_index = order_nodes_degree(graph)
    time_start = time.time()
    # reverse order of visiting each node
    ord = list(range(n))
    print("Calculating core decomposition...")
    for i in range(n):
        u = sorted_nodes[i]
        u_degree = degrees[u][1]
        ord[u] = n-i
        visited_neighbour = False
        if u_degree > c:
            c = u_degree
        nodes_core[u] = (u, c)
        # remove node u from graph: set degree of node u to inf so not to be considered anymore
        degrees[u] = (u, float(inf))
        # iterate its neighbours to decrease their degree
        neighbours = list(graph.neighbors(u))
        for v in neighbours:
            v_degree = degrees[v][1]
            # consider only nodes with degree != inf
            if not isinf(v_degree):
                # as u is deleted, v's degree will decrease by 1
                degrees[v] = (v, v_degree - 1)
                if i < start_degrees_index[v_degree]:
                    a = start_degrees_index[v_degree]
                    b = node_index[v]
                    # swap the head of section with a
                    sorted_nodes[a], sorted_nodes[b] = sorted_nodes[b], sorted_nodes[a]
                    node_index[sorted_nodes[a]], node_index[sorted_nodes[b]] = node_index[sorted_nodes[b]], node_index[sorted_nodes[a]]
                    start_degrees_index[v_degree] += 1
                    if not visited_neighbour:
                        start_degrees_index[u_degree] += 1
                else:
                    a = i + 1
                    b = int(node_index[v])
                    sorted_nodes[a], sorted_nodes[b] = sorted_nodes[b], sorted_nodes[a]
                    node_index[sorted_nodes[a]], node_index[sorted_nodes[b]] = node_index[sorted_nodes[b]], node_index[sorted_nodes[a]]
                    start_degrees_index[v_degree] += 2
                    start_degrees_index[v_degree - 1] += 1
                visited_neighbour = True

        #print(degrees)
        #print(sorted_nodes)
        #print("---")
    time_end = time.time()
    print("Calculation time:", time_end - time_start, "seconds")
    return c, nodes_core, ord


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: <input-graph-filename.txt>")
        sys.exit()

    graph_filename = sys.argv[1]
    G, _, _ = load_graph(graph_filename)
    Edges = list(G.edges)
    c, NodesCore, rev_ord = core_decomposition(G)
    print("Core value:", c)
    print("Core value of each node:", NodesCore)
    print("Reverse order of visiting: ", rev_ord)