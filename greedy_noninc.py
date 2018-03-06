from tqdm import tqdm
from networkit import Glist
from core import best_edge


def do_greedy(g, k, cand_edges=set(), debug=False, log=False, show_progress=True):
    cand_edges = set(cand_edges)
    glist = Glist(g)
    inserted_edges = []
    if show_progress:
        iters = tqdm(range(k), total=k)
    else:
        iters = range(k)
                    
    for i in iters:
        u, v = best_edge(g, glist, cand_edges, debug=debug)

        if log:
            print('selected {}, score={}'.format((u, v), len(glist.fake_insert(u, v))))

        glist.insert_edge(u, v)

        cand_edges.remove((u, v))

        inserted_edges.append(tuple(sorted((u, v))))

    # revert back
    for u, v in inserted_edges:
        g.removeEdge(u, v)
    cand_edges |= set(inserted_edges)
    return inserted_edges
