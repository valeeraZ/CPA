import networkx as nx
import sklearn.metrics.cluster as sk
from graph import load_graph, load_community
import numpy as np

# LPA & Louvain

graphs = ["n400_p0.3_q0.3.txt", "n400_p0.6_q0.3.txt",
          "n400_p0.8_q0.1.txt", "n400_p0.8_q0.2.txt",
          "benchmark_n128_e1024.txt", "benchmark_n1000_e8000.txt"]

clusters = ["cluster_c4_n400_p0.3_q0.3.txt", "cluster_c4_n400_p0.6_q0.3.txt",
            "cluster_c4_n400_p0.8_q0.1.txt", "cluster_c4_n400_p0.8_q0.2.txt",
            "cluster_c4_benchmark_n128_e1024.txt", "cluster_c31_benchmark_n1000_e8000.txt"]

lpa_res = ["lpa_c4_n400_p0.3_q0.3.txt", "lpa_c3_n400_p0.6_q0.3.txt",
           "lpa_c6_n400_p0.8_q0.1.txt", "lpa_c2_n400_p0.8_q0.2.txt",
           "lpa_c10_benchmark_n128_e1024.txt", "lpa_c47_benchmark_n1000_e8000.txt"]

louvain_res = ["louvain_n400_p0.3_q0.3.txt", "louvain_n400_p0.6_q0.3.txt",
               "louvain_n400_p0.8_q0.1.txt", "louvain_n400_p0.8_q0.2.txt",
               "louvain_benchmark_n128_e1024.txt", "louvain_benchmark_n1000_e8000.txt"]

# divisive appraoch

graphs_div = ["benchmark_n128_e1024.txt"]

clusters_div = ["cluster_c4_benchmark_n128_e1024.txt"]

da_res = ["div_c4_benchmark_n128_e1024.txt"]

if __name__ == '__main__':
    for i in range(len(graphs)):
        graph_file = graphs[i]
        cluster_file = clusters[i]
        lpa_file = lpa_res[i]
        louvain_file = louvain_res[i]

        print("---")
        print("Metrics for graph " + graph_file)

        graph, edges, nodes = load_graph("data/" + graph_file)
        cluster = load_community("data/" + cluster_file)
        lpa = load_community("results/" + lpa_file)
        louvain = load_community("results/" + louvain_file, " ")

        # modularity
        communities = []  # communities : [{1, 2, 3}, {4, 5, 6}, ...partition]
        for l in set(lpa):
            communities.append(set([i for (i, j) in enumerate(lpa) if j == l]))
        print("LPA Modularity:", nx.algorithms.community.modularity(graph, communities))

        communities = []
        for l in set(louvain):
            communities.append(set([i for (i, j) in enumerate(louvain) if j == l]))
        print("Louvain Modularity:", nx.algorithms.community.modularity(graph, communities))

        # AMI
        LPA_AMI = sk.adjusted_mutual_info_score(cluster, lpa)
        Louvain_AMI = sk.adjusted_mutual_info_score(cluster, louvain)
        print("LPA AMI:", LPA_AMI)
        print("Louvain AMI:", Louvain_AMI)

        # RI
        LPA_RI = sk.adjusted_rand_score(cluster, lpa)
        Louvain_RI = sk.adjusted_rand_score(cluster, louvain)
        print("LPA RI:", LPA_RI)
        print("Louvain RI:", Louvain_RI)

        # NMI
        LPA_NMI = sk.normalized_mutual_info_score(cluster, lpa)
        Louvain_NMI = sk.normalized_mutual_info_score(cluster, louvain)
        print("LPA NMI:", LPA_NMI)
        print("Louvain NMI:", Louvain_NMI)

    # divisive approach
    for i in range(len(graphs_div)):
        graph_file = graphs_div[i]
        cluster_file = clusters_div[i]
        da_file = da_res[i]

        print("---")
        print("Metrics for graph " + graph_file)

        graph, edges, nodes = load_graph("data/" + graph_file)
        cluster = load_community("data/" + cluster_file)
        da = load_community("results/" + da_file)

        # modularity
        communities = []  # communities : [{1, 2, 3}, {4, 5, 6}, ...partition]
        for l in set(da):
            communities.append(set([i for (i, j) in enumerate(da) if j == l]))
        print("Divisive Algorithm Modularity:", nx.algorithms.community.modularity(graph, communities))

        # AMI
        DA_AMI = sk.adjusted_mutual_info_score(cluster, da)
        print("Divisive Algorithm AMI:", DA_AMI)

        # RI
        DA_RI = sk.adjusted_rand_score(cluster, da)
        print("Divisive Algorithm RI:", DA_RI)

        # NMI
        DA_NMI = sk.normalized_mutual_info_score(cluster, da)
        print("Divisive Algorithm NMI:", DA_NMI)