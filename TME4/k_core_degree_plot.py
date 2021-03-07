import k_core as kc
import pandas as pd
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    # load and calculate graph
    G = kc.load_graph("data/scholar/net.txt",delimiter=" ")
    c, node_core, rev_ord, degrees = kc.core_decomposition(G, degree=True)

    # sort by id and only take the value
    cores = [core for(node, core) in sorted(node_core.items(), key=lambda t: t[0])]
    degrees = [degree for(node, degree) in sorted(degrees.items(), key=lambda t: t[0])]

    tuple = pd.DataFrame(list(zip(cores, degrees)))
    density_dict = tuple.value_counts().to_dict()
    density = [density_dict[i] for i in zip(cores, degrees)]

    fig, ax = plt.subplots()
    ax.set(xscale='log', yscale='log')
    plt.plot(np.arange(0, max(cores)+10), np.arange(0, max(cores)+10), color="black")
    # x, y, color, size, marker, normalize
    points = ax.scatter(degrees, cores, c=density,
                         s=30, marker=',', norm=LogNorm(), cmap="jet")
    plt.colorbar(points)
    plt.title("Google Scholar")
    plt.xlabel('Degree')  # Set x-axis label
    plt.ylabel('Coreness')  # Set y-axis label
    plt.savefig("result/google_scolar_coreness_degree.png")
    plt.show()

    # load name file
    names = pd.read_table('data/scholar/ID.txt', encoding='utf-8', header=None).values.tolist()
    core = max(cores)
    anomalous_nodes = [i for (i, j) in enumerate(cores) if j == core]
    print("Anomalous Authors:")
    for node in anomalous_nodes:
        name = " ".join(names[node]).split(" ", 1)[1]
        print(name)
