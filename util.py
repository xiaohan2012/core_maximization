from graph_tool import Graph, GraphView
from itertools import combinations


def sort_pair(e):
    return tuple(sorted(e))


def complementary_edges(g):
    if isinstance(g, Graph) or isinstance(g, GraphView):
        nodes = list(map(int, g.vertices()))
    else:
        nodes = g.nodes()

    all_edges = set(map(sort_pair, combinations(nodes, 2)))
    return all_edges - set(map(sort_pair, g.edges()))


def edge_set(g):
    return set(map(sort_pair, g.edges()))
