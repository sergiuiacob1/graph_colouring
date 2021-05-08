import os
import networkx as nx
from typing import List


def get_test_graphs() -> List[nx.Graph]:
    # return nx.graph_atlas_g()[1:100]
    # TODO add graph names

    names = ["Path graph (10)", "Complete graph (30)", "Balanced Tree (2, 3)", "Barbell graph (5, 1)", "Binomial tree (4)",
             "Circular ladder graph (5)", "Cycle graph (10)", "Star graph (10)", "Wheel graph (6)"]
    optimal_colorings = [0] * len(names)  # TODO
    graphs = [nx.path_graph(10), nx.complete_graph(30), nx.balanced_tree(2, 3), nx.barbell_graph(5, 1), nx.binomial_tree(4),
              nx.circular_ladder_graph(5), nx.cycle_graph(10), nx.star_graph(10), nx.wheel_graph(6)]

    # load graph instances
    # TODO serialize these reads – it takes a lot of time
    # TODO only keep files which aren't too large – ACO needs an adjancy matrix
    # for file in os.listdir("./instances"):
    #     new_graph = nx.Graph()
    #     with open(os.path.join("instances", file), "r") as f:
    #         # data = f.read()
    #         edges = []
    #         line = f.readline()
    #         line.strip()
    #         while line:
    #             if " " not in line:
    #                 break
    #             # need indexes to be from 0
    #             edges.append([int(x) - 1 for x in line.split(" ")])
    #             line = f.readline()
    #             line.strip()

    #         # last line is the optimal coloring
    #         if line == '?':
    #             continue  # ignore graphs for which we don't know the optimal coloring
    #         names.append(file)
    #         optimal_colorings.append(line)
    #         new_graph.add_edges_from(edges)
    #         graphs.append(new_graph)

    for i, g in enumerate(graphs):
        g.name = names[i]
    return graphs, optimal_colorings
