from networkit import Glist
from util import edge_set


def best_edge(g, glist, cand_edges):
    best_e = None
    best_gain = 0
    for u, v in cand_edges:
        prev_edges = edge_set(g)
        # print('fake insert', u, v)
        promoted_nodes = glist.fake_insert(u, v)
        new_edges = edge_set(g) - prev_edges
        while new_edges:
            print('considering ({},{})'.format(u, v))
            print('new edges: {}'.format(new_edges))
            glist.remove_edge(u, v)
            new_edges = edge_set(g) - prev_edges
        if len(promoted_nodes) > best_gain:
            best_gain = len(promoted_nodes)
            best_e = (u, v)
    return best_e


def do_greedy(g, k, cand_edges=set()):
    glist = Glist(g)
    inserted_edges = []
    for i in range(k):
        u, v = best_edge(g, glist, cand_edges)
        # print('selected', u, v)
        glist.insert_edge(u, v)
        # print('score for ({}, {}) = {}'.format(u, v, len(glist.fake_insert(u, v))))
        cand_edges.remove((u, v))

        inserted_edges.append(tuple(sorted((u, v))))

    # revert back
    for u, v in inserted_edges:
        g.removeEdge(u, v)
    cand_edges |= set(inserted_edges)
    return inserted_edges
