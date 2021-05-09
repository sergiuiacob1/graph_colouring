import matplotlib.pyplot as plt
from typing import List
import networkx as nx
import os


def plot_coloring(method_name: str, graph: nx.Graph, num_iter: int, num_colors: List[int]):
    file_name = f"{method_name}_{graph.name}.png"
    ox = list(range(1, num_iter + 1))
    oy = num_colors
    print(ox, oy)

    fig = plt.figure()
    plt.title(file_name)
    plt.plot(ox, oy)
    fig.savefig(os.path.join("plots", file_name))
    plt.close()
