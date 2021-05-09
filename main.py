import csv
import time
import networkx as nx
import matplotlib.pyplot as plt
from test_graphs import get_test_graphs
from ACO_graph_colouring import solveACO, draw_graph
from GA_graph_coloring import solveGA


def solve_with_method(graph: nx.Graph, max_iter: int, method: str):
    start = time.time()
    res = None

    if method == "ACO":
        res = solve_with_aco(graph, max_iter)
    if method == "GA":
        res = solve_with_ga(graph, max_iter)

    execution_time = (time.time() - start)  # in seconds
    execution_time = int(execution_time * 1000)  # in milliseconds
    return (execution_time, res)


def solve_with_aco(graph: nx.Graph, max_iter: int):
    return solveACO(graph, iter=1, num_ants=1) #TODO


def solve_with_ga(graph: nx.Graph, max_iter: int):
    return solveGA(graph)


def write_results_to_csv(results):
    with open('results.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['Graph', 'Optimal coloring', 'Max. iters.', 'Method', 'Execution time', 'Colors'])

        for result in results:
            spamwriter.writerow(result)



def main():
    print("Building graphs...")
    graphs, optimal_colorings = get_test_graphs()
    results = []
    max_iter = 10

    print ("Start coloring...")
    for graph, optimal_coloring in zip(graphs[1:2], optimal_colorings[1:2]):
        methods = ["ACO","GA"]
        for method in methods:
            print(f"Coloring {graph.name} with {method}")
            (execution_time, solve_result) = solve_with_method(graph, max_iter, method)
            print(f"\tMethod {method} solved in {execution_time} ms")
            print("\t", solve_result)

            results.append([graph.name, optimal_coloring, max_iter, method, execution_time, solve_result[0]])

        if len(graph.nodes) < 30:
            # TODO color nodes with their colors
            draw_graph(graph, {})
        plt.show()

    print("Done!")
    write_results_to_csv(results)


if __name__ == "__main__":
    main()
