import itertools
import random
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


def generate_graph(p, q):
    """
    draw a graph of 400 nodes partition into 4 clusters of size 100.
    :param p: Each pair of nodes in the same cluster is connected with a probability p
    :param q: Each pair of nodes in diﬀerent clusters is connected with a probability q <= p
    :return: a Graph
    """
    # number of nodes
    n = 400
    # number of clusters
    c = 4
    # nodes
    nodes = range(n)
    # edges
    edges = []
    # clusters
    clusters = []
    for node in nodes:
        clusters.append(node % c)
    for pair in itertools.combinations(nodes, 2):
        if clusters[pair[0]] == clusters[pair[1]]:
            if random.random() < p:
                edges.append(pair)
        else:
            if random.random() < q:
                edges.append(pair)
    # building graph
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print("Number of nodes: ", len(nodes))
    print("Number of edges: ", len(edges))
    return G, clusters, nodes, edges


def write2file(G, file_name):
    """
    write a graph to file in the format:
    src \t dest \n
    :param G: nx.graph
    :param file_name: name of file
    :return: nothing
    """
    f = open("data/"+file_name, "w")
    f.writelines([str(i) + "\t" + str(j) + "\n" for (i,j) in G.edges()])


def draw_graph(graph, clusters, filename=""):
    pos = nx.nx_agraph.graphviz_layout(graph)
    nx.draw(graph, pos=pos, node_color=clusters, node_size=120)
    if filename != "":
        plt.savefig("graph/" + filename)
    plt.show()


def load_graph(filename):
    """
    load a graph from file of format:
    src dest
    :param filename:
    :return: G: nx.graph, list of edges, list of nodes
    """
    data_edge = pd.read_table(filename, dtype=int, header=None)
    edges = data_edge.values.tolist()
    print("Number of edges:", len(edges))
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])
    print("Number of nodes:", len(nodes))
    # make id-index correspondence
    v = 0
    # dictionary id node:index
    node_to_index = {}
    for node in nodes:
        node_to_index[node] = v
        v += 1
    for edge in edges:
        edge[0] = node_to_index[edge[0]]
        edge[1] = node_to_index[edge[1]]
    nodes = list(node_to_index.values())
    nodes.sort()
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G, edges, nodes


def makeAdjArray(edges):
    """
    make an adjacent array of graph
    :param edges: list of edges [[s,t]]
    :return: adj_array: adjacent array {nodeA: [nodeB, nodeC]}
    """
    adj_array = {}
    for edge in edges:
        if edge[0] not in adj_array.keys():
            adj_array[edge[0]] = [edge[1]]
        else:
            adj_array[edge[0]].append(edge[1])
    return adj_array


def load_community(filename, delimiter="\t"):
    """
    load community from file
    format: id-node id-community
    :param delimiter: delimiter by default is tab
    :param filename: file
    :return: [cluster of node-1, cluster of node-2, ...]
    """
    data_cluster = pd.read_table(filename, dtype=int, header=None, delimiter=delimiter)
    node_clusters = data_cluster.values.tolist()
    clusters = []
    for elem in node_clusters:
        clusters.append(elem[1])
    return clusters