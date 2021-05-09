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
    return solveACO(graph, iter=max_iter, num_ants=10)


def solve_with_ga(graph: nx.Graph, max_iter: int):
    return solveGA(graph)


def write_results_to_csv(results):
    with open('results.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(['Graph', 'Optimal coloring',
                             'Max. iters.', 'Method', 'Execution time', 'Colors'])

        for result in results:
            csv_writer.writerow(result)


def main():
    print("Building graphs...")
    graphs, optimal_colorings = get_test_graphs()
    results = []
    max_iter = 10

    print("Start coloring...")
    for i, (graph, optimal_coloring) in enumerate(zip(graphs, optimal_colorings)):
        methods = ["ACO"]
        for method in methods:
            print(f"Coloring {graph.name} with {method}, {i}/{len(graphs)}")
            (execution_time, solve_result) = solve_with_method(
                graph, max_iter, method)
            print(f"\tMethod {method} solved in {execution_time} ms")
            print("\t", solve_result)

            results.append([graph.name, optimal_coloring, max_iter,
                            method, execution_time, solve_result[0]])

        # if len(graph.nodes) < 30:
        #     # TODO color nodes with their colors
        #     draw_graph(graph, {})
        plt.show()

    print("Done!")
    write_results_to_csv(results)


if __name__ == "__main__":
    main()
