import random
from graph_tool import GraphView, Graph
from graph_tool.topology import kcore_decomposition
from graph_helpers import (edge_induced_subgraph,
                           node_induced_subgraph,
                           maximal_matching,
                           get_subcores)


def find_nodes_to_promote(g, subcore_nodes, kcore):
    """
    return the set of nodes in `subcore_nodes` such that:

    kcore(v) = deg(v, subcore)

    these nodes are potentially promotable by adding **intra-subcore** edges

    so for a subcore with a single node, that node is not returned
    """
    vfilt = g.new_vertex_property('bool')
    for v in subcore_nodes:
        vfilt[v] = True
    sc = GraphView(g, vfilt=vfilt)
    deg = sc.degree_property_map('out')
    # print('subcore_nodes', subcore_nodes)
    # print('kcore.a', kcore.a)
    # print('deg.a', deg.a)
    return list(filter(lambda v: kcore[v] == deg[v], subcore_nodes))


def partition_promotable_nodes(nodes, cand_edges):
    """
    given a set of nodes, partition them into two groups:

    1. nodes s.t. at least one edge in `cand_edges` cover it ($V_1$ in doc)
    2. otherwise ($V_2$ in doc)
    """
    node_set = set(nodes)
    nodes_coverable = {u for e in cand_edges for u in e}
    return node_set.intersection(nodes_coverable), node_set.difference(nodes_coverable)


def edges_to_promote_subcore_by_maximal_matching(g, subcore_nodes, cand_edges, kcore):
    """get the edges to promote as many nodes in subcore as possible using cand_edges by maximal matching

    return:
    - the selected edges
    - unpromotable nodes that need to be promoted
    """
    if len(subcore_nodes) == 1:
        # single node as subcore is a special case
        return [], set(subcore_nodes)
    else:
        promotable_nodes = find_nodes_to_promote(g, subcore_nodes, kcore)
        print('promotable_nodes', promotable_nodes)

        subg = node_induced_subgraph(
            edge_induced_subgraph(g, cand_edges),
            promotable_nodes)
        from graph_helpers import gt_int_edges, gt_int_nodes
        print('graphs to match on, nodes', gt_int_nodes(subg))
        print('graphs to match on, edges', gt_int_edges(subg))
        edges = maximal_matching(subg, return_unmatched=False)

        promoted = {u for e in edges for u in e}
        return edges, set(promotable_nodes) - promoted
    

def edges_to_promote_subcore(g, subcore_nodes, cand_edges, kcore):
    """
    given `subcore_nodes`, promote them to the next core
    """
    cand_edge_graph = Graph(directed=False)
    cand_edge_graph.add_vertex(g.num_vertices())
    cand_edge_graph.add_edge_list(cand_edges)
    
    ret_edges, unpromoted = edges_to_promote_subcore_by_maximal_matching(
        g, subcore_nodes, cand_edges, kcore)

    print('edges by maximal matching:', ret_edges)
    print('unpromoted:', unpromoted)

    for v in unpromoted:
        print('promoting {}'.format(v))
        out_edges = cand_edge_graph.vertex(v).out_edges()
        edges_subset = []
        for e in out_edges:
            s, t = map(int, [e.source(), e.target()])
            if kcore[s] < kcore[t]:  # focus on higher-core edges
                edges_subset.append((s, t))
        print('cand edges', edges_subset)
        
        if len(edges_subset) == 0:
            print('fail to promote, abort')
            # ABORT: impossible to promote the whole subcore
            return None
        else:
            e = random.choice(edges_subset)
            print('selected edge', e)
            # cand_edge_graph.remove_edge(cand_edge_graph.edge(*e_star))
            ret_edges.append(e)
    
    return ret_edges


def subcore_greedy(g, cand_edges, B):
    """
    return edges to promote nodes in `g` by calling `edges_to_promote_subcore` greedily

    Note: without cache yet
    """
    ret_edges = []
    
    kcore = kcore_decomposition(g)
    subcores = get_subcores(g, kcore)
    print('subcores', subcores)

    subcores = [tuple(sorted(sc)) for sc in subcores]
    B_rem = B
    while B_rem > 0:
        sc2score = {}
        sc2edges = {}

        for sc in subcores:
            edges = edges_to_promote_subcore(g, sc, cand_edges, kcore)
            if edges is not None and B_rem >= len(edges):
                sc = tuple(sorted(sc))
                # only promotable subcores under current budget
                print('edges to promote ', sc, 'are ', edges)
                sc2edges[sc] = edges
                sc2score[sc] = len(sc) / len(edges)

        if len(sc2score) > 0:
            best_sc = max(sc2score.keys(), key=lambda sc: sc2score[sc])
            print('promote', best_sc)
            B_rem -= len(sc2edges[best_sc])
            ret_edges += sc2edges[best_sc]

            # update
            # NOTE: non-incremental
            # TODO: make it incremental
            print('adding edges', sc2edges[best_sc])
            g.add_edge_list(sc2edges[best_sc])
            kcore = kcore_decomposition(g)
            print('new core number', kcore.a)
            subcores = get_subcores(g, kcore)
            print('new subcores', subcores)
            # cand_edges -= set(sc2edges[best_sc])
        else:
            # no promotable subcores
            break
        print('-' * 20)
        
    return ret_edges
