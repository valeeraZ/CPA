from IPython.display import SVG
import numpy as np
from sknetwork.data import karate_club, painters, movie_actor
from sknetwork.data import load_edge_list
from sknetwork.ranking import PageRank, BiPageRank
from sknetwork.visualization import svg_graph, svg_digraph, svg_bigraph

if __name__ == '__main__':
    graph = load_edge_list('test.csv', directed=True, fast_format=False)
    adjacency = graph.adjacency
    "position = graph.position"
    pagerank = PageRank(damping_factor=0.15)
    scores = pagerank.fit_transform(adjacency)
    print(scores)
    sum = sum(scores)
    print(sum)
    "image = svg_graph(adjacency, position, scores=np.log(scores))"
    "SVG(image)"