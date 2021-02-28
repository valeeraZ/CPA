import time

import networkx as nx
import numpy as np


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
    print("Divisive Approach Algorithm")
    G = nx.karate_club_graph()
    print("Number of edges:", len(G.edges))
    print("Number of nodes:", len(G.nodes))
    New_Labels = divisive_approach(G)
    labels_unique, count = np.unique(New_Labels, return_counts=True)
    print("Number of clusters/labels:", len(labels_unique))
    print("Partition of nodes in different clusters/labels:", count)