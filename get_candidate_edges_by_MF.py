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
    recommend_edges = []
    for u in range(g.num_vertices()):
        recommendations = model.recommend(u, adj, N=n_recommendations)
        recommend_edges += [tuple(sorted((u, v))) for v, _ in recommendations]

    output_path = 'data/{}/recommended_edges_N{}.pkl'.format(graph_name, n_recommendations)
    pkl.dump(
        recommend_edges,
        open(output_path, 'wb'))

    # for u, v in recommend_edges:
    #     assert g.edge(u, v) is None, (u, v)

    print('recommended {} edges'.format(len(set(recommend_edges))))
    print('dumped to {}'.format(output_path))

if __name__ == '__main__':
    main()
