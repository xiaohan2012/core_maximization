from itertools import combinations


def sort_pair(e):
    return tuple(sorted(e))


def complementary_edges(g):
    all_edges = set(map(sort_pair, combinations(g.nodes(), 2)))
    return all_edges - set(map(sort_pair, g.edges()))


def edge_set(g):
    return set(map(sort_pair, g.edges()))
