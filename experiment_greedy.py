# coding: utf-8

import argparse
import pickle as pkl
import os

from networkit import Glist
from graph_tool import load_graph
from graph_tool.topology import kcore_decomposition
from greedy_noninc import do_greedy
from networkit.graphio import readGraph, Format

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-g', '--graph', help='graph name')
    parser.add_argument('-b', '--budget',
                        type=int,
                        help='number of edges to recommend')
    parser.add_argument('-n', '--n_cand_edges_per_node',
                        type=int,
                        help='number of candidate edges per node')

    args = parser.parse_args()

    graph_name = args.graph
    budget = args.budget

    g = readGraph('data/{}/graph.graphml'.format(graph_name), fileformat=Format.GraphML)
    g_gt = load_graph('data/{}/graph.gt'.format(graph_name))

    kcore = kcore_decomposition(g_gt)
    print('sum of core', sum(kcore.a))
    print('num edges', g.numberOfEdges())

    glist = Glist(g)
    prev_score = sum(glist.core)
    print('prev_score={}'.format(sum(glist.core)))

    cand_edges = pkl.load(open(
        'data/{}/recommended_edges_N{}.pkl'.format(graph_name, args.n_cand_edges_per_node), 'rb'))

    greedy_edges = do_greedy(g, budget, cand_edges, debug=False, log=False, show_progress=True)

    output_dir = 'output/{}/greedy'.format(graph_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, 'B{}-N{}.pkl'.format(budget, args.n_cand_edges_per_node))
    print('result dumpted to', output_path)
    pkl.dump(greedy_edges, open(
        output_path, 'wb'))

    core_before = sum(kcore.a)

    g_gt.add_edge_list(greedy_edges)

    core_after = sum(kcore_decomposition(g_gt).a)

    print('core before/after', core_before, core_after)

