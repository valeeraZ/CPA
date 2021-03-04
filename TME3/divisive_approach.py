import os
import sys
import time

import networkx as nx
import numpy as np
from graph import load_graph, draw_graph


# deep copy a graph
def clone_graph(G):
    cloned_graph = nx.Graph()
    for edge in G.edges():
        cloned_graph.add_edge(edge[0], edge[1])
    return cloned_graph


# modularity Q
def cal_Q(partition, G):
    """
    Modularity is the fraction of the edges that fall within the given groups
    minus the expected such fraction if edges were distributed at random.
    :param partition: community
    :param G: a nx.graph
    :return: value of Q
    """
    # number of links
    m = len(list(G.edges()))
    f = []
    e = []
    # we suppose the fraction of edges fell in community (M_s / M) = f
    for community in partition:
        # sum of degree inside the community
        t = 0
        for i in range(len(community)):
            for j in range(len(community)):
                if i != j:
                    if G.has_edge(community[i], community[j]):
                        t += 1
        # each edge is counted 2 times so divided by 2
        f.append(t / float(2 * m))
    # we suppose the expectation of a random edge belonging(distributed) to the community (D_s / 2m) = e
    for community in partition:
        # number of edges in the community
        t = 0
        for node in community:
            t += len(list(G.neighbors(node)))
        e.append(t / float(2 * m))
    # sum
    q = 0
    for fi, ei in zip(f, e):
        q += (fi - ei ** 2)
    return q


def divisive_approach(graph):
    """
    a modularity-based algorithm, by deleting the weakest links in graph;
    edge betweenness is the negatively relevant strength score for a link
    :param graph: a nx.Graph
    :return: labels of each node
    """
    time_start = time.time()
    print("Calculating communities with DA...")
    g = clone_graph(graph)
    partitions = [[n for n in g.nodes()]]
    labels = list(g.nodes())
    max_q = 0.0
    while len(g.edges()) > 0:
        edge = max(nx.edge_betweenness_centrality(g).items(),
                   key=lambda item: item[1])[0]
        g.remove_edge(edge[0], edge[1])
        components = [list(c) for c in list(nx.connected_components(g))]
        if len(components) != len(partitions):
            q = cal_Q(components, graph)
            if q > max_q:
                max_q = q
                partitions = components
    for i in range(len(partitions)):
        for node in partitions[i]:
            labels[node] = i
    time_end = time.time()
    print("Calculation time:", time_end - time_start, "seconds")
    return labels


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: <input-graph-filename.txt>")
        sys.exit()

    graph_filename = sys.argv[1]
    print("Divisive Approach Algorithm")
    G, _ ,_ = load_graph(graph_filename)
    New_Labels = divisive_approach(G)
    labels_unique, partition = np.unique(New_Labels, return_counts=True)
    number_communities = len(labels_unique)

    # save results
    filename = os.path.split(graph_filename)[1]
    graph_name = os.path.splitext(filename)[0]

    community_filename = "div_" + graph_name
    f = open("results/" + community_filename + ".txt", "w")
    for i in range(len(New_Labels)):
        label = New_Labels[i]
        f.write(str(i) + "\t" + str(label) + "\n")
    # draw the community result
    draw_graph(G, New_Labels, community_filename + ".png")

    print("Results of community exported to results/" + community_filename + ".txt")
    print("Number of clusters/labels:", number_communities)
    print("Partition of nodes in different clusters/labels:", [item for item in partition])