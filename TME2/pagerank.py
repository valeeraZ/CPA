import numpy as np
import time
from itertools import islice

if __name__ == '__main__':
    time_start = time.time()
    # read the undirected graph
    f = open('dirLinks.txt', 'r')
    nodes = set()
    edges = []
    for edge in [line.strip('\n').split() for line in islice(f, 5, None)]:
        edges.append(edge)
        nodes.add(edge[0])
        nodes.add(edge[1])
    print("Number of edges: ", len(edges))
    print("Number of nodes: ", len(nodes))
    N = len(nodes)
    """
    print("edges:")
    print(edges)
    """

    # get id - name
    g = open("pageNum2Name.txt", "r", encoding="UTF-8")
    coordinates = {}
    for co in [line.strip('\n').split() for line in islice(g, 5, None)]:
        coordinates[co[0]] = co[1]
    """
    print("Coordinates of id-name:")
    print(coordinates)
    """
    print("reading ok")

    # turn node Symbol to numbers from 0
    v = 0
    # dictionary id node:index
    node_to_index = {}
    # dictionary index:id node
    index_to_node = {}
    for node in nodes:
        node_to_index[node] = v
        index_to_node[v] = node
        v += 1
    for edge in edges:
        edge[0] = node_to_index[edge[0]]
        edge[1] = node_to_index[edge[1]]
    node_to_index = {}
    time_end = time.time()
    print("Charge time: ", time_end - time_start, "seconds")

    time_start = time.time()
    # init transition matrix T
    # matrix takes too much memory which is impossible to realize
    # use vector(N) here
    T = np.zeros([N, N])
    for edge in edges:
        T[edge[1], edge[0]] = 1
    # calculation of out degree value
    for u in range(N):
        sum_of_col = sum(T[:, u])
        for v in range(N):
            if sum_of_col != 0:
                T[v, u] /= sum_of_col
            else:
                T[v, u] = 1 / N
    """
    print("Transition matrix T':")
    print(T)
    """

    # Matrix A: (1 − alpha) * T
    alpha = 0.15
    A = (1 - alpha) * T
    """
    print("Matrix A: (1 − alpha) * T")
    print(A)
    """

    P_n = np.ones(N) / N
    P_n1 = np.zeros(N)

    e = 100000  # difference inaccuracy between two iterations
    k = 0  # iteration times
    print('loop...')

    while e > 0.00000001:  # 误差在0.00000001
        P_n1 = np.dot(A, P_n) + alpha * 1 / N
        norm = np.linalg.norm(P_n1, 1)  # ||P||_1
        P_n1 += (1 - norm) / N  # normalize
        e = P_n1 - P_n
        e = max(map(abs, e))  # 计算误差
        P_n = P_n1
        k += 1
        # print('iteration %s:' % str(k), P_n1)
    print("iteration times:", k)
    """print("final result: ", P_n)"""

    time_end = time.time()
    print("Calculation time: ", time_end - time_start, "seconds")

    print("Top 5 highest page rank node:")
    t = P_n.tolist()
    for _ in range(5):
        number = max(t)
        if number >= 0:
            index = t.index(number)
            node = index_to_node[index]
            name = coordinates[node]
            print("ID: ", node, " Name: ", name, " Page Rank value: ", number)
            t[index] = -1
    print("Top 5 lowest page rank node:")
    t = P_n.tolist()
    for _ in range(5):
        number = min(t)
        if number <= 1:
            index = t.index(number)
            node = index_to_node[index]
            name = coordinates[node]
            print("ID: ", node, " Name: ", name, " Page Rank value: ", number)
            t[index] = 2
