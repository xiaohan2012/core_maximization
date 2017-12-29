from networkit import Glist
from itertools import combinations


def do_brute_force(g, k, cand_edges):
    glist = Glist(g)
    best_gain = 0
    best_edges = None

    for edges in combinations(cand_edges, k):
        freq = glist.fake_insert_edges(edges)
        gain = sum(freq.values())
        # print(edges, 'gain-->', gain)
        if gain > best_gain:
            best_gain = gain
            best_edges = edges
    return set(best_edges)
