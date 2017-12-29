# coding: utf-8

from networkit.graphio import readGraph, Format
from networkit import Glist

from greedy_noninc import do_greedy
from brute_force import do_brute_force
from util import complementary_edges
from graph_tool.all import load_graph, sfdp_layout, graph_draw
from graph_tool.topology import kcore_decomposition


k = 2

g = readGraph('data/karate.edgelist', fileformat=Format.EdgeListSpaceOne)

cand_edges = complementary_edges(g)


glist = Glist(g)
prev_score = sum(glist.core)
print('prev_score={}'.format(sum(glist.core)))


greedy_edges = do_greedy(g, k, cand_edges)


def get_score(g, edges):
    for u, v in edges:
        g.addEdge(u, v)
    score = sum(Glist(g).core)
    for u, v in edges:
        g.removeEdge(u, v)
    return score


print('greedy score:', get_score(g, greedy_edges))


optimal_edges = do_brute_force(g, 2, cand_edges)


print('optimal score:', get_score(g, optimal_edges))


######################
#  visualization
######################

g = load_graph('data/karate.gml')

pos = sfdp_layout(g)

core = kcore_decomposition(g)
graph_draw(g, pos, vertex_fill_color=core, vertex_text=core,
           output='figs/karate_original.png')


def draw_improvement(g, edges, output_path):
    g.add_edge_list(edges)
    core = kcore_decomposition(g)
    edge_color = g.new_edge_property('int')
    edge_color.set_value(1)
    for u, v in edges:
        edge_color[g.edge(u, v)] = 5
    graph_draw(g, pos, vertex_fill_color=core, vertex_text=core, edge_pen_width=edge_color,
               output=output_path)
    for e in edges:
        g.remove_edge(g.edge(*e))

draw_improvement(g, greedy_edges, output_path='figs/karate_greedy_k2.png')

draw_improvement(g, optimal_edges, output_path='figs/karate_optimal_k2.png')
