import os
import sys
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
            """
            neighbour = list(graph.neighbors(u))
            degree = len(neighbour)
            """
            # no neighbour
            if degree == 0:
                counter += 1
            else:
                # 1 neighbour
                if degree == 1:
                    v = adj_list.get(u)[0]
                    "v = neighbour[0]"
                    if labels[u] == labels[v]:
                        counter += 1
                    else:
                        labels[u] = labels[v]
                # 1 more neighbours
                else:
                    neighbour_labels = []
                    """
                    for v in neighbour:
                        neighbour_labels.append(labels[v])
                    """
                    for v in adj_list.get(u):
                        neighbour_labels.append(labels[v])
                    new_label = most_frequent(neighbour_labels, labels[u])
                    """
                    new_label = max(neighbour_labels, key=neighbour_labels.count)
                    """
                    if new_label == labels[u]:
                        counter += 1
                    else:
                        labels[u] = new_label
    time_end = time.time()
    print("Calculation time:", time_end - time_start, "seconds")
    return labels


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: <input-graph-filename.txt>")
        sys.exit()

    graph_filename = sys.argv[1]

    print("Label Propagation Algorithm")
    # use a simple graph with 400 nodes and about 20,000 edges
    G, Edges, Nodes = load_graph(graph_filename)
    Labels = Nodes.copy()
    AdjList = makeAdjArray(Edges)
    New_Labels = label_propagation(AdjList, Nodes, Labels)
    labels_unique, partition = np.unique(New_Labels, return_counts=True)
    number_communities = len(labels_unique)

    # save results
    filename = os.path.split(graph_filename)[1]
    graph_name = os.path.splitext(filename)[0]

    community_filename = "lpa_" + graph_name
    f = open("results/" + community_filename+".txt" , "w")
    for i in range(len(New_Labels)):
        label = New_Labels[i]
        f.write(str(i) + "\t" + str(label) + "\n")
    # draw the community result
    draw_graph(G, New_Labels, community_filename+".png")

    print("Results of community exported to results/" + community_filename + ".txt")
    print("Number of clusters/labels:", number_communities)
    print("Partition of nodes in different clusters/labels:", [item for item in partition])
