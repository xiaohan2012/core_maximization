from graph_tool import Graph


def gt_int_nodes(g):
    """return list of nodes as integer in g
    """
    return list(sorted(map(int, g.vertices())))


def gt_int_edges(g):
    """return list of edges as (int, int) in g
    """
    return list(sorted(map(lambda e: tuple(sorted(e)), g.edges())))


def edge_induced_subgraph(g, edges):
    """
    given graph `g`, return the subgraph that:

    - contains `edges`, which DOES NOT intersect with existing edges in `g`
    - nodes incident to `edges`

    note that the induced subgraph might be disconnected
    """
    vfilt = g.new_vertex_property('bool')
    node_subset = {u for e in edges for u in e}
    for v in node_subset:
        vfilt[v] = True

    new_g = Graph(directed=False)
    new_g.add_vertex(g.num_vertices())
    new_g.set_vertex_filter(vfilt)
    new_g.add_edge_list(edges)
    return new_g
    

def maximal_matching(g, return_unmatched=True):
    """given graph `g`, perform greedy matching algorithm, which gives factor-2 approximation"""
    edges = []
    to_match = set(g.vertices())
    unmatched = []
    while len(to_match) > 0:
        v = next(iter(to_match))
        try:
            e = next(v.out_edges())
            
            s, t = e.source(), e.target()
            edges.append(tuple(sorted((int(s), int(t)))))
            to_match.remove(s)
            to_match.remove(t)
        except StopIteration:
            to_match.remove(v)
            unmatched.append(v)

    if return_unmatched:
        return edges, unmatched
    else:
        return edges


def graph_equal(g1, g2):
    return (set(gt_int_nodes(g1)) == set(gt_int_nodes(g2)) and
            set(gt_int_edges(g1)) == set(gt_int_edges(g2)))
