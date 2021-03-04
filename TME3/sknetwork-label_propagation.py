from graph import load_graph, generate_graph, draw_graph
from sknetwork.clustering import PropagationClustering
from sknetwork.utils import edgelist2adjacency
import numpy as np
from networkx.algorithms.community import asyn_lpa_communities, label_propagation_communities

if __name__ == '__main__':
    print("Label Propagation Algorithm of Scikit NetWork & Network X")

    # use a simple graph with 400 nodes and about 20,000 edges
    G, Edges, _ = load_graph('data/n400_p0.8_q0.1.txt')
    print("--Scikit Network--")
    propagation = PropagationClustering()
    adjacency = edgelist2adjacency(list(G.edges))
    New_Labels = propagation.fit_transform(adjacency)
    labels_unique, count = np.unique(New_Labels, return_counts=True)
    print("Number of clusters/labels:", len(labels_unique))
    print("Partition of nodes in different clusters/labels:", [item for item in count])

    print("--NetWorkX--")
    nx_labels = label_propagation_communities(G)
    nx_labels = list(nx_labels)
    print("Number of clusters/labels:", len(nx_labels))
    print("Partition of nodes in different clusters/labels:", [len(item) for item in nx_labels])
