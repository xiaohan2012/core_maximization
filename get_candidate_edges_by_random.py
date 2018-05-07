# coding: utf-8

import os
import argparse
import pickle as pkl

from graph_tool import load_graph
from tqdm import tqdm
from graph_helpers import rand_edge


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-g', '--graph',
                        required=True,
                        help='graph name')

    parser.add_argument('-n', '--n_recommendations',
                        type=int, default=10,
                        help='num. of edges to recommend')

    args = parser.parse_args()

    os.environ['OPENBLAS_NUM_THREADS'] = '1'

    n_recommendations = args.n_recommendations

    graph_name = args.graph

    g = load_graph('data/{}/graph.gt'.format(graph_name))

    recommended_edges = set()

    n_edges_to_go = args.n_recommendations * g.num_vertices()
    for i in tqdm(range(n_edges_to_go), total=n_edges_to_go):
        e = rand_edge(g.num_vertices())
        while g.edge(*e) is not None or e in recommended_edges or e[0] == e[1]:
            e = rand_edge(g.num_vertices())
        recommended_edges.add(e)

    output_path = 'data/{}/recommended_edges_N{}_random.pkl'.format(graph_name, n_recommendations)

    # filter out self-loops
    # print('filtering out self-loops')
    recommended_edges = [(u, v)
                         for (u, v) in tqdm(recommended_edges)
                         if u != v]
    for u, v in tqdm(recommended_edges):
        assert u != v
        assert g.edge(u, v) is None, (u, v)

    pkl.dump(
        set(recommended_edges),
        open(output_path, 'wb'))
    print('recommended {} edges'.format(len(set(recommended_edges))))
    print('dumped to {}'.format(output_path))

if __name__ == '__main__':
    main()
