import numpy as np
import pandas as pd
import time
import sys


def readGraph():
    """
    read graph from (i) the list of directed hyperlinks and (ii) the name of the pages corresponding to each node ID
    :return: (list of edges, list of pages, dictionary node_id:node_index)
    """
    time_start = time.time()
    print("Reading files...")

    # Reading
    data_edge = pd.read_table('alr21--dirLinks--enwiki-20071018.txt', skiprows=5, dtype=int, header=None)
    data_page = pd.read_table('alr21--pageNum2Name--enwiki-20071018.txt', skiprows=5, encoding='utf-8', header=None)
    edges = data_edge.values.tolist()
    pages = data_page.values.tolist()
    print("Number of edges:", len(edges))
    print("Number of nodes:", len(pages))

    # make id-index correspondence
    v = 0
    # dictionary id node:index
    node_to_index = {}
    for node in pages:
        node_to_index[node[0]] = v
        v += 1
    for edge in edges:
        edge[0] = node_to_index[edge[0]]
        edge[1] = node_to_index[edge[1]]
    time_end = time.time()
    print("Charge time:", time_end - time_start, "seconds")
    return edges, pages, node_to_index


def pageRank(edges, pages, alpha):
    """
    do page rank
    :param edges: list of edges [[s,t]]
    :param pages: list of pages [[id,'name']]
    :param alpha: alpha value in calculation
    :return: (page rank vector, out degree vector, in degree vector)
    """
    time_start = time.time()
    # Number of nodes
    n = len(pages)
    # Number of edges
    e = len(edges)

    print("Calculating Page Rank value with alpha =", alpha)

    degree_out = np.zeros(n)
    degree_in = np.zeros(n)
    page_rank = np.ones(n) / n
    page_rank_temp = np.zeros(n)
    for i in range(e):
        index = edges[i][0]
        degree_out[index] += 1
    for i in range(e):
        index = edges[i][1]
        degree_in[index] += 1

    var = 100000  # variant of difference inaccuracy between two iterations
    k = 0  # iteration times
    print('loop...')

    while var > 0.000001:
        var = page_rank
        for i in range(e):
            source = edges[i][0]
            dest = edges[i][1]
            if degree_out[source] > 0:
                page_rank_temp[dest] += page_rank[source] / degree_out[source]
        # (1 - alpha) * T * P + alpha * l, where l = vector(N, 1/N)
        page_rank_temp = (1 - alpha) * page_rank_temp + alpha / n
        norm = np.linalg.norm(page_rank_temp, 1)  # ||P||_1
        # normalize
        page_rank = page_rank_temp + (1 - norm) / n
        # inaccuracy
        var = page_rank - var
        var = max(map(abs, var))
        # reinitialize
        page_rank_temp = np.zeros(n)
        k += 1

    time_end = time.time()
    print("Iteration times:", k)
    print("Calculation time:", time_end - time_start, "seconds")
    return page_rank, degree_out, degree_in


def print_highest_lowest_values(page_rank, pages):
    """
    print the 5 highest page rank value with id and name of page and the 5 lowest ones
    :param page_rank: [page_rank_value]
    :param pages: [[id, 'name']]
    :return: nothing
    """
    print("Top 5 highest page rank nodes:")
    t = page_rank.tolist()
    for _ in range(5):
        number = max(t)
        if number >= 0:
            index = t.index(number)
            name = pages[index][1]
            node = pages[index][0]
            print("ID:", node, "Name:", name, "Page Rank value:", number)
            t[index] = -1
    print("Top 5 lowest page rank nodes:")
    t = page_rank.tolist()
    for _ in range(5):
        number = min(t)
        if number <= 1:
            index = t.index(number)
            name = pages[index][1]
            node = pages[index][0]
            print("ID:", node, "Name:", name, "Page Rank value: ", number)
            t[index] = 2


def saveResults2File(page_rank, degree_out, degree_in, pages, alpha):
    """
    save page rank values, out degree vector and in degree vector to files
    :param page_rank: [page_rank_value]
    :param degree_out: [degree]
    :param degree_in: [degree]
    :param pages: [[id, 'name']]
    :param alpha: a float value smaller than 1
    :return: nothing
    """
    print("Writing results to files. Please wait...")
    ids = [iden for [iden, name] in pages]
    data_page_rank = pd.DataFrame(page_rank, index=ids, columns=["Page Rank"])
    data_degree_out = pd.DataFrame(degree_out, index=ids, columns=["Degree Out"])
    data_degree_in = pd.DataFrame(degree_in, index=ids, columns=["Degree In"])
    file_page_rank = "results/" + str(alpha) + "page-rank.txt"
    file_degree_out = "results/degree-out.txt"
    file_degree_in = "results/degree-in.txt"
    data_page_rank.to_csv(file_page_rank, sep="\t")
    data_degree_out.to_csv(file_degree_out, sep="\t")
    data_degree_in.to_csv(file_degree_in, sep="\t")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: <alpha-value>")
        sys.exit()

    # value of alpha
    Alpha = float(sys.argv[1])

    # reading graph
    Edges, Pages, Node_to_Index = readGraph()

    # calculating
    PageRank, DegreeOut, DegreeIn = pageRank(Edges, Pages, Alpha)

    # printing results
    print_highest_lowest_values(PageRank, Pages)

    # save results of page rank to files
    saveResults2File(PageRank, DegreeOut, DegreeIn, Pages, Alpha)
