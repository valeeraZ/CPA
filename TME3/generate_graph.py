from TME3.graph import generate_graph, draw_graph, write2file


if __name__ == '__main__':
    P = 0.5
    Q = 0.1
    G, Clusters, _, _ = generate_graph(P, Q)
    draw_graph(G, Clusters)
    write2file(G, "question1.txt")

