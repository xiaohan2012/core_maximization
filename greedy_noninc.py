from networkit import Glist
from core import best_edge


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
