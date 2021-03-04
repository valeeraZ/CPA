from sknetwork.clustering import Louvain
from sknetwork.utils import edgelist2adjacency
import numpy as np
from TME3.graph import load_graph

if __name__ == '__main__':
    print("Louvain Algorithm of Scikit NetWork")
    louvain = Louvain()

    # use a simple graph with 400 nodes and about 20,000 edges
    print("Graph 1:")
    G, Edges, Nodes = load_graph('data/n400_p0.8_q0.1.txt')
    adjacency = edgelist2adjacency(Edges)
    New_Labels = louvain.fit_transform(adjacency)
    labels_unique, count = np.unique(New_Labels, return_counts=True)
    print("Number of clusters/labels:", len(labels_unique))
    print("Partition of nodes in different clusters/labels:", count)

    print("---")

    # use a graph with about 900,000 edges
    print("Graph 2:")
    G, Edges, Nodes = load_graph('data/amazon.txt')
    adjacency = edgelist2adjacency(Edges)
    labels = louvain.fit_transform(adjacency)
    labels_unique = np.unique(labels)
    print("Number of clusters:", len(labels_unique))