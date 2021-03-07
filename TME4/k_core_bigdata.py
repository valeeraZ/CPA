import os
import sys
sys.path.append(os.getcwd())
from k_core import load_graph, core_decomposition, densest_prefix


if __name__ == '__main__':
    G = load_graph(sys.stdin, skiprow=4)
    c, _, rev_ord = core_decomposition(G)
    print("Core value:", c)

    add = len(G.edges) / len(G.nodes)
    print("average degree density :", add)

    ed = (2 * len(G.edges)) / (len(G.nodes) * (len(G.nodes) - 1))
    print("the edge density :", ed)

    densest_p = densest_prefix(rev_ord, G)
    max_densest_p = max(densest_p)
    print("maximum value of densest prefix:", max_densest_p)

    k = densest_p.index(max_densest_p) + 1
    print("the size of a densest core ordering prefix:", k)
