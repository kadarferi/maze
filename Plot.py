# -------------------------------------------------------------------------------------------------------
# Plot the maze with escape route :-)
from matplotlib import pyplot as plt

def plot_maze(graph, route, output_file):
    plt.figure(figsize=((graph.ncol - 1) / 5, (graph.nrow - 1) / 5))
    plt.plot([v[0] for v in route], [v[1] for v in route], color='green', linewidth=3)
    plt.xlim(-1, graph.ncol)
    plt.ylim(graph.nrow, -1)
    for barrier in graph.barriers:
        plt.scatter([v[0] for v in barrier], [v[1] for v in barrier], color='black', marker='s', s=100)
    plt.scatter([v[0] for v in graph.mines], [v[1] for v in graph.mines], color='red', marker='X', s=50)
    plt.scatter(*graph.start_point, color='blue', marker='v', s=100)

    # plt.scatter(*goal, color='purple', marker='*', s=100)
    plt.scatter([v[0] for v in graph.end_points], [v[1] for v in graph.end_points], color='purple', marker='*',
                s=100)
    plt.savefig(output_file)
    #plt.show()
