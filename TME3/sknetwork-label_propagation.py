from graph import load_graph, generate_graph, draw_graph
from sknetwork.clustering import PropagationClustering
from sknetwork.utils import edgelist2adjacency
import numpy as np


if __name__ == '__main__':
    print("Label Propagation Algorithm of Scikit NetWork")
    propagation = PropagationClustering()

    # use a simple graph with 400 nodes and about 20,000 edges
    print("Graph 1:")
    G, Edges, Nodes = load_graph('data/n400_p0.8_q0.1.txt')
    Labels = Nodes.copy()
    adjacency = edgelist2adjacency(Edges)
    New_Labels = propagation.fit_transform(adjacency)
    labels_unique, count = np.unique(New_Labels, return_counts=True)
    print("Number of clusters/labels:", len(labels_unique))
    print("Partition of nodes in different clusters/labels:", count)

    print("---")

    # use a graph with about 900,000 edges
    print("Graph 2:")
    G, Edges, Nodes = load_graph('data/amazon.txt')
    adjacency = edgelist2adjacency(Edges)
    New_Labels = propagation.fit_transform(adjacency)
    labels_unique = np.unique(New_Labels)
    print("Number of clusters:", len(labels_unique))