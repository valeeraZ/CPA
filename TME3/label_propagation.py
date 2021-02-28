from random import choice, shuffle
from TME3.graph import makeAdjArray, load_graph, generate_graph, draw_graph
import numpy as np
import time


def most_frequent(labels, current_label):
    frequencies = {}
    max_frequencies = []
    max_frequency = 0

    # calculating frequencies
    for label in labels:
        frequencies[label] = frequencies.get(label, 0) + 1

    # calculating max frequency labels
    for label, freq in frequencies.items():
        if freq > max_frequency:
            max_frequency = freq
            max_frequencies.clear()
            max_frequencies.append(label)
        if freq == max_frequency:
            max_frequencies.append(label)
    # check if the current label is among the max frequency labels
    for label in max_frequencies:
        if label == current_label:
            return current_label

    # else, return a random label from the max frequencies label list
    return choice(max_frequencies)


def label_propagation(adj_list, nodes, labels):
    time_start = time.time()
    print("Calculating communities with LPA...")
    n = len(nodes)
    counter = 0
    while counter < n:
        shuffle(nodes)
        counter = 0
        for u in nodes:
            degree = len(adj_list.get(u, []))
            # no neighbour
            if degree == 0:
                counter += 1
            else:
                # 1 neighbour
                if degree == 1:
                    v = adj_list.get(u)[0]
                    if labels[u] == labels[v]:
                        counter += 1
                    else:
                        labels[u] = labels[v]
                # 1 more neighbours
                else:
                    neighbour_labels = []
                    for v in adj_list.get(u):
                        neighbour_labels.append(labels[v])
                    new_label = most_frequent(neighbour_labels, labels[u])
                    if new_label == labels[u]:
                        counter += 1
                    else:
                        labels[u] = new_label
    time_end = time.time()
    print("Calculation time:", time_end - time_start, "seconds")
    return labels


if __name__ == '__main__':
    print("Label Propagation Algorithm")
    # use a simple graph with 400 nodes and about 20,000 edges
    print("Graph 1")
    G, Edges, Nodes = load_graph('data/question1.txt')
    Labels = Nodes.copy()
    AdjList = makeAdjArray(Edges)
    New_Labels = label_propagation(AdjList, Nodes, Labels)
    labels_unique, count = np.unique(New_Labels, return_counts=True)
    print("Number of clusters/labels:", len(labels_unique))
    print("Partition of nodes in different clusters/labels:", count)

    print("---")

    # use a graph with about 900,000 edges
    print("Graph 2")
    G, Edges, Nodes = load_graph('data/amazon.txt')
    AdjList = makeAdjArray(Edges)
    Labels = Nodes.copy()
    Labels = label_propagation(AdjList, Nodes, Labels)
    labels_unique = np.unique(Labels)
    print("Number of clusters/labels:", len(labels_unique))
    # the graph is too immense and meaningless to draw a figure
