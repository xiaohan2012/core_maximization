from graph_tool import GraphView
from graph_helpers import (edge_induced_subgraph,
                           node_induced_subgraph,
                           maximal_matching)


def find_nodes_to_promote(g, subcore_nodes, kcore):
    """
    return the set of nodes in `subcore_nodes` () such that:

    kcore(v) = deg(v, subcore)
    """
    vfilt = g.new_vertex_property('bool')
    for v in subcore_nodes:
        vfilt[v] = True
    sc = GraphView(g, vfilt=vfilt)
    deg = sc.degree_property_map('out')
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


def promote_subcore_by_maximal_matching(g, subcore_nodes, cand_edges, kcore):
    """promote as many nodes in subcore as possible using cand_edges by maximal matching

    return:
    - the selected edges
    - unpromoted promotable nodes
    """
    promotable_nodes = find_nodes_to_promote(g, subcore_nodes, kcore)

    subg = node_induced_subgraph(
        edge_induced_subgraph(g, cand_edges),
        promotable_nodes)
    edges = maximal_matching(subg, return_unmatched=False)

    promoted = {u for e in edges for u in e}
    return edges, set(promotable_nodes) - promoted
    

def promote_subcore(g, subcore_nodes, cand_edges, kcore):
    """
    given `subcore_nodes`, promote them to the next core
    """

    ret_edges, unpromoted = promote_subcore_by_maximal_matching(
        g, subcore_nodes, cand_edges, kcore)
    
    for v in unpromoted:
        pass  # TODO

    return ret_edges
