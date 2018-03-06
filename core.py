from util import edge_set


def best_edge(g, glist, cand_edges, debug=False):
    """without pruning
    """
    best_e = None
    best_gain = 0
    for u, v in cand_edges:
        # prev_edges = edge_set(g)
        # if debug:
        #     print('BEST_EDGE: fake insert', u, v)

        promoted_nodes = glist.fake_insert(u, v)
        
        # if debug:
        #     print('BEST_EDGE: gain=', len(promoted_nodes))

        # new_edges = edge_set(g) - prev_edges
        # while new_edges:
        #     print('considering ({},{})'.format(u, v))
        #     print('new edges: {}'.format(new_edges))
        #     glist.remove_edge(u, v)
        #     new_edges = edge_set(g) - prev_edges
        if len(promoted_nodes) > best_gain:
            best_gain = len(promoted_nodes)
            best_e = (u, v)
            if debug:
                print('BEST_EDGE: update {}, score {}'.format(best_e, best_gain))
    return best_e
