import os
import numpy as np
from graph import load_community, draw_graph, load_graph

graphs = ["n400_p0.3_q0.3.txt", "n400_p0.6_q0.3.txt",
          "n400_p0.8_q0.1.txt", "n400_p0.8_q0.2.txt",
          "benchmark_n128_e1024.txt", "benchmark_n1000_e8000.txt"]

louvain_res = ["louvain_n400_p0.3_q0.3.txt", "louvain_n400_p0.6_q0.3.txt",
               "louvain_n400_p0.8_q0.1.txt", "louvain_n400_p0.8_q0.2.txt",
               "louvain_benchmark_n128_e1024.txt", "louvain_benchmark_n1000_e8000.txt"]


if __name__ == '__main__':
    print("Loading Louvain Algorithm's results")
    for i in range(len(louvain_res)):

        louvain_filename = louvain_res[i]
        graph_filename = graphs[i]

        print("---")
        print("Louvain Algorithm's result of graph " + graph_filename)

        cluster = load_community("results/" + louvain_filename, delimiter=" ")
        graph, _, _ = load_graph("data/" + graph_filename)

        labels_unique, partition = np.unique(cluster, return_counts=True)
        number_communities = len(labels_unique)

        community_filename = os.path.splitext(louvain_filename)[0]
        draw_graph(graph, cluster, community_filename+".png")

        print("Picture of communities exported to graph/" + community_filename + ".png")
        print("Number of communities:", number_communities)
        print("Partition of nodes in different clusters/labels:", [item for item in partition])