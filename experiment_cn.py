import argparse
import os
import pickle as pkl
from graph_tool import load_graph
from baselines import CommonNeighbors
import networkx as nx


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-g', '--graph', help='graph name')
    parser.add_argument('-b', '--budget',
                        type=int,
                        help='number of edges to recommend')
    parser.add_argument('-n', '--n_cand_edges_per_node',
                        type=int,
                        help='number of candidate edges per node')

    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    
    args = parser.parse_args()

    graph_name = args.graph
    budget = args.budget

    print('load graph {}'.format(graph_name))
    # g = load_graph('data/{}/graph.gt'.format(graph_name))
    G = nx.read_edgelist('data/{}/graph.edgelist'.format(graph_name))
    G = nx.convert_node_labels_to_integers(G)
    
    cand_edges_path = 'data/{}/recommended_edges_N{}.pkl'.format(graph_name, args.n_cand_edges_per_node)
    print('reading cand edges from {}'.format(cand_edges_path))
    cand_edges = pkl.load(open(
        cand_edges_path, 'rb'))

    recommender = CommonNeighbors(G)
    rec_edges = recommender.get_top_k_edges(cand_edges, budget)

    output_dir = 'output/{}/cn'.format(graph_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, 'B{}-N{}.pkl'.format(budget, args.n_cand_edges_per_node))
    print('result dumpted to', output_path)

    pkl.dump(rec_edges, open(
        output_path, 'wb'))
