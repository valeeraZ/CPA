from TME3.graph import generate_graph, draw_graph, write2file
import numpy as np

if __name__ == '__main__':
    P = [0.3, 0.6, 0.8, 0.8, 1]
    Q = [0.3, 0.3, 0.2, 0.1, 0.1]
    for (p, q) in zip(P, Q):
        G, Clusters, _, _ = generate_graph(p, q)
        filename = "n400_p" + str(p) + "_q" + str(q)
        draw_graph(G, Clusters, filename + ".png")
        write2file(G, filename + ".txt")
        # save the cluster
        cluster_filename = "cluster_c4_" + filename
        f = open("data/" + cluster_filename + ".txt", "w")
        for i in range(len(Clusters)):
            label = Clusters[i]
            f.write(str(i) + "\t" + str(label) + "\n")



