from networkit import Glist


def best_edge(g, glist, cand_edges):
    best_e = None
    best_gain = 0
    for u, v in cand_edges:
        # print('fake insert', u, v)
        promoted_nodes = glist.fake_insert(u, v)
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
        cand_edges.remove((u, v))
        
        inserted_edges.append(tuple(sorted((u, v))))

    return inserted_edges
