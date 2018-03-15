# coding: utf-8

import os
import argparse
import implicit
from graph_tool import load_graph
from graph_tool.spectral import adjacency
import pickle as pkl


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-g', '--graph', help='graph name')

    parser.add_argument('-n', '--n_recommendations',
                        type=int, default=10,
                        help='num. of edges to recommend')

    args = parser.parse_args()

    os.environ['OPENBLAS_NUM_THREADS'] = '1'

    n_recommendations = args.n_recommendations

    graph_name = args.graph

    g = load_graph('data/{}/graph.gt'.format(graph_name))

    adj = adjacency(g)

    model = implicit.als.AlternatingLeastSquares(factors=50)

    # train the model on a sparse matrix of item/user/confidence weights
    model.fit(adj)

    # recommend n_recommendations users for each user
    recommended_edges = []
    for u in range(g.num_vertices()):
        recommendations = model.recommend(u, adj, N=n_recommendations)
        recommended_edges += [tuple(sorted((u, v))) for v, _ in recommendations]

    output_path = 'data/{}/recommended_edges_N{}.pkl'.format(graph_name, n_recommendations)

    # filter out self-loops
    recommended_edges = [(u, v)
                         for (u, v) in recommended_edges
                         if u != v]
    for u, v in recommended_edges:
        assert u != v
        assert g.edge(u, v) is None, (u, v)

    pkl.dump(
        set(recommended_edges),
        open(output_path, 'wb'))
    print('recommended {} edges'.format(len(set(recommended_edges))))
    print('dumped to {}'.format(output_path))

if __name__ == '__main__':
    main()
