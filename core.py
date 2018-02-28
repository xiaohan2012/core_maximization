from util import edge_set


def best_edge(g, glist, cand_edges):
    """without pruning
    """
    best_e = None
    best_gain = 0
    for u, v in cand_edges:
        # prev_edges = edge_set(g)
        print('fake insert', u, v)
        promoted_nodes = glist.fake_insert(u, v)
        print('gain=', len(promoted_nodes))
        # new_edges = edge_set(g) - prev_edges
        # while new_edges:
        #     print('considering ({},{})'.format(u, v))
        #     print('new edges: {}'.format(new_edges))
        #     glist.remove_edge(u, v)
        #     new_edges = edge_set(g) - prev_edges
        if len(promoted_nodes) > best_gain:
            best_gain = len(promoted_nodes)
            best_e = (u, v)
    return best_e
