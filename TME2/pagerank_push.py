from pagerank_highPerformance import readGraph, print_highest_lowest_values
from pagerank_personalized import readInterestedCategories
import sys
import numpy as np
import time


def approximatePageRank(edges, pages, alpha, interested_pages, adj_array):
    """
    push method
    :param edges: list of edges [[s,t]]
    :param pages: list of pages [[id,'name']]
    :param alpha: alpha value in calculation
    :param interested_pages: list of interested pages [page_id]
    :param adj_array: adjacent array {nodeA: [nodeB, nodeC]}
    :return: page rank vector
    """
    time_start = time.time()
    # Number of nodes
    n = len(pages)
    # Number of edges
    e = len(edges)

    print("Calculating Personalized Page Rank value of categories Chess / Boxing with alpha =", alpha)

    p = np.zeros(n, dtype="double")
    r = np.zeros(n, dtype="double")
    for index in interested_pages:
        r[index] = 1 / len(interested_pages)

    eps = 0.000001  # precision, variant of difference inaccuracy between two iterations
    degree_out = np.zeros(n)
    for i in range(e):
        index = edges[i][0]
        degree_out[index] += 1

    # a queue containing those vertices with r(u)/d(u) >= epsilon
    queue_push = []
    for source in interested_pages:
        if eps * degree_out[source] < 1:
            queue_push.append(source)
    k = 0  # push iteration times
    print('loop...')

    while len(queue_push) > 0:
        u = queue_push.pop()
        p[u] += alpha * r[u]
        tmp = (1 - alpha) * r[u] / 2
        r[u] = tmp
        "r[u] = (1 - alpha) * r[u] / 2"
        "r[u] = 0"
        # all the vertex 'v' connected to 'u'
        if u in adj_array:
            for v in adj_array[u]:
                r[v] += tmp / degree_out[u]
                if r[v] > eps * degree_out[v]:
                    queue_push.append(v)
        k += 1

    time_end = time.time()
    print("Push Operation times:", k)
    print("Calculation time:", time_end - time_start, "seconds")
    return p


def makeAdjArray(edges):
    """
    make an adjacent array of graph
    :param edges: list of edges [[s,t]]
    :return: adj_array: adjacent array {nodeA: [nodeB, nodeC]}
    """
    adj_array = {}
    for edge in edges:
        if edge[0] not in adj_array.keys():
            adj_array[edge[0]] = [edge[1]]
        else:
            adj_array[edge[0]].append(edge[1])
    return adj_array


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: <alpha-value> <interest_category_id_1> <interest_category_id_2> ... <interest_category_id_n>")
        sys.exit()

    # value of alpha
    Alpha = float(sys.argv[1])

    # interested categories ID
    Interests = []
    for i in range(2, len(sys.argv)):
        Interests.append(sys.argv[i])

    # reading graph
    Edges, Pages, Node_Index = readGraph()

    # make an adjacent array
    AdjArray = makeAdjArray(Edges)

    # getting interested pages
    InterestedPage = readInterestedCategories(Interests, Node_Index)

    # calculating
    PageRank = approximatePageRank(Edges, Pages, Alpha, InterestedPage, AdjArray)

    # printing results
    print_highest_lowest_values(PageRank, Pages)
