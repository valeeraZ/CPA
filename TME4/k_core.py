import sys, os, time
sys.path.append(os.getcwd())
from math import inf, isinf
import networkx as nx
import numpy as np
import pandas as pd


def load_graph(filename, skiprow=0, delimiter=None):
    time_start = time.time()
    print("Start loading graph")
    edges = pd.read_table(filename, dtype=int, skiprows=skiprow, header=None, delimiter=delimiter)
    g = nx.from_pandas_edgelist(edges, 0, 1)
    # mapping = {old_label: new_label for new_label, old_label in enumerate(g.nodes())}
    time_end = time.time()
    print("Number of edges:", len(g.edges))
    print("Number of nodes:", len(g.nodes))
    print("Loading time:", time_end - time_start, "seconds")
    return g


def order_nodes_degree(graph):
    """
    :param graph: nx.Graph
    :return: dict of (node, degree),
    list of nodes sorted by its degree,
    list of indexes where each degree section starts (degree section is sorted),
    location of each node in sorted_node
    """
    # number of nodes
    n = len(graph.nodes)
    # degrees[i] == (i, degree_node_i)
    degrees = dict(graph.degree())
    # (i, degree_node_i)
    max_degree = max(degrees.values())
    # sort nodes, by degree of each node
    sorted_nodes = [node for (node, degree) in sorted(graph.degree, key=lambda t: t[1])]
    # sorted_nodes = list(range(n))

    # indexes where each degree section starts
    start_degrees_index = list(range(max_degree + 1))
    # location of each node in sorted_node
    # node_index = list(range(n))
    node_index = {}

    # a 2-dimension array (dictionary in python) to represent the nodes having a same degree
    ordered_nodes = {i: [] for i in range(max_degree + 1)}

    for (node, index) in zip(graph.nodes, range(n)):
        d = degrees[node]
        ordered_nodes[d].append(node)
    index = 0
    for d in range(max_degree + 1):
        start_degrees_index[d] = index
        for node in ordered_nodes[d]:
            # sorted_nodes[index] = node
            node_index[node] = index
            index += 1
    return degrees, sorted_nodes, start_degrees_index, node_index


def core_decomposition(graph, degree=False):
    """
    core decomposition of a graph
    :param graph: a networkx.Graph
    :param degree: boolean, return degree of graph or not
    :return: a core value of graph,
    a dict of node : core value,
    a dict of node : reverse visiting order,
    a dict of node : degree
    """
    # core value
    c = 0
    # nodes
    n = len(graph.nodes)
    # core of each node, initialised to 0
    nodes_core = {}
    degrees, sorted_nodes, start_degrees_index, node_index = order_nodes_degree(graph)
    time_start = time.time()
    # reverse order of visiting each node
    ord = {}
    print("Calculating core decomposition...")
    for i in range(n):
        u = sorted_nodes[i]
        u_degree = degrees[u]
        ord[u] = n - i
        visited_neighbour = False
        if u_degree > c:
            c = u_degree
        nodes_core[u] = c
        # remove node u from graph: set degree of node u to inf so not to be considered anymore
        degrees[u] = float(inf)
        # iterate its neighbours to decrease their degree
        neighbours = list(graph.neighbors(u))
        for v in neighbours:
            v_degree = degrees[v]
            # consider only nodes with degree != inf
            if not isinf(v_degree):
                # as u is deleted, v's degree will decrease by 1
                degrees[v] = v_degree - 1
                if i < start_degrees_index[v_degree]:
                    a = start_degrees_index[v_degree]
                    b = node_index[v]
                    # swap the head of section with a
                    sorted_nodes[a], sorted_nodes[b] = sorted_nodes[b], sorted_nodes[a]
                    node_index[sorted_nodes[a]], node_index[sorted_nodes[b]] = node_index[sorted_nodes[b]], node_index[
                        sorted_nodes[a]]
                    start_degrees_index[v_degree] += 1
                    if not visited_neighbour:
                        start_degrees_index[u_degree] += 1
                else:
                    a = i + 1
                    b = int(node_index[v])
                    sorted_nodes[a], sorted_nodes[b] = sorted_nodes[b], sorted_nodes[a]
                    node_index[sorted_nodes[a]], node_index[sorted_nodes[b]] = node_index[sorted_nodes[b]], node_index[
                        sorted_nodes[a]]
                    start_degrees_index[v_degree] += 2
                    start_degrees_index[v_degree - 1] += 1
                visited_neighbour = True

        # print(degrees)
        # print(sorted_nodes)
        # print("---")
    time_end = time.time()
    print("Calculation time:", time_end - time_start, "seconds")
    if degree:
        return c, nodes_core, ord, dict(graph.degree)
    else:
        return c, nodes_core, ord


def densest_prefix(ordering, g):
    edges = g.edges
    res = list(np.zeros(len(ordering), int))

    for (e1, e2) in edges:
        e = max(ordering[e1], ordering[e2])
        res[e - 1] = res[e - 1] + 1

    for i in range(1, len(res)):
        res[i] = res[i] + res[i - 1]

    for i in range(1, len(res)):
        res[i] = res[i] / (i + 1)
    return res


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: <input-graph-filename.txt> <optional: header-lines-to-skip>")
        sys.exit()

    graph_filename = sys.argv[1]
    if len(sys.argv) > 2:
        skiprows = int(sys.argv[2])
        G = load_graph(graph_filename, skiprows)
    else:
        G = load_graph(graph_filename)

    c, NodesCore, rev_ord, _ = core_decomposition(G)
    print("Core value:", c)

    add = len(G.edges) / len(G.nodes)
    print("average degree density :", add)

    ed = (2 * len(G.edges)) / (len(G.nodes) * (len(G.nodes) - 1))
    print("the edge density :", ed)

    densest_p = densest_prefix(rev_ord, G)
    max_densest_p = max(densest_p)
    print("maximum value of densest prefix:", max_densest_p)

    k = densest_p.index(max_densest_p) + 1
    print("the size of a densest core ordering prefix:", k)

    # print("Core value of each node:", NodesCore)
