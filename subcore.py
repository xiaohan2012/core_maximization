import random
from graph_tool import Graph
from tqdm import tqdm
from graph_tool.topology import kcore_decomposition
from graph_helpers import (edge_induced_subgraph,
                           node_induced_subgraph,
                           maximal_matching,
                           get_subcores,
                           get_degree_ge)


def find_nodes_to_promote(g, subcore_nodes, kcore, degge, debug=False):
    """
    return the set of nodes in `subcore_nodes` such that:

    kcore(v) = deg^{\ge}(v), where deg^{\ge} is the degree received from higher-core nodes

    these nodes are the nodes that edges need to be added on them,
    otherwise, there is no way to promote them

    so for a subcore with a single node, that node is returned
    """
    if debug:
        print('FIND_PROM: subcore_nodes', subcore_nodes)
        print('FIND_PROM: kcore[subcore_nodes]', [kcore[v] for v in subcore_nodes])
        print('FIND_PROM: degge[subcore_nodes]', [degge[v] for v in subcore_nodes])
    return list(filter(lambda v: kcore[v] == degge[v], subcore_nodes))


def partition_promotable_nodes(nodes, cand_edges):
    """
    given a set of nodes, partition them into two groups:

    1. nodes s.t. at least one edge in `cand_edges` cover it ($V_1$ in doc)
    2. otherwise ($V_2$ in doc)
    """
    node_set = set(nodes)
    nodes_coverable = {u for e in cand_edges for u in e}
    return node_set.intersection(nodes_coverable), node_set.difference(nodes_coverable)


def edges_to_promote_subcore_by_maximal_matching(g, subcore_nodes, cand_edges, kcore, degge, debug=False):
    """get the edges to promote as many nodes in subcore as possible using cand_edges by maximal matching

    return:
    - the selected edges
    - unpromotable nodes that need to be promoted
    """
    if len(subcore_nodes) == 1:
        # single node as subcore is a special case
        return [], set(subcore_nodes)
    else:
        promotable_nodes = find_nodes_to_promote(g, subcore_nodes, kcore, degge, debug=debug)
        if debug:
            print('PROMOTE_SC_MM: promotable_nodes', promotable_nodes)

        subg = node_induced_subgraph(
            edge_induced_subgraph(g, cand_edges),
            promotable_nodes)

        if debug:
            from graph_helpers import gt_int_edges, gt_int_nodes
            print('PROMOTE_SC_MM: graphs to match on, nodes', gt_int_nodes(subg))
            print('PROMOTE_SC_MM: graphs to match on, edges', gt_int_edges(subg))

        edges = maximal_matching(subg, return_unmatched=False, debug=debug)

        promoted = {u for e in edges for u in e}
        return edges, set(promotable_nodes) - promoted
    

def edges_to_promote_subcore(g, subcore_nodes, cand_edges, kcore, degge, debug=False):
    """
    given `subcore_nodes`, promote them to the next core
    """
    cand_edge_graph = Graph(directed=False)
    cand_edge_graph.add_vertex(g.num_vertices())
    cand_edge_graph.add_edge_list(cand_edges)
    
    ret_edges, unpromoted = edges_to_promote_subcore_by_maximal_matching(
        g, subcore_nodes, cand_edges, kcore, degge, debug=debug)

    if debug:
        print('PROMOTE_SC: edges by maximal matching:', ret_edges)
        print('PROMOTE_SC: unpromoted:', unpromoted)

    for v in unpromoted:

        if debug:
            print('PROMOTE_SC: promoting {}'.format(v))

        out_edges = cand_edge_graph.vertex(v).out_edges()
        edges_subset = []
        for e in out_edges:
            s, t = map(int, [e.source(), e.target()])
            if kcore[s] < kcore[t]:  # focus on higher-core edges
                edges_subset.append((s, t))

        if debug:
            print('PROMOTE_SC: cand edges', edges_subset)
        
        if len(edges_subset) == 0:
            if debug:
                print('PROMOTE_SC: fail to promote, abort')
            # ABORT: impossible to promote the whole subcore
            return None
        else:            
            e = random.choice(edges_subset)
            if debug:
                print('PROMOTE_SC: selected edge (by random)', e)
            # cand_edge_graph.remove_edge(cand_edge_graph.edge(*e_star))
            ret_edges.append(e)
    
    return ret_edges


def subcore_greedy(g, cand_edges, B, debug=False, log=False, show_progress=True):
    """
    return edges to promote nodes in `g` by calling `edges_to_promote_subcore` greedily

    Note: without cache yet
    """
    cand_edges = set(cand_edges)
    ret_edges = []

    if log:
        log = {'edges_list': []}
    
    kcore = kcore_decomposition(g)
    degge = get_degree_ge(g, kcore)
    subcores = get_subcores(g, kcore)
    # print('subcores', subcores)
    
    subcores = [tuple(sorted(sc)) for sc in subcores]
    B_rem = B
    iter_n = 0
    while B_rem > 0:
        sc2score = {}
        sc2edges = {}

        if show_progress:
            print('iter {}'.format(iter_n))
            iters = tqdm(subcores)
        else:
            iters = subcores

        for sc in iters:
            edges = edges_to_promote_subcore(g, sc, cand_edges, kcore,
                                             degge, debug=False)
            if edges is not None and B_rem >= len(edges):
                sc = tuple(sorted(sc))
                # only promotable subcores under current budget

                if debug:
                    print('SC_GREEDY: considering {}, edges to promote it: {}'.format(sc, edges))
                    # print('--' * 10)

                sc2edges[sc] = edges
                sc2score[sc] = len(sc) / len(edges)

        if len(sc2score) > 0:
            best_sc = max(sc2score.keys(), key=lambda sc: sc2score[sc])
            if debug:
                print('#' * 25)
                print('SC_GREEDY: decided to promote {} using edges {}'.format(best_sc, sc2edges[best_sc]))

            if log:
                log['edges_list'].append(sc2edges[best_sc])

            B_rem -= len(sc2edges[best_sc])
            ret_edges += sc2edges[best_sc]

            # update graph, core and degge
            # NOTE: non-incremental
            # TODO: make it incremental
            # print('adding edges', sc2edges[best_sc])
            g.add_edge_list(sc2edges[best_sc])
            kcore = kcore_decomposition(g)
            degge = get_degree_ge(g, kcore)

            # print('new core number', kcore.a)
            subcores = get_subcores(g, kcore)
            # print('new subcores', subcores)
            cand_edges -= set(sc2edges[best_sc])
        else:
            # no promotable subcores
            break
        print('-' * 20)

    if log:
        return ret_edges, log
    else:
        return ret_edges
