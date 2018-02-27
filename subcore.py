from graph_tool import GraphView


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
