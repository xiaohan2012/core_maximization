import itertools
from graph_tool import Graph, GraphView
from networkit import Graph as NGraph
from graph_tool.topology import kcore_decomposition

from itertools import combinations


def sort_pair(e):
    return tuple(sorted(e))


def normalize_edges(es):
    return set(map(sort_pair, es))


def complementary_edges(g):
    if isinstance(g, Graph) or isinstance(g, GraphView):
        nodes = list(map(int, g.vertices()))
    else:
        nodes = g.nodes()

    all_edges = set(map(sort_pair, combinations(nodes, 2)))
    return all_edges - set(map(sort_pair, g.edges()))


def edge_set(g):
    return set(map(sort_pair, g.edges()))


def gt_edge2tuple(e):
    return tuple(sorted([int(e.source()), int(e.target())]))


def gt_int_nodes(g):
    """return list of nodes as integer in g
    """
    return list(sorted(map(int, g.vertices())))


def gt_int_edges(g):
    """return list of edges as (int, int) in g
    """
    return list(sorted(map(gt_edge2tuple, g.edges())))


def edge_induced_subgraph(g, edges):
    """
    given graph `g`, return the subgraph that:

    - contains `edges`, which DOES NOT intersect with existing edges in `g`
    - nodes incident to `edges`

    note that the induced subgraph might be disconnected
    """
    vfilt = g.new_vertex_property('bool')
    node_subset = {u for e in edges for u in e}
    vfilt.a = False
    for v in node_subset:
        vfilt[v] = True

    new_g = Graph(directed=False)
    new_g.add_vertex(g.num_vertices())
    new_g.set_vertex_filter(vfilt)
    new_g.add_edge_list(edges)
    return new_g

def has_vertex(g, i):
    # to avoid calling g.vertex, which is heavy
    vfilt = g._Graph__filter_state['vertex_filter'][0]
    if vfilt is None:  # no filter
        return i < g.num_vertices() and i >= 0
    else:
        return vfilt.a[i] > 0


def node_induced_subgraph(g, nodes):
    vfilt = g.new_vertex_property('bool')
    vfilt.a = False
    for v in nodes:
        if has_vertex(g, v):
            vfilt[v] = True
    return GraphView(g, vfilt=vfilt)


def maximal_matching(g, return_unmatched=True):
    """given graph `g`, perform greedy matching algorithm, which gives factor-2 approximation"""
    print(g)
    edges = []
    to_match = set(g.vertices())
    unmatched = []
    while len(to_match) > 0:
        v = next(iter(to_match))  # take a element from the set
        v = g.vertex(int(v))  # need to refresh because graph changes after one step of matching
        print('trying to match', v)
        try:
            e = next(v.out_edges())
            
            s, t = e.source(), e.target()

            print('selected edge', sort_pair([int(s), int(t)]))
            edges.append(sort_pair([int(s), int(t)]))
            to_match.remove(s)
            to_match.remove(t)

            # hide matched nodes
            vfilt = g.get_vertex_filter()[0]
            if vfilt is None:
                vfilt = g.new_vertex_property('bool')
                vfilt.a = True
            for v in [s, t]:
                vfilt[int(v)] = False
            g.set_vertex_filter(vfilt)
            print('g after hiding', g)
            print('g.nodes() after hiding', gt_int_nodes(g))
            print('g.edges() after hiding', gt_int_edges(g))
        except StopIteration:
            to_match.remove(v)
            unmatched.append(int(v))

    if return_unmatched:
        return edges, unmatched
    else:
        return edges


def graph_equal(g1, g2):
    return (set(gt_int_nodes(g1)) == set(gt_int_nodes(g2)) and
            set(gt_int_edges(g1)) == set(gt_int_edges(g2)))


def gt2nk(gt_g):
    """convert from `graph_tool.Graph` to `Networkit.Graph`
    """
    nk_g = NGraph(n=gt_g.num_vertices(), directed=False)
    for e in gt_g.edges():
        nk_g.addEdge(int(e.source()), int(e.target()))
    return nk_g


def get_subcores(g, kcore):
    """get the subcores by running kcore-guided BFS
    """
    visited = {v: False for v in g.vertices()}
    subcores = []
    for v in g.vertices():
        if visited[v]:
            continue
        
        subcore = {int(v)}
        queue = [v]
        while len(queue) > 0:
            v = queue.pop(0)
            visited[v] = True
            for u in v.out_neighbours():
                if not visited[u] and kcore[u] == kcore[v]:
                    visited[u] = True
                    queue.append(u)
                    subcore.add(int(u))
                
        subcores.append(subcore)
    return subcores
