from pagerank_highPerformance import readGraph, print_highest_lowest_values
import time
import numpy as np
import pandas as pd
import sys


def readInterestedCategories(interested_categories, node_to_index):
    """
    get all pages by interested categories
    :param interested_categories: the interested categories [interested_category_id]
    :param node_to_index: dictionary node_id:node_index {node_id:node_index}
    :return: [pages_index]
    """
    data_page_category = pd.read_table('alr21--pageCategList--enwiki--20071018.txt', dtype=str, skiprows=5, header=None)
    page_categories = data_page_category.values.tolist()
    interested_pages = []
    for page_category in page_categories:
        if isinstance(page_category[1], str):
            categories = page_category[1].split()
            interested = list(set(interested_categories) & set(categories))
            if interested:
                interested_pages.append(page_category[0])
    # turn id to index
    for i in range(len(interested_pages)):
        page = interested_pages[i]
        interested_pages[i] = node_to_index[int(page)]
    return interested_pages


def pageRankPersonalized(edges, pages, alpha, interested_pages):
    """
    do page rank
    :param edges: list of edges [[s,t]]
    :param pages: list of pages [[id,'name']]
    :param alpha: alpha value in calculation
    :param interested_pages: list of interested pages [page_id]
    :return: (page rank vector, out degree vector, in degree vector)
    """
    time_start = time.time()
    # Number of nodes
    n = len(pages)
    # Number of edges
    e = len(edges)

    print("Calculating Personalized Page Rank value of categories Chess and Boxing with alpha =", alpha)

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
    # rooted page rank, if a,b,c are pages with interested categories then p_0[a] = p_0[b] = p_0[c] = 1/3, the other = 0
    p_0 = np.zeros(n)
    for page in interested_pages:
        p_0[page] = 1 / len(interested_pages)
    print('loop...')

    while var > 0.000001:
        var = page_rank
        for i in range(e):
            source = edges[i][0]
            dest = edges[i][1]
            if degree_out[source] > 0:
                page_rank_temp[dest] += page_rank[source] / degree_out[source]
        # (1 - alpha) * T * P + alpha * P_0
        page_rank_temp = (1 - alpha) * page_rank_temp + alpha * p_0
        norm = np.linalg.norm(page_rank_temp, 1)  # ||P||_1
        # normalize with rooted page rank p_0
        page_rank = page_rank_temp + p_0 * ((1 - norm) / n)
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

    # getting interested pages
    InterestedPage = readInterestedCategories(Interests, Node_Index)

    # calculating
    PageRank, DegreeOut, DegreeIn = pageRankPersonalized(Edges, Pages, Alpha, InterestedPage)

    # printing results
    print_highest_lowest_values(PageRank, Pages)
