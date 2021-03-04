import networkx as nx
from graph import write2file
import numpy as np


if __name__ == '__main__':
    # load graph
    edges = []
    with open("LFR-Benchmark/network.dat") as f:
        header = next(f)
        n = str(header[9:12])
        for line in f:
            edge = line.split('\t')
            edges.append((int(edge[0])-1, int(edge[1])-1))
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])
    clusters = []
    for line in open("LFR-Benchmark/community.dat").readlines():
        clusters.append( int(line.split('\t')[1]) - 1)

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    n = len(nodes)
    e = len(edges)
    labels_unique = np.unique(clusters, return_counts=False)
    number_communities = len(labels_unique)

    # save graph
    write2file(G, "benchmark_n" + str(n) + "_e" + str(e) + ".txt")
    # save community
    f = open("data/"+"cluster_c" + str(number_communities) + "_benchmark_n" + str(n) + "_e" + str(e) + ".txt", "w")
    for i in range(len(clusters)):
        label = clusters[i]
        f.write(str(i) + "\t" + str(label) + "\n")